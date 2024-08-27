# Generated by Django 5.1 on 2024-08-27 03:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_remove_hotelroom_payment_completed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='booking',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.booking'),
        ),
    ]
