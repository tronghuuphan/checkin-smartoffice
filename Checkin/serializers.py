from django.db.models import fields
from rest_framework import serializers
from .models import Log, Student, ClassSH

class ClassSHSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSH
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    classSH = ClassSHSerializer()
    class Meta:
        model = Student
        fields = ('CCCD', 'first_name', 'last_name', 'email', 'sex', 'birthday', 'image', 'classSH')

class LogSerializer(serializers.ModelSerializer):

    student = StudentSerializer()
    class Meta:
        model = Log
        fields = ('id', 'date', 'time', 'mask', 'image', 'camera', 'student')