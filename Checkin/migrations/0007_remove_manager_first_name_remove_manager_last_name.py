# Generated by Django 4.0.1 on 2022-01-19 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Checkin', '0006_manager_first_name_manager_last_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manager',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='manager',
            name='last_name',
        ),
    ]
