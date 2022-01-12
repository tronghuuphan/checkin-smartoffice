from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClassSHViewSet, LogViewSet, DetailStudentViewSet, StudentViewSet, ClassLogViewSet, StudentLogViewSet
from rest_framework_nested import routers

router = DefaultRouter()
router.register("classSH", viewset=ClassSHViewSet, basename="classSH")
router.register("students", viewset=DetailStudentViewSet, basename="student")
router.register("logs", viewset=LogViewSet, basename="log")

classSH = routers.NestedDefaultRouter(
    parent_router=router,
    parent_prefix="classSH",
    lookup="classSH"
)

classSH.register(
    prefix="students",
    viewset=StudentViewSet,
    basename="classSH-students")

classSH.register(
    prefix="logs",
    viewset=ClassLogViewSet,
    basename="classSH-logs")

students = routers.NestedDefaultRouter(
    parent_router=router,
    parent_prefix="students",
    lookup="student"
)

students.register(
    prefix='logs',
    viewset=StudentLogViewSet,
    basename="student-logs"
)

urlpatterns = router.urls + classSH.urls + students.urls
