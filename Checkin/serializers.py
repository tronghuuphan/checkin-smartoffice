from django.db.models import fields
from rest_framework import serializers
from .models import (
    Log,
    Student,
    ClassSH,
    Department,
    Manager,
)
from django.conf import settings


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
    department_id = serializers.IntegerField(required=False)
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Manager
        fields = ('id', 'user_id', 'phone',
                  'birthday', 'department_id', 'image',)


class HiddenManagerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Manager
        fields = ('id', 'phone', 'user_id',  'birthday', 'image')


class ListManagerSerializer(serializers.ModelSerializer):
    department_id = serializers.IntegerField(required=False)
    user_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True, source='user.username')
    first_name = serializers.CharField(
        max_length=50, source='user.first_name', read_only=True)
    last_name = serializers.CharField(
        max_length=50, source='user.last_name', read_only=True)
    email = serializers.EmailField(read_only=True, source='user.email')
    date_joined = serializers.DateTimeField(read_only=True, source='user.date_joined')

    class Meta:
        model = Manager
        fields = ('id',
                  'user_id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'phone',
                  'birthday',
                  'department_id',
                  'date_joined',
                  'image',
                  )
