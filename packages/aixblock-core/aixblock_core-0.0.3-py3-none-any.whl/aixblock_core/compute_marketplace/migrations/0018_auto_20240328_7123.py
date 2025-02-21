# Generated by Django 3.2.14 on 2024-27-03 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compute_marketplace', '0017_auto_20240328_8213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='computegpu',
            name='teraflops',
        ),
        migrations.AddField(
            model_name='computegpu',
            name='serialno',
            field=models.TextField(verbose_name='serialno', null=True),
        ), 
        migrations.AddField(
            model_name='computegpu',
            name='memory_usage',
            field=models.TextField(verbose_name='memory_usage', null=True),
        ),
        migrations.AddField(
            model_name='computegpu',
            name='power_usage',
            field=models.TextField(verbose_name='power_usage', null=True),
        ),
    ]
