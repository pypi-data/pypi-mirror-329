# Generated by Django 3.2.14 on 2024-03-26 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0043_merge_0041_add_s3_fields_0042_auto_20240327_7128'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectMLPort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.IntegerField(default=None, verbose_name='project_id')),
                ('host', models.TextField(null=True, verbose_name='host')),
                ('port', models.IntegerField(default=0, verbose_name='port')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
        ),
    ]
