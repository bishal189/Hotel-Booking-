# Generated by Django 5.1 on 2024-08-28 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_booking_check_in_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelroom',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
