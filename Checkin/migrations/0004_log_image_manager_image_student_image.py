# Generated by Django 4.0.1 on 2022-01-10 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Checkin', '0003_remove_student_name_student_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='image',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='manager',
            name='image',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='image',
            field=models.CharField(max_length=255, null=True),
        ),
    ]