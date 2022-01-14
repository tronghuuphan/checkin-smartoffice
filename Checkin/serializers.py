from django.db.models import fields
from rest_framework import serializers
from .models import Log, Student, ClassSH, Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("id", "name",)


class ClassSHSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = ClassSH
        fields = ("id", "name", "year", "location", "department")


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            "CCCD",
            "first_name",
            "last_name",
            "email",
            "sex",
            "birthday",
            "image",
        )


class DetailStudentSerializer(StudentSerializer):
    classSH = ClassSHSerializer()

    class Meta:
        model = StudentSerializer.Meta.model
        fields = StudentSerializer.Meta.fields + ('classSH',)


class SimpleLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ('id', 'date', 'time', 'mask', 'image', 'camera')


class LogSerializer(SimpleLogSerializer):
    student = DetailStudentSerializer()

    class Meta:
        model = SimpleLogSerializer.Meta.model
        fields = SimpleLogSerializer.Meta.fields + ('student',)


class SimpleClassLogSerializer(LogSerializer):
    student = StudentSerializer()
