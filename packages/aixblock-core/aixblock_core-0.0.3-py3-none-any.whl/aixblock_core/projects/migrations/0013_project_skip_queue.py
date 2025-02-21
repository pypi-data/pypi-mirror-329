# Generated by Django 3.1.13 on 2021-11-02 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_auto_20210906_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='skip_queue',
            field=models.CharField(choices=[('REQUEUE_FOR_ME', 'Requeue for me'), ('REQUEUE_FOR_OTHERS', 'Requeue for others'), ('IGNORE_SKIPPED', 'Ignore skipped')], default='REQUEUE_FOR_OTHERS', max_length=100, null=True),
        ),
    ]
