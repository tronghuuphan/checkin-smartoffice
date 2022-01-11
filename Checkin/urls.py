from django.urls import path
from .views import LogAPIView

urlpatterns = [
    path('log/', LogAPIView.as_view())
]