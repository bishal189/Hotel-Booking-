# Generated by Django 5.1 on 2024-08-28 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_amenity_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='check_in_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='booking',
            name='check_out_date',
            field=models.DateTimeField(),
        ),
    ]
