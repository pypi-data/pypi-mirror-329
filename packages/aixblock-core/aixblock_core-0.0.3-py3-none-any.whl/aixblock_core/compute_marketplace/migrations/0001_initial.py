# Generated by Django 3.2.14 on 2023-07-21 04:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='compute_marketplace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='name')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now_add=False, verbose_name='created at')),
                ('owner_id', models.IntegerField(verbose_name='owner_id')),
                ('author_id', models.IntegerField(verbose_name='author_id')),
                ('catalog_id', models.IntegerField(verbose_name='catalog_id')),
                ('order', models.TextField(verbose_name='order')),
                ('config', models.TextField(verbose_name='config')),
                ('infrastructure_id', models.TextField(verbose_name='infrastructure_id')),
                ('infrastructure_desc', models.TextField(verbose_name='infrastructure_desc')),
                ('ip_address', models.TextField(verbose_name='ip_address')),
                ('type', models.TextField(verbose_name='type')),
                ('port', models.TextField(verbose_name='port')),
                ('status', models.CharField(choices=[('CREATED', 'Created'), ('IN_PROGRESS', 'In Marketplace'), ('RENTED_BOUGHT', 'Rented/Bought'), ('COMPLETED', 'Completed'), ('PENDING', 'Pending'), ('SUPPEND', 'Suppend'), ('EXPIRED', 'Expired')], default=None, max_length=100, null=True)),
                ('file', models.FileField(verbose_name='file')),
                ('callback_url', models.TextField(verbose_name='callback_url')),
                ('client_id', models.TextField(verbose_name='client_id')),
                ('client_secret', models.TextField(verbose_name='client_secret'))
            ],
        ),
    ]
