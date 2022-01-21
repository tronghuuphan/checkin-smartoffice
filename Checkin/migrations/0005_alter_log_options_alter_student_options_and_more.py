# Generated by Django 4.0.1 on 2022-01-15 13:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Checkin', '0004_log_image_manager_image_student_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='log',
            options={'ordering': ['-date', '-time']},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['classSH']},
        ),
        migrations.AlterField(
            model_name='manager',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='managers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='student',
            name='active_status',
            field=models.BooleanField(default=True),
        ),
    ]