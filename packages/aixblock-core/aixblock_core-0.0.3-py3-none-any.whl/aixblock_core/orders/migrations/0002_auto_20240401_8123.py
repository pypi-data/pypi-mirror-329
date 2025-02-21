# Generated by Django 3.2.23 on 2024-02-06 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='Order',
            name='price',
            field=models.DecimalField(verbose_name='price', max_digits=10, decimal_places=2),
        ),
        migrations.AddField(
            model_name='Order',
            name='payment_code',
            field=models.CharField(max_length=100, verbose_name='payment code', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='Order',
            name='reward_points_used',
            field=models.IntegerField( verbose_name='reward_points_used', default=0, null=True),
        ),
         migrations.AlterField(
            model_name='Order',
            name='total_amount',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='Order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid'), ('completed', 'Completed'), ('canceled', 'Canceled'), ('refund', 'Refund')], default='pending', max_length=20),
        ),
    ]
