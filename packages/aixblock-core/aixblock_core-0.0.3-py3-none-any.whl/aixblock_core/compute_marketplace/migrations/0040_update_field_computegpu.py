# Generated by Django 3.2.14 on 2024-27-03 15:08

from django.db import migrations, models
from django.utils.translation import gettext_lazy as _


class Migration(migrations.Migration):

    dependencies = [
        ("compute_marketplace", "0039_add_field_computegpu"),
    ]

    operations = [
        migrations.AddField(
            model_name="computegpu",
            name="memory",
            field=models.TextField(
                _("memory for gpu convert to bytes"), blank=True, null=True
            ),
        ),
    ]
