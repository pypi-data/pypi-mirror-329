# Generated by Django 3.1.12 on 2021-08-17 11:36

import core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0002_auto_20210310_2044'),
        ('projects', '0011_auto_20210517_2101'),
    ]

    operations = [
        migrations.CreateModel(
            name='Webhook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(help_text='URL of webhook', max_length=2048, verbose_name='URL of webhook')),
                ('send_payload', models.BooleanField(default=True, help_text='If value is False send only action', verbose_name='does webhook send the payload')),
                ('send_for_all_actions', models.BooleanField(default=True, help_text='If value is False - used only for actions from WebhookAction', verbose_name='Use webhook for all actions')),
                ('headers', models.JSONField(default=dict, help_text='Key Value Json of headers', validators=[core.validators.JSONSchemaValidator({'additionalProperties': False, 'maxProperties': 10, 'patternProperties': {'^[a-zA-Z0-9-_]+$': {'type': 'string'}}, 'type': 'object'})], verbose_name='request extra headers of webhook')),
                ('is_active', models.BooleanField(default=True, help_text='If value is False the webhook is disabled', verbose_name='is webhook active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation time', verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Last update time', verbose_name='updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='webhooks', to='organizations.organization')),
                ('project', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='webhooks', to='projects.project')),
            ],
            options={
                'db_table': 'webhook',
            },
        ),
        migrations.CreateModel(
            name='WebhookAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[['PROJECT_CREATED', 'Project created'], ['PROJECT_UPDATED', 'Project updated'], ['PROJECT_DELETED', 'Project deleted'], ['TASKS_CREATED', 'Task created'], ['TASKS_DELETED', 'Task deleted'], ['ANNOTATION_CREATED', 'Annotation created'], ['ANNOTATION_UPDATED', 'Annotation updated'], ['ANNOTATIONS_DELETED', 'Annotation deleted']], db_index=True, help_text='Action value', max_length=128, verbose_name='action of webhook')),
                ('webhook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='webhooks.webhook')),
            ],
            options={
                'db_table': 'webhook_action',
                'unique_together': {('webhook', 'action')},
            },
        ),
    ]
