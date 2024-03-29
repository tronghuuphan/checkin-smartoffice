from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.fields import BLANK_CHOICE_DASH
from django.conf import settings
from uuid import uuid4
import os

def path_and_rename(instance, filename):
    extension = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, extension)
    return os.path.join('students', filename)

def path_and_rename_manager(instance, filename):
    extension = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, extension)
    return os.path.join('managers', filename)

class Camera(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ClassSH(models.Model):
    name = models.CharField(max_length=255)
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(3000)]
    )
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, related_name="departments"
    )
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Student(models.Model):
    SEX_CHOICES = [(0, "Not known"), (1, "Male"),
                   (2, "Female"), (9, "Not applicable")]

    CCCD = models.CharField(primary_key=True, max_length=12)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    sex = models.IntegerField(choices=SEX_CHOICES, default=0)
    birthday = models.DateField(null=True, blank=True)
    classSH = models.ForeignKey(
        ClassSH, on_delete=models.SET_NULL, null=True, related_name="classes"
    )
    active_status = models.BooleanField(default=True)
    image = models.ImageField(max_length=255, upload_to=path_and_rename)
    trained = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ['classSH']

    def __str__(self):
        return f"{self.CCCD}"


class Log(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    mask = models.BooleanField()
    image = models.CharField(max_length=255, null=True)

    class Meta:
        ordering = ['-date', '-time']


class Manager(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, unique=True, on_delete=models.CASCADE, related_name='managers')
    phone = models.CharField(max_length=26, null=True)
    birthday = models.DateField(blank=True, null=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    image = models.ImageField(max_length=255, null=True, upload_to=path_and_rename_manager)

    def __str__(self):
        return f"{self.user} - {self.phone}"
