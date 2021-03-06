# Generated by Django 4.0.1 on 2022-01-25 13:03

import Checkin.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Checkin', '0011_alter_manager_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='image',
            field=models.FileField(max_length=255, null=True, upload_to=Checkin.models.path_and_rename_manager),
        ),
        migrations.AlterField(
            model_name='student',
            name='image',
            field=models.FileField(max_length=255, upload_to=Checkin.models.path_and_rename),
        ),
    ]
