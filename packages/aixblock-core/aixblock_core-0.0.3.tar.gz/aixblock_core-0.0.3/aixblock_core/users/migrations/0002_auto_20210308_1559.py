# Generated by Django 3.1.4 on 2021-03-08 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_squashed_0009_auto_20210219_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activity_at',
            field=models.DateTimeField(auto_now=True, verbose_name='last annotation activity'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether to treat this user as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
    ]
