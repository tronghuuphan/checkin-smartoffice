from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.fields import BLANK_CHOICE_DASH
from django.conf import settings


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
        return f"{self.name} - {self.year}"


class Student(models.Model):
    SEX_CHOICES = [(0, "Not known"), (1, "Male"), (2, "Female"), (9, "Not applicable")]

    CCCD = models.CharField(primary_key=True, max_length=12)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    sex = models.IntegerField(choices=SEX_CHOICES, default=0)
    birthday = models.DateField(null=True, blank=True)
    classSH = models.ForeignKey(
        ClassSH, on_delete=models.SET_NULL, null=True, related_name="classes"
    )
    active_status = models.BooleanField()

    def __str__(self):
        return f"{self.name} - {self.CCCD}"


class Log(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    mask = models.BooleanField()


class Manager(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=26)
    birthday = models.DateField(blank=True, null=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user} - {self.phone}"
