"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
import json
import logging
import os
import datetime
import numbers
import tempfile

from urllib.parse import urljoin, quote

import requests
from core.audio import get_audio_info
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.db import models, transaction
from django.db.models import Q
from django.db.models.signals import post_delete, pre_save, post_save, pre_delete
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField
from django.urls import reverse
from django.utils.timesince import timesince
from django.utils.timezone import now
from django.dispatch import receiver, Signal
from django.core.files.storage import default_storage
from rest_framework.exceptions import ValidationError

from core.feature_flags import flag_set
from core.utils.common import find_first_one_to_one_related_field_by_prefix, string_is_url, load_func, \
    temporary_disconnect_list_signal
from core.utils.params import get_env
from core.label_config import SINGLE_VALUED_TAGS, replace_task_data_undefined_with_config_field
from core.current_request import get_current_request
from data_manager.managers import PreparedTaskManager, TaskManager
from core.bulk_update_utils import bulk_update
from data_import.models import FileUpload
import projects
from data_manager.task_queue_function import Task_Manage_Queue
from core.settings.aixblock_core import RQ_QUEUES
from plugins.plugin_centrifuge import publish_message

logger = logging.getLogger(__name__)

TaskMixin = load_func(settings.TASK_MIXIN)


class Task(TaskMixin, models.Model):
    """ Business tasks from project
    """
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID', db_index=True)
    _data = JSONField('data', name='data', null=False, help_text='User imported or uploaded data for a task. Data is formatted according to '
                                                   'the project label config. You can find examples of data for your project '
                                                   'on the Import page in the AiXBlock Data Manager UI.')

    meta = JSONField('meta', null=True, default=dict,
                     help_text='Meta is user imported (uploaded) data and can be useful as input for an ML '
                               'Backend for embeddings, advanced vectors, and other info. It is passed to '
                               'ML during training/predicting steps.')
    project = models.ForeignKey('projects.Project', related_name='tasks', on_delete=models.CASCADE, null=True,
                                help_text='Project ID for this task')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, help_text='Time a task was created')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_tasks',
                                   on_delete=models.SET_NULL, null=True, verbose_name=_('created by'),
                                   help_text='The user who created this task')
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, help_text='Last time a task was updated')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='updated_tasks',
                                   on_delete=models.SET_NULL, null=True, verbose_name=_('updated by'),
                                   help_text='Last annotator or reviewer who updated this task')
    is_labeled = models.BooleanField(_('is_labeled'), default=False,
                                     help_text='True if the number of annotations for this task is greater than or equal '
                                               'to the number of maximum_completions for the project', db_index=True)
    overlap = models.IntegerField(_('overlap'), default=1, db_index=True,
                                  help_text='Number of distinct annotators that processed the current task')
    file_upload = models.ForeignKey(
        'data_import.FileUpload', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks',
        help_text='Uploaded file used as data source for this task'
    )
    inner_id = models.BigIntegerField(_('inner id'), default=0, null=True,
                                      help_text='Internal task ID in the project, starts with 1')
    updates = ['is_labeled']
    total_annotations = models.IntegerField(_('total_annotations'), default=0, db_index=True,
                                  help_text='Number of total annotations for the current task except cancelled annotations')
    cancelled_annotations = models.IntegerField(_('cancelled_annotations'), default=0, db_index=True,
                                                help_text='Number of total cancelled annotations for the current task')
    total_predictions = models.IntegerField(_('total_predictions'), default=0, db_index=True,
                                  help_text='Number of total predictions for the current task')

    comment_count = models.IntegerField(
        _('comment count'), default=0, db_index=True,
        help_text='Number of comments in the task including all annotations')
    unresolved_comment_count = models.IntegerField(
        _('unresolved comment count'), default=0, db_index=True,
        help_text='Number of unresolved comments in the task including all annotations')
    comment_authors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, default=None,
        related_name='tasks_with_comments', help_text='Users who wrote comments')
    last_comment_updated_at = models.DateTimeField(
        _('last comment updated at'), default=None, null=True, db_index=True,
        help_text='When the last comment was updated')

    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                    verbose_name=_('reviewed by'), help_text='Last reviewer who reviewed this task',
                                    related_name='reviewed_tasks')

    reviewed_result = models.TextField(null=True, verbose_name=_('reviewed result'), help_text='Last review result')

    is_in_review = models.BooleanField(_('is_in_review'), default=False,
                                     help_text='Mark task in in reviewing process', db_index=True, blank=True)

    is_in_qc = models.BooleanField(_('is_in_qc'), default=False,
                                     help_text='Mark task in in qualifying process', db_index=True, blank=True)

    qualified_result = models.TextField(null=True, verbose_name=_('qualified result'), help_text='Last qualify result')

    qualified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                    verbose_name=_('qualified by'), help_text='Last qualifier who qualify this task',
                                     related_name='qualified_tasks')

    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                    verbose_name=_('Assigned to'), help_text='The people who is working on this task')

    is_data_optimized = models.BooleanField(_('is data optimized'), default=False,
                                   help_text='Mark optimization status of the task data', db_index=True, blank=True)

    objects = TaskManager()  # task manager by default
    prepared = PreparedTaskManager()  # task manager with filters, ordering, etc for data_manager app

    class Meta:
        db_table = 'task'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['project', 'is_labeled']),
            models.Index(fields=['project', 'inner_id']),
            models.Index(fields=['id', 'project']),
            models.Index(fields=['id', 'overlap']),
            models.Index(fields=['overlap']),
            models.Index(fields=['is_labeled'])
        ]

    @property
    def data(self):
        file = self._data.get("text", None)

        if file is not None and len(file) > 6:
            from data_import.models import FileUpload
            file = file[6:]
            file_upload = FileUpload.objects.filter(file=file).last()

            if file_upload is not None:
                file = file_upload.file

                if file.storage.exists(file.name):
                    file.open(mode='r')
                    self._data['text'] = file.read()
                    file.close()

        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def file_upload_name(self):
        return os.path.basename(self.file_upload.file.name)

    def get_locking_user(self, user):
        lock = TaskLock.objects.filter(task=self, expire_at__gt=now()).first()

        if lock is None:
            return None

        return lock.user

    @classmethod
    def get_locked_by(cls, user, project=None, tasks=None):
        """ Retrieve the task locked by specified user. Returns None if the specified user didn't lock anything.
        """
        lock = None
        if project is not None:
            lock = TaskLock.objects.filter(user=user, expire_at__gt=now(), task__project=project).first()
        elif tasks is not None:
            locked_tasks = tasks.filter(locks__user=user, locks__expire_at__gt=now())[:1]
            if locked_tasks:
                return locked_tasks[0]
        else:
            raise Exception('Neither project or tasks passed to get_locked_by')

        if lock:
            return lock.task

    def has_lock(self, user=None):
        """Check whether current task has been locked by some user"""
        num_locks = self.num_locks
        if self.project.skip_queue == self.project.SkipQueue.REQUEUE_FOR_ME:
            num_annotations = self.annotations.filter(ground_truth=False).exclude(Q(was_cancelled=True) | ~Q(completed_by=user)).count()
        else:
            num_annotations = self.annotations.filter(ground_truth=False).exclude(Q(was_cancelled=True) & ~Q(completed_by=user)).count()

        num = num_locks + num_annotations
        if num > self.overlap:
            logger.error(
                f"Num takes={num} > overlap={self.overlap} for task={self.id} - it's a bug",
                extra=dict(
                    lock_ttl=self.get_lock_ttl(),
                    num_locks=num_locks,
                    num_annotations=num_annotations,
                )
            )
        result = bool(num >= self.overlap)
        logger.debug(f'Task {self} locked: {result}; num_locks: {num_locks} num_annotations: {num_annotations}')
        return result

    @property
    def num_locks(self):
        return self.locks.filter(expire_at__gt=now()).count()

    @property
    def storage_filename(self):
        for link_name in settings.IO_STORAGES_IMPORT_LINK_NAMES:
            if hasattr(self, link_name):
                return getattr(self, link_name).key

    def get_lock_ttl(self):
        if settings.TASK_LOCK_TTL is not None:
            return settings.TASK_LOCK_TTL
        return settings.TASK_LOCK_MIN_TTL

    def has_permission(self, user):
        return self.project.has_permission(user)

    def clear_expired_locks(self):
        self.locks.filter(expire_at__lt=now()).delete()

    def set_lock(self, user):
        """Lock current task by specified user. Lock lifetime is set by `expire_in_secs`"""
        num_locks = self.locks.filter(expire_at__gt=now()).exclude(user=user).count()
        if num_locks < self.overlap:
            lock_ttl = self.get_lock_ttl()
            expire_at = now() + datetime.timedelta(seconds=lock_ttl)
            TaskLock.objects.create(task=self, user=user, expire_at=expire_at)
            logger.debug(f'User={user} acquires a lock for the task={self} ttl: {lock_ttl}')
            return True
        else:
            logger.error(
                f"Current number of locks for task {self.id} is {num_locks}, but overlap={self.overlap}: "
                f"that's a bug because this task should not be taken in a label stream (task should be locked)")
            return False
        self.clear_expired_locks()

    def release_lock(self, user=None):
        """Release lock for the task.
        If user specified, it checks whether lock is released by the user who previously has locked that task"""

        if user is None:
            self.locks.all().delete()
            return True

        locks = self.locks.filter(user=user)

        if locks.count() == 0:
            return False

        locks.delete()
        self.clear_expired_locks()
        return True

    def get_storage_link(self):
        # TODO: how to get neatly any storage class here?
        return find_first_one_to_one_related_field_by_prefix(self, '.*io_storages_')

    @staticmethod
    def is_upload_file(filename):
        if not isinstance(filename, str):
            return False
        return filename.startswith(settings.UPLOAD_DIR + '/')

    def resolve_uri(self, task_data, project):
        if project.task_data_login and project.task_data_password:
            protected_data = {}
            for key, value in task_data.items():
                if isinstance(value, str) and string_is_url(value):
                    path = reverse('projects-file-proxy', kwargs={'pk': project.pk}) + '?url=' + quote(value)
                    value = urljoin(settings.HOSTNAME, path)
                protected_data[key] = value
            return protected_data
        else:
            storage_objects = project.get_all_storage_objects(type_='import')

            # try resolve URLs via storage associated with that task
            for field in task_data:
                # file saved in django file storage
                if settings.CLOUD_FILE_STORAGE_ENABLED and self.is_upload_file(task_data[field]):
                    # permission check: resolve uploaded files to the project only
                    file_upload = None
                    file_upload = FileUpload.objects.filter(project=project, file=task_data[field]).first()
                    if file_upload is not None:
                        if flag_set('ff_back_dev_2915_storage_nginx_proxy_26092022_short', self.project.organization.created_by):
                            task_data[field] = file_upload.url
                        else:
                            task_data[field] = default_storage.url(name=task_data[field])
                    # it's very rare case, e.g. user tried to reimport exported file from another project
                    # or user wrote his django storage path manually
                    else:
                        task_data[field] = task_data[field] + '?not_uploaded_project_file'
                    continue

                # project storage
                storage = self.storage or self._get_storage_by_url(task_data[field], storage_objects)
                if storage:
                    try:
                        resolved_uri = storage.resolve_uri(task_data[field])
                    except Exception as exc:
                        logger.debug(exc, exc_info=True)
                        resolved_uri = None
                    if resolved_uri:
                        task_data[field] = resolved_uri
            return task_data

    def _get_storage_by_url(self, url, storage_objects):
        """Find the first compatible storage and returns pre-signed URL"""
        from io_storages.models import get_storage_classes

        for storage_object in storage_objects:
            # check url is string because task can have int, float, dict, list
            # and 'can_resolve_url' will fail
            if isinstance(url, str) and storage_object.can_resolve_url(url):
                return storage_object

    @property
    def storage(self):
        # maybe task has storage link
        storage_link = self.get_storage_link()
        if storage_link:
            return storage_link.storage

        # or try global storage settings (only s3 for now)
        elif get_env('USE_DEFAULT_S3_STORAGE', default=False, is_bool=True):
            # TODO: this is used to access global environment storage settings.
            # We may use more than one and non-default S3 storage (like GCS, Azure)
            from io_storages.s3.models import S3ImportStorage
            return S3ImportStorage()

    @property
    def completed_annotations(self):
        """Annotations that we take into account when set completed status to the task"""
        if self.project.skip_queue == self.project.SkipQueue.IGNORE_SKIPPED:
            return self.annotations.order_by("created_at")
        else:
            return self.annotations.filter(Q_finished_annotations).order_by("created_at")

    def update_is_labeled(self):
        self.is_labeled = self._get_is_labeled_value()

    def increase_project_summary_counters(self):
        if hasattr(self.project, 'summary'):
            summary = self.project.summary
            summary.update_data_columns([self])

    def decrease_project_summary_counters(self):
        if hasattr(self.project, 'summary'):
            summary = self.project.summary
            summary.remove_data_columns([self])

    def ensure_unique_groundtruth(self, annotation_id):
        self.annotations.exclude(id=annotation_id).update(ground_truth=False)

    def save(self, *args, **kwargs):
        if flag_set('ff_back_2070_inner_id_12052022_short', AnonymousUser):
            if self.inner_id == 0:
                task = Task.objects.filter(project=self.project).order_by("-inner_id").first()
                max_inner_id = 1
                if task:
                    max_inner_id = task.inner_id

                # max_inner_id might be None in the old projects
                self.inner_id = None if max_inner_id is None else (max_inner_id + 1)

        send_notify = False

        if self.is_audio_data() and not self.is_data_has_audio_meta():
            if self.calculate_audio_meta():
                if 'update_fields' in kwargs:
                    kwargs['update_fields'] = frozenset(['data']).union(kwargs['update_fields'])

                send_notify = True

        super().save(*args, **kwargs)

        if send_notify:
            self.send_update_signal()

    @staticmethod
    def delete_tasks_without_signals(queryset):
        """
        Delete Tasks queryset with switched off signals
        :param queryset: Tasks queryset
        """
        signals = [
            (post_delete, update_all_task_states_after_deleting_task, Task),
            (pre_delete, remove_data_columns, Task)
        ]
        with temporary_disconnect_list_signal(signals):
            queryset.delete()

    @staticmethod
    def delete_tasks_without_signals_from_task_ids(task_ids):
        queryset = Task.objects.filter(id__in=task_ids)
        Task.delete_tasks_without_signals(queryset)

    def is_audio_data(self):
        return "Audio" in self.project.data_types.values() or "AudioPlus" in self.project.data_types.values()

    def is_data_has_audio_meta(self):
        return "duration" in self._data and "channels" in self._data and "bit_rate" in self._data and "sample_rate" in self._data

    def calculate_audio_meta(self):
        if not self.is_audio_data():
            return False

        _resolved_data = self._data.copy()
        self.resolve_uri(_resolved_data, self.project)
        replace_task_data_undefined_with_config_field(_resolved_data, self.project)
        is_success = False

        for dk in self.project.data_types:
            if self.project.data_types[dk] not in ["Audio", "AudioPlus"]:
                continue

            url = _resolved_data[dk]

            if not url.startswith("http://") or not url.startswith("https://"):
                if not settings.HOSTNAME:
                    print("Can not download audio file: " + url + ". Please set the HOST environment variable.")
                    continue

                url = urljoin(settings.HOSTNAME, url)

            temp_file = tempfile.NamedTemporaryFile("wb")

            try:
                res = requests.get(url)

                if res.ok:
                    temp_file.write(res.content)
                    file = temp_file.name
                    audio_info = get_audio_info(file)

                    if audio_info:
                        self._data = self._data | audio_info
                        is_success = True
                else:
                    print("Can not download audio file: " + url)
            except Exception as e:
                logger.error(f"Can not download audio file: {e}")

            temp_file.close()

        return is_success

        # file = None
        # temp_file = None
        #
        # # Data is file URL, download it
        # if self.file_upload is None:
        #     if self.project is not None:
        #         import copy
        #
        #         data = copy.deepcopy(self._data)
        #         data = self.resolve_uri(data, self.project)
        #         url = data.get("audio", None)
        #     else:
        #         url = self._data.get("audio", None)
        #
        #     import requests
        #     import tempfile
        #
        #     try:
        #         res = requests.get(url)
        #
        #         if res.ok:
        #             temp_file = tempfile.NamedTemporaryFile("wb")
        #             temp_file.write(res.content)
        #             file = temp_file.name
        #         else:
        #             print("Can not download audio file: " + url)
        #     except Exception as e:
        #         logger.error(e)
        # # Data is uploaded file
        # else:
        #     import os
        #
        #     file = self.file_upload.filepath.lstrip("/")
        #     media_path = settings.MEDIA_ROOT.rstrip("/")
        #
        #     if not os.path.isfile(file) and os.path.isfile(media_path + "/" + file):
        #         file = media_path + "/" + file
        #     else:
        #         print("The local audio file is not found")
        #
        # if file is None:
        #     print("The audio file is not found")
        # else:
        #     audio_info = get_audio_info(file)
        #
        #     if audio_info:
        #         self._data = self._data | audio_info
        #
        #     # try:
        #     #     import mutagen
        #     #     file_meta = mutagen.File(file)
        #     #
        #     #     if file_meta is not None:
        #     #         self._data["duration"] = round(file_meta.info.length, 2)
        #     #         self._data["channels"] = file_meta.info.channels
        #     #         print("[mutagen] The duration of the file " + file + " is " + file_meta.info.length.__str__() + "s")
        #     #     else:
        #     #         from ffprobe import FFProbe
        #     #         metadata = FFProbe(file)
        #     #         duration = round(float(metadata.audio[0].duration), 2)
        #     #         self._data["duration"] = duration
        #     #         self._data["channels"] = int(metadata.audio[0].channels)
        #     #         print("[ffprobe] The duration of the file " + file + " is " + duration.__str__() + "s")
        #     # except Exception as e:
        #     #     print("Can not update the audio duration of task #" + self.id.__str__())
        #     #     logger.exception(e)
        #
        # if temp_file is not None:
        #     temp_file.close()

    def send_update_signal(self):
        publish_message(
            channel=f"task/{self.id}",
            data={"command": "update"},
        )

    # def update_qa_state(self):
    #     with transaction.atomic():
    #         # Reverse the applied state of this task to the project
    #         if self.reviewed_result == "approved":
    #             if self.project.is_audio_project():
    #                 self.project.audio_approved_duration -= round(self.data.get("duration", 0), 2)
    #
    #             self.project.qa_approved_tasks -= 1
    #         elif self.reviewed_result == "rejected":
    #             if self.project.is_audio_project():
    #                 self.project.audio_rejected_duration -= round(self.data.get("duration", 0), 2)
    #
    #             self.project.qa_rejected_tasks -= 1
    #
    #         self.reviewed_result = None
    #         self.reviewed_by = None
    #
    #         # Calculate new state for this task and apply this state to project
    #         last_annotation = self.annotations.last()
    #
    #         if last_annotation is not None:
    #             last_state = last_annotation.get_qa_state()
    #
    #             if last_state == "approved":
    #                 if self.project.is_audio_project():
    #                     self.project.audio_approved_duration += round(self.data.get("duration", 0), 2)
    #
    #                 self.project.qa_approved_tasks += 1
    #             elif last_state == "rejected":
    #                 if self.project.is_audio_project():
    #                     self.project.audio_rejected_duration += round(self.data.get("duration", 0), 2)
    #
    #                 self.project.qa_rejected_tasks += 1
    #
    #             self.reviewed_result = last_state
    #             self.reviewed_by = last_annotation.completed_by
    #
    #         self.save(update_fields=[
    #             "reviewed_result",
    #             "reviewed_by",
    #         ])
    #
    #         self.project.save(update_fields=[
    #             "audio_approved_duration",
    #             "audio_rejected_duration",
    #             "qa_approved_tasks",
    #             "qa_rejected_tasks",
    #         ])


pre_bulk_create = Signal(providing_args=["objs", "batch_size"])
post_bulk_create = Signal(providing_args=["objs", "batch_size"])


class AnnotationManager(models.Manager):
    def for_user(self, user):
        return self.filter(task__project__organization=user.active_organization)

    def bulk_create(self, objs, batch_size=None):
        pre_bulk_create.send(sender=self.model, objs=objs, batch_size=batch_size)
        res = super(AnnotationManager, self).bulk_create(objs, batch_size)
        post_bulk_create.send(sender=self.model, objs=objs, batch_size=batch_size)
        return res


GET_UNIQUE_IDS = """
with tt as (
    select jsonb_array_elements(tch.result) as item from task_completion_history tch
    where task=%(t_id)s and task_annotation=%(tc_id)s
) select count( distinct tt.item -> 'id') from tt"""

AnnotationMixin = load_func(settings.ANNOTATION_MIXIN)


class Annotation(AnnotationMixin, models.Model):
    """ Annotations & Labeling results
    """
    objects = AnnotationManager()

    result = JSONField('result', null=True, default=None, help_text='The main value of annotator work - '
                                                                    'labeling result in JSON format')

    task = models.ForeignKey('tasks.Task', on_delete=models.CASCADE, related_name='annotations', null=True,
                             help_text='Corresponding task for this annotation')
    completed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="annotations", on_delete=models.SET_NULL,
                                     null=True, help_text='User ID of the person who created this annotation')
    was_cancelled = models.BooleanField(_('was cancelled'), default=False, help_text='User skipped the task', db_index=True)
    ground_truth = models.BooleanField(_('ground_truth'), default=False, help_text='This annotation is a Ground Truth (ground_truth)', db_index=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, help_text='Creation time')
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, help_text='Last updated time')
    lead_time = models.FloatField(_('lead time'), null=True, default=None, help_text='How much time it took to annotate the task')
    prediction = JSONField(
        _('prediction'),
        null=True, default=dict, help_text='Prediction viewed at the time of annotation')
    result_count = models.IntegerField(_('result count'), default=0,
                                       help_text='Results inside of annotation counter')

    parent_prediction = models.ForeignKey('tasks.Prediction', on_delete=models.SET_NULL, related_name='child_annotations',
                                          null=True, help_text='Points to the prediction from which this annotation was created')
    parent_annotation = models.ForeignKey('tasks.Annotation', on_delete=models.SET_NULL,
                                          related_name='child_annotations',
                                          null=True,
                                          help_text='Points to the parent annotation from which this annotation was created')

    class Meta:
        db_table = 'task_completion'
        indexes = [
            models.Index(fields=['task', 'ground_truth']),
            models.Index(fields=['task', 'completed_by']),
            models.Index(fields=['id', 'task']),
            models.Index(fields=['task', 'was_cancelled']),
            models.Index(fields=['was_cancelled']),
            models.Index(fields=['ground_truth']),
            models.Index(fields=['created_at']),
        ] + AnnotationMixin.Meta.indexes

    def created_ago(self):
        """ Humanize date """
        return timesince(self.created_at)

    def entities_num(self):
        res = self.result
        if isinstance(res, str):
            res = json.loads(res)
        if res is None:
            res = []

        return len(res)

    def has_permission(self, user):
        return self.task.project.has_permission(user)

    def increase_project_summary_counters(self):
        if hasattr(self.task.project, 'summary'):
            logger.debug(f'Increase project.summary counters from {self}')
            summary = self.task.project.summary
            summary.update_created_annotations_and_labels([self])

    def decrease_project_summary_counters(self):
        if hasattr(self.task.project, 'summary'):
            logger.debug(f'Decrease project.summary counters from {self}')
            summary = self.task.project.summary
            summary.remove_created_annotations_and_labels([self])

    def update_task(self):
        update_fields = ['updated_at']
        request = get_current_request()

        # self.task.update_qa_state()

        # updated_by
        if request:
            self.task.updated_by = request.user
            update_fields.append('updated_by')

        self.task.save(update_fields=update_fields)

    def save(self, *args, **kwargs):
        self.check_review_status()

        if not self.pk:
            limit = self.task.project.annotations_limit

            if limit is not None and self.task.annotations.count() >= self.task.project.annotations_limit:
                raise Exception("Can not submit more annotation. "
                                "This task has reached the maximum annotations per task "
                                "(" + limit.__str__() + " annotation" + ("s" if limit > 1 else "") + ")."
                                )

        result = super().save(*args, **kwargs)
        self.update_task()
        return result

    def delete(self, *args, **kwargs):
        self.check_review_status()
        result = super().delete(*args, **kwargs)
        self.on_delete_update_counters()
        self.update_task()
        return result

    def on_delete_update_counters(self):
        task = self.task
        logger.debug(f"Start updating counters for task {task.id}.")
        if self.was_cancelled:
            cancelled = task.annotations.all().filter(was_cancelled=True).count()
            Task.objects.filter(id=task.id).update(cancelled_annotations=cancelled)
            logger.debug(f"On delete updated cancelled_annotations for task {task.id}")
        else:
            total = task.annotations.all().filter(was_cancelled=False).count()
            Task.objects.filter(id=task.id).update(total_annotations=total)
            logger.debug(f"On delete updated total_annotations for task {task.id}")

        logger.debug(f'Update task stats for task={task}')
        task.update_is_labeled()
        Task.objects.filter(id=task.id).update(is_labeled=task.is_labeled)

        # remove annotation counters in project summary followed by deleting an annotation
        logger.debug("Remove annotation counters in project summary followed by deleting an annotation")
        self.decrease_project_summary_counters()

    # def get_qa_state(self):
    #     if self.result is None:
    #         return None
    #
    #     result_state = None
    #
    #     for tmp in self.result:
    #         if "from_name" not in tmp \
    #                 or tmp["from_name"] != "review" \
    #                 or "value" not in tmp \
    #                 or "choices" not in tmp["value"]:
    #             continue
    #
    #         if "Approve" in tmp["value"]["choices"]:
    #             result_state = "approved"
    #         elif "Reject" in tmp["value"]["choices"]:
    #             result_state = "rejected"
    #
    #     return result_state

    def check_review_status(self, user=None):
        if not self.task.project.need_to_qa:
            # try:
            #     task_annotation_name = f'task_annotation_{self.task.project_id}'
            #     connection_params = RQ_QUEUES['custom']
            #     task_annotation = Task_Manage_Queue(task_annotation_name, connection_params)
            #     task_annotation.delete_completed_task(self.task.id)
            # except Exception as e:
            #     print(e)
                
            return

        if not user:
            request = get_current_request()

            if request and request.user:
                user = request.user

        if not user or user.is_superuser:
            return

        is_qa = user.is_qa
        is_qc = user.is_qc
        try:
            from organizations.models import Organization_Project_Permission
            user_role = Organization_Project_Permission.objects.filter(user_id=user.id, project_id=self.task.project.id, deleted_at__isnull=True).order_by("-id").first()
            is_qa = user_role.is_qa
            is_qc = user_role.is_qc
        except Exception as e:
            print(e)

        if self.task.is_in_review and not is_qa:
            raise Exception("Only QA can update task in QA pool.")
        elif self.task.is_in_qc and not is_qc:
            raise Exception("Only QC can update task in QC pool.")
        elif not self.task.is_in_review and not self.task.is_in_qc and (is_qa or is_qc):
            raise Exception("This task is in working pool, only annotators can update it.")


class TaskLock(models.Model):
    task = models.ForeignKey(
        'tasks.Task', on_delete=models.CASCADE, related_name='locks', help_text='Locked task')
    expire_at = models.DateTimeField(_('expire_at'))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='task_locks', on_delete=models.CASCADE,
        help_text='User who locked this task')


class AnnotationDraft(models.Model):
    result = JSONField(
        _('result'),
        help_text='Draft result in JSON format')
    lead_time = models.FloatField(
        _('lead time'), blank=True, null=True,
        help_text='How much time it took to annotate the task')
    task = models.ForeignKey(
        'tasks.Task', on_delete=models.CASCADE, related_name='drafts', blank=True, null=True,
        help_text='Corresponding task for this draft')
    annotation = models.ForeignKey(
        'tasks.Annotation', on_delete=models.CASCADE, related_name='drafts', blank=True, null=True,
        help_text='Corresponding annotation for this draft')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='drafts', on_delete=models.CASCADE,
        help_text='User who created this draft')
    was_postponed = models.BooleanField(
        _('was postponed'),
        default=False,
        help_text='User postponed this draft (clicked a forward button) in the label stream',
        db_index=True
    )

    created_at = models.DateTimeField(_('created at'), auto_now_add=True, help_text='Creation time')
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, help_text='Last update time')

    def created_ago(self):
        """ Humanize date """
        return timesince(self.created_at)

    def has_permission(self, user):
        return self.task.project.has_permission(user)


class Prediction(models.Model):
    """ ML backend predictions
    """
    result = JSONField('result', null=True, default=dict, help_text='Prediction result')
    score = models.FloatField(_('score'), default=None, help_text='Prediction score', null=True)
    model_version = models.TextField(_('model version'), default='', blank=True, null=True)
    cluster = models.IntegerField(_('cluster'), default=None, help_text='Cluster for the current prediction', null=True)
    neighbors = JSONField('neighbors', null=True, blank=True, help_text='Array of task IDs of the closest neighbors')
    mislabeling = models.FloatField(_('mislabeling'), default=0.0, help_text='Related task mislabeling score')

    task = models.ForeignKey('tasks.Task', on_delete=models.CASCADE, related_name='predictions')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def created_ago(self):
        """ Humanize date """
        return timesince(self.created_at) if self.created_at is not None else None

    def has_permission(self, user):
        return self.task.project.has_permission(user)

    @classmethod
    def prepare_prediction_result(cls, result, project):
        """
        This function does the following logic of transforming "result" object:
        result is list -> use raw result as is
        result is dict -> put result under single "value" section
        result is string -> find first occurrence of single-valued tag (Choices, TextArea, etc.) and put string under corresponding single field (e.g. "choices": ["my_label"])  # noqa
        """
        if isinstance(result, list):
            # full representation of result
            for item in result:
                if not isinstance(item, dict):
                    raise ValidationError(f'Each item in prediction result should be dict')
            # TODO: check consistency with project.label_config
            return result

        elif isinstance(result, dict):
            # "value" from result
            # TODO: validate value fields according to project.label_config
            for tag, tag_info in project.get_parsed_config().items():
                tag_type = tag_info['type'].lower()
                if tag_type in result:
                    return [{
                        'from_name': tag,
                        'to_name': ','.join(tag_info['to_name']),
                        'type': tag_type,
                        'value': result
                    }]

        elif isinstance(result, (str, numbers.Integral)):
            # If result is of integral type, it could be a representation of data from single-valued control tags (e.g. Choices, Rating, etc.)  # noqa
            for tag, tag_info in project.get_parsed_config().items():
                tag_type = tag_info['type'].lower()
                if tag_type in SINGLE_VALUED_TAGS and isinstance(result, SINGLE_VALUED_TAGS[tag_type]):
                    return [{
                        'from_name': tag,
                        'to_name': ','.join(tag_info['to_name']),
                        'type': tag_type,
                        'value': {
                            tag_type: [result]
                        }
                    }]
        else:
            raise ValidationError(f'Incorrect format {type(result)} for prediction result {result}')

    def update_task(self):
        update_fields = ['updated_at']

        # updated_by
        request = get_current_request()
        if request:
            self.task.updated_by = request.user
            update_fields.append('updated_by')

        self.task.save(update_fields=update_fields)

    def save(self, *args, **kwargs):
        # "result" data can come in different forms - normalize them to JSON
        self.result = self.prepare_prediction_result(self.result, self.task.project)
        # set updated_at field of task to now()
        self.update_task()
        return super(Prediction, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        result = super().delete(*args, **kwargs)
        # set updated_at field of task to now()
        self.update_task()
        return result

    class Meta:
        db_table = 'prediction'


@receiver(post_delete, sender=Task)
def update_all_task_states_after_deleting_task(sender, instance, **kwargs):
    """ after deleting_task
        use update_tasks_states for all project
        but call only tasks_number_changed section
    """
    try:
        instance.project.update_tasks_states(
            maximum_annotations_changed=False,
            overlap_cohort_percentage_changed=False,
            tasks_number_changed=True
        )
    except Exception as exc:
        logger.error('Error in update_all_task_states_after_deleting_task: ' + str(exc))


# =========== PROJECT SUMMARY UPDATES ===========


@receiver(pre_delete, sender=Task)
def remove_data_columns(sender, instance, **kwargs):
    """Reduce data column counters afer removing task"""
    instance.decrease_project_summary_counters()


def _task_data_is_not_updated(update_fields):
    if update_fields and list(update_fields) == ['is_labeled']:
        return True


@receiver(pre_save, sender=Task)
def delete_project_summary_data_columns_before_updating_task(sender, instance, update_fields, **kwargs):
    """Before updating task fields - ensure previous info removed from project.summary"""
    if _task_data_is_not_updated(update_fields):
        # we don't need to update counters when other than task.data fields are updated
        return
    try:
        old_task = sender.objects.get(id=instance.id)
    except Task.DoesNotExist:
        # task just created - do nothing
        return
    old_task.decrease_project_summary_counters()


@receiver(post_save, sender=Task)
def update_project_summary_data_columns(sender, instance, created, update_fields, **kwargs):
    """Update task counters in project summary in case when new task has been created"""
    if _task_data_is_not_updated(update_fields):
        # we don't need to update counters when other than task.data fields are updated
        return
    instance.increase_project_summary_counters()


@receiver(pre_save, sender=Annotation)
def delete_project_summary_annotations_before_updating_annotation(sender, instance, **kwargs):
    """Before updating annotation fields - ensure previous info removed from project.summary"""
    try:
        old_annotation = sender.objects.get(id=instance.id)
    except Annotation.DoesNotExist:
        # annotation just created - do nothing
        return
    old_annotation.decrease_project_summary_counters()

    # update task counters if annotation changes it's was_cancelled status
    task = instance.task
    if old_annotation.was_cancelled != instance.was_cancelled:
        if instance.was_cancelled:
            task.cancelled_annotations = task.cancelled_annotations + 1
            task.total_annotations = task.total_annotations - 1
        else:
            task.cancelled_annotations = task.cancelled_annotations - 1
            task.total_annotations = task.total_annotations + 1
        task.update_is_labeled()

        Task.objects.filter(id=instance.task.id).update(
            is_labeled=task.is_labeled,
            total_annotations=task.total_annotations,
            cancelled_annotations=task.cancelled_annotations
        )


@receiver(post_save, sender=Annotation)
def update_project_summary_annotations_and_is_labeled(sender, instance, created, **kwargs):
    """Update annotation counters in project summary"""
    instance.increase_project_summary_counters()

    if created:
        # If new annotation created, update task.is_labeled state
        logger.debug(f'Update task stats for task={instance.task}')
        if instance.was_cancelled:
            instance.task.cancelled_annotations = instance.task.annotations.all().filter(was_cancelled=True).count()
        else:
            instance.task.total_annotations = instance.task.annotations.all().filter(was_cancelled=False).count()
        instance.task.update_is_labeled()
        instance.task.save(update_fields=['is_labeled', 'total_annotations', 'cancelled_annotations'])
        logger.debug(f"Updated total_annotations and cancelled_annotations for {instance.task.id}.")


@receiver(pre_delete, sender=Prediction)
def remove_predictions_from_project(sender, instance, **kwargs):
    """Remove predictions counters"""
    instance.task.total_predictions = instance.task.predictions.all().count() - 1
    instance.task.save(update_fields=['total_predictions'])
    logger.debug(f"Updated total_predictions for {instance.task.id}.")


@receiver(post_save, sender=Prediction)
def save_predictions_to_project(sender, instance, **kwargs):
    """Add predictions counters"""
    instance.task.total_predictions = instance.task.predictions.all().count()
    instance.task.save(update_fields=['total_predictions'])
    logger.debug(f"Updated total_predictions for {instance.task.id}.")

# =========== END OF PROJECT SUMMARY UPDATES ===========


@receiver(post_save, sender=Annotation)
def delete_draft(sender, instance, **kwargs):
    task = instance.task
    query_args = {'task': task, 'annotation': instance}
    drafts = AnnotationDraft.objects.filter(**query_args)
    num_drafts = drafts.count()
    drafts.delete()
    logger.debug(f'{num_drafts} drafts removed from task {task} after saving annotation {instance}')


@receiver(post_save, sender=Annotation)
def update_ml_backend(sender, instance, **kwargs):
    if instance.ground_truth:
        return

    project = instance.task.project

    if hasattr(project, 'ml_backends') and project.min_annotations_to_start_training:
        annotation_count = Annotation.objects.filter(task__project=project).count()

        # start training every N annotation
        if annotation_count % project.min_annotations_to_start_training == 0:
            for ml_backend in project.ml_backends.all():
                ml_backend.train()


def update_task_stats(task, stats=('is_labeled',), save=True):
    """Update single task statistics:
        accuracy
        is_labeled
    :param task: Task to update
    :param stats: to update separate stats
    :param save: to skip saving in some cases
    :return:
    """
    logger.debug(f'Update stats {stats} for task {task}')
    if 'is_labeled' in stats:
        task.update_is_labeled()
    if save:
        task.save()


def bulk_update_stats_project_tasks(tasks):
    """bulk Task update accuracy
       ex: after change settings
       apply several update queries size of batch
       on updated Task objects
       in single transaction as execute sql
    :param tasks:
    :return:
    """
    # recalc accuracy
    with transaction.atomic():
        # update objects without saving
        for task in tasks:
            update_task_stats(task, save=False)
            task.send_update_signal()
        # start update query batches
        bulk_update(tasks, update_fields=['is_labeled'], batch_size=settings.BATCH_SIZE)


Q_finished_annotations = Q(was_cancelled=False) & Q(result__isnull=False)
Q_task_finished_annotations = Q(annotations__was_cancelled=False) & \
                              Q(annotations__result__isnull=False)
class TaskQueue(models.Model):
    """ Task Queue
    """
    task_id = models.IntegerField(_('task_id'), default=None, help_text='')
    project_id = models.IntegerField(_('project_id'), default=None, help_text='')
    user_id = models.IntegerField(_('user_id'), default=None, help_text='')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    try_count = models.IntegerField(_('try_count'), default=5, help_text='')
    max_tries = models.IntegerField(_('max_tries'), default=10, help_text='')
    priority = models.IntegerField(_('priority'), default=0, help_text='')
    status = models.TextField(_('status'), default="", help_text='')    
    def update_task(self):
        update_fields = ['updated_at']

        # updated_by
        request = get_current_request()
        if request:
            # self.task.updated_by = request.user
            update_fields.append('updated_by')

        self.save(update_fields=update_fields)

    def save(self, *args, **kwargs):
        # "result" data can come in different forms - normalize them to JSON
        # self.result = self.prepare_prediction_result(self.result, self.task.project)
        # set updated_at field of task to now()
        # self.update_task()
        return super(TaskQueue, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        result = super().delete(*args, **kwargs)
        # set updated_at field of task to now()
        self.update_task()
        return result