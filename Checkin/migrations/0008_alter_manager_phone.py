# Generated by Django 4.0.1 on 2022-01-19 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Checkin', '0007_remove_manager_first_name_remove_manager_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='phone',
            field=models.CharField(max_length=26, null=True),
        ),
    ]
