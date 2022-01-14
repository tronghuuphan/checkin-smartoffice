from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import ClassSH, Log, Student, Department
from .serializers import DetailStudentSerializer, LogSerializer, ClassSHSerializer, SimpleLogSerializer, StudentSerializer, SimpleClassLogSerializer, DepartmentSerializer
from .paginations import LogPagination, StudentPagination
from .filters import LogFilter, SimpleLogFilter, ClassSHFilter


class DepartmentViewSet(ListModelMixin, GenericViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class ClassSHViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = ClassSH.objects.all().select_related('department')
    serializer_class = ClassSHSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ClassSHFilter


class StudentViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = StudentSerializer
    filter_backends = (SearchFilter,)
    search_fields = ['first_name', 'last_name']
    pagination_class = StudentPagination


    def get_queryset(self):
        return Student.objects.filter(classSH_id=self.kwargs['classSH_pk'])


class DetailStudentViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = Student.objects.all().select_related('classSH', 'classSH__department')
    serializer_class = DetailStudentSerializer


class ClassLogViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = SimpleClassLogSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filter_class = SimpleLogFilter
    pagination_class = LogPagination
    search_fields = ['student__first_name', 'student__last_name']

    def get_queryset(self):
        return Log.objects.filter(student__classSH__id=self.kwargs['classSH_pk']).select_related('student')


class StudentLogViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = SimpleLogSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filter_class = SimpleLogFilter
    pagination_class = LogPagination

    def get_queryset(self):
        return Log.objects.filter(student_id=self.kwargs['student_pk'])


class LogViewSet(ListModelMixin, GenericViewSet):
    queryset = Log.objects.all().select_related(
        'student', 'student__classSH', 'student__classSH__department')
    serializer_class = LogSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filter_class = LogFilter
    pagination_class = LogPagination
    search_fields = ['student__first_name', 'student__last_name']
