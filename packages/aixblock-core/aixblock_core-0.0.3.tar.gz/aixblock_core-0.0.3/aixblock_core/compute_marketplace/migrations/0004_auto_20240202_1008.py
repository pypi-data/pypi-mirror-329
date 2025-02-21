# Generated by Django 3.2.14 on 2024-02-02 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compute_marketplace', '0003_auto_20240201_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogcomputemarketplace',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='updated at'),
        ),
        migrations.AlterField(
            model_name='computemarketplace',
            name='config',
            field=models.TextField(default='cpu,ram,gpu_memory,gpu_card', verbose_name='config'),
        ),
    ]
