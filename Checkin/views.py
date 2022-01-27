from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
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
    Department,
    Manager,
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
    ManagerSerializer,
    HiddenManagerSerializer,
    ListManagerSerializer
)
from .paginations import LogPagination, StudentPagination
from .filters import (
    LogFilter,
    SimpleLogFilter,
    ClassSHFilter,
)
from .permissions import IsAdminOrReadOnly, IsAuthenticatedAndActivated


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = (OrderingFilter,)
    ordering_fields = ('name',)
    permission_classes = [IsAdminOrReadOnly]


class ClassSHViewSet(ModelViewSet):
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = ClassSHFilter
    ordering_fields = ('name', 'year', 'location', 'department')
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        if (self.request.user.is_staff):
            return ClassSH.objects.all().select_related('department')
        elif self.request.user.is_authenticated:
            if self.request.user.managers.department_id is not None:
                return ClassSH.objects.filter(department_id=self.request.user.managers.department_id).select_related('department')
            elif self.request.user.managers.department_id is None:
                return ClassSH.objects.none()
        return ClassSH.objects.all().select_related('department')

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Student.objects.filter(classSH_id=self.kwargs['classSH_pk'])
        return Student.objects.filter(classSH_id=self.kwargs['classSH_pk'], classSH__department_id=self.request.user.managers.department_id)

    def get_serializer_context(self):
        return {'classSH_id': self.kwargs['classSH_pk']}


class DetailStudentViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Student.objects.all().select_related('classSH', 'classSH__department')
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateStudentSerializer
        return DetailStudentSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        allowed_classes_list = list(ClassSH.objects.filter(department_id=self.request.user.managers.department_id).values_list('id', flat=True))
        student_class_id = int(serializer.initial_data['classSH'])
        if student_class_id in allowed_classes_list:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class ClassLogViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = SimpleClassLogSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = SimpleLogFilter
    pagination_class = LogPagination
    search_fields = ['student__first_name', 'student__last_name']
    ordering_fields = ['camera', 'student__last_name', 'date', 'time']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Log.objects.filter(student__classSH__id=self.kwargs['classSH_pk']).select_related('student')
        return Log.objects.filter(student__classSH__id=self.kwargs['classSH_pk'],
                                  student__classSH__department_id=self.request.user.managers.department_id).select_related('student')


class StudentLogViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = SimpleLogSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filter_class = SimpleLogFilter
    pagination_class = LogPagination
    ordering_fields = ('date', 'time', 'mask', 'camera')
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Log.objects.filter(student_id=self.kwargs['student_pk'])


class LogViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Log.objects.all().select_related(
        'student', 'student__classSH', 'student__classSH__department')
    serializer_class = LogSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = LogFilter
    pagination_class = LogPagination
    search_fields = ['student__first_name', 'student__last_name']
    ordering_fields = ['student__classSH', 'camera',
                       'student__last_name', 'date', 'time']


class ManagerViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Manager.objects.all()
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ListManagerSerializer
        return HiddenManagerSerializer

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        manager = Manager.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = ManagerSerializer(manager)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = HiddenManagerSerializer(manager, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
