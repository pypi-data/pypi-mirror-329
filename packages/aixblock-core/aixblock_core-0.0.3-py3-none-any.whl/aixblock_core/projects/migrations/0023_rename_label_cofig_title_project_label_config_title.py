# Generated by Django 3.2.14 on 2023-04-05 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0022_project_label_cofig_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='label_cofig_title',
            new_name='label_config_title',
        ),
    ]
