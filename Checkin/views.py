from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin
)
from rest_framework.viewsets import (
    GenericViewSet,
    ModelViewSet,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import (
    ClassSH,
    Log,
    Student,
    Department
)
from .serializers import (
    DetailStudentSerializer,
    LogSerializer,
    ClassSHSerializer,
    SimpleLogSerializer,
    StudentSerializer,
    SimpleClassLogSerializer,
    DepartmentSerializer,
    CreateStudentSerializer,
    BaseClassSHSerializer,
)
from .paginations import LogPagination, StudentPagination
from .filters import (
    LogFilter,
    SimpleLogFilter,
    ClassSHFilter,
)


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = (OrderingFilter,)
    ordering_fields = ('name',)


class ClassSHViewSet(ModelViewSet):
    queryset = ClassSH.objects.all().select_related('department')
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = ClassSHFilter
    ordering_fields = ('name', 'year', 'location', 'department')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BaseClassSHSerializer
        return ClassSHSerializer


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['first_name', 'last_name']
    pagination_class = StudentPagination
    ordering = ('last_name',)

    def get_queryset(self):
        return Student.objects.filter(classSH_id=self.kwargs['classSH_pk'])

    def get_serializer_context(self):
        return {'classSH_id': self.kwargs['classSH_pk']}


class DetailStudentViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Student.objects.all().select_related('classSH', 'classSH__department')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateStudentSerializer
        return DetailStudentSerializer


class ClassLogViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = SimpleClassLogSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = SimpleLogFilter
    pagination_class = LogPagination
    search_fields = ['student__first_name', 'student__last_name']
    ordering_fields = ['camera', 'student__last_name', 'date', 'time']

    def get_queryset(self):
        return Log.objects.filter(student__classSH__id=self.kwargs['classSH_pk']).select_related('student')


class StudentLogViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = SimpleLogSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filter_class = SimpleLogFilter
    pagination_class = LogPagination
    ordering_fields = ('date', 'time', 'mask', 'camera')

    def get_queryset(self):
        return Log.objects.filter(student_id=self.kwargs['student_pk'])


class LogViewSet(ListModelMixin, GenericViewSet):
    queryset = Log.objects.all().select_related(
        'student', 'student__classSH', 'student__classSH__department')
    serializer_class = LogSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = LogFilter
    pagination_class = LogPagination
    search_fields = ['student__first_name', 'student__last_name']
    ordering_fields = ['student__classSH', 'camera',
                       'student__last_name', 'date', 'time']
