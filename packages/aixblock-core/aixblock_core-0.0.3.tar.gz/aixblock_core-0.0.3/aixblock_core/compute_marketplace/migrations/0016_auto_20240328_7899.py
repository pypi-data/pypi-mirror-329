# Generated by Django 3.2.14 on 2024-27-03 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compute_marketplace', '0015_auto_20240327_7489'),
    ]

    operations = [
      
        migrations.AddField(
            model_name='Trade',
            name='resource',
            field=models.CharField(max_length=100, null=True), 

        ),
         migrations.AddField(
            model_name='Trade',
            name='resource_id',
            field=models.IntegerField(null=True),
        ),
         
        migrations.AddField(
            model_name='trade',
            name='payment_method',
            field=models.CharField(max_length=20, choices=[('wallet', 'Electronic Wallet'), ('visa', 'Visa'), ('mastercard', 'MasterCard'), ('reward', 'Reward Point')], default='reward'),
        ),
        
        migrations.AddField(
            model_name='Trade',
            name='order',
            field=models.IntegerField(null=True),
        ),
         
       
    ]
