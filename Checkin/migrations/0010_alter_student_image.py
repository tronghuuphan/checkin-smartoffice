# Generated by Django 4.0.1 on 2022-01-21 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Checkin', '0009_alter_student_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='image',
            field=models.FileField(max_length=255, upload_to=''),
        ),
    ]
