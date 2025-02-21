# Generated by Django 3.2.14 on 2023-10-30 08:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0034_task_is_in_qc'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='qualified_by',
            field=models.ForeignKey(help_text='Last qualifier who qualify this task', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='qualified_tasks', to=settings.AUTH_USER_MODEL, verbose_name='qualified by'),
        ),
        migrations.AddField(
            model_name='task',
            name='qualified_result',
            field=models.TextField(help_text='Last qualify result', null=True, verbose_name='qualified result'),
        ),
        migrations.AlterField(
            model_name='task',
            name='reviewed_by',
            field=models.ForeignKey(help_text='Last reviewer who reviewed this task', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_tasks', to=settings.AUTH_USER_MODEL, verbose_name='reviewed by'),
        ),
         migrations.AddField(
            model_name='task',
            name='assigned_to_id',
            field=models.ForeignKey(help_text='Last reviewer who reviewed this task', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='reviewed by'),
        )
        
    ]
