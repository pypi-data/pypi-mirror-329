# Generated by Django 3.2.14 on 2024-27-03 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compute_marketplace', '0014_auto_20240327_6789'),
    ]

    operations = [
      
        migrations.AddField(
            model_name='Trade',
            name='cost',
            field=models.FloatField(verbose_name='cost of payment with blockchain', null=True, default=0),
        ),
       
    ]
