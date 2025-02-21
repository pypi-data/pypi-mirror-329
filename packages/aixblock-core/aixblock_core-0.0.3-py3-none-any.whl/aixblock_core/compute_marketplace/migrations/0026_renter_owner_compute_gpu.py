# Generated by Django 3.2.14 on 2024-27-03 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compute_marketplace', '0025_auto_20240804_1147'),
    ]

    operations = [
      
        migrations.AlterField(
            model_name='computegpu',
            name='status',
            field=models.CharField(choices=[('created', 'Created'),('completed', 'Completed'), ('renting', 'Renting'), ('pending', 'Pending'),('suppend', 'Suppend'), ('in_marketplace', 'In Marketplace'),('underperformance', 'Underperformance'), ('failed', 'Failed')], default='created', max_length=50),
        ),
        migrations.AddField(
            model_name='computegpu',
            name='owner_id',
            field=models.IntegerField(('owner_id'),null=True)
        ),
        migrations.AddField(
            model_name='computegpu',
            name='renter_id',
            field=models.IntegerField(('renter_id'),null=True)
        ),
        migrations.AlterField(
            model_name='computemarketplace',
            name='status',
            field=models.CharField(choices=[('created', 'Created'),('completed', 'Completed'), ('renting', 'Renting'), ('pending', 'Pending'),('suppend', 'Suppend'), ('in_marketplace', 'In Marketplace'), ('failed', 'Failed')], default='created', max_length=50),
        ),

    ]
