# Generated by Django 5.1 on 2024-08-27 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_remove_booking_payment_completed_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotelroom',
            name='payment_completed',
        ),
        migrations.AddField(
            model_name='booking',
            name='payment_completed',
            field=models.BooleanField(default=False),
        ),
    ]
