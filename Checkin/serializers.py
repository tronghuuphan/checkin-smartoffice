from django.db.models import fields
from rest_framework import serializers
from .models import (
    Log,
    Student,
    ClassSH,
    Department,
    Manager,
)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("id", "name",)


class BaseClassSHSerializer(serializers.ModelSerializer):
    '''Base class for CREATE a new class and base for LIST class'''
    class Meta:
        model = ClassSH
        fields = ("id", "name", "year", "location", "department")


class ClassSHSerializer(BaseClassSHSerializer):
    department = DepartmentSerializer(read_only=True)


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

    def create(self, validated_data):
        classSH_id = self.context['classSH_id']
        return Student.objects.create(classSH_id=classSH_id, **validated_data)


class DetailStudentSerializer(StudentSerializer):
    classSH = ClassSHSerializer()

    class Meta:
        model = StudentSerializer.Meta.model
        fields = StudentSerializer.Meta.fields + ('classSH',)


class CreateStudentSerializer(serializers.ModelSerializer):
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
            "classSH"
        )


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


class ManagerSerializer(serializers.ModelSerializer):
    department_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    class Meta:
        model = Manager
        fields = ('id', 'user_id', 'phone',
                  'birthday', 'department_id', 'image')
