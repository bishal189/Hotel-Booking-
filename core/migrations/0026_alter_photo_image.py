# Generated by Django 5.1 on 2024-08-30 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_photo_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.FileField(upload_to='hotel_photos/'),
        ),
    ]
