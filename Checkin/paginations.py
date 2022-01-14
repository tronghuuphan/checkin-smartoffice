from rest_framework.pagination import PageNumberPagination

class LogPagination(PageNumberPagination):
    page_size = 40

class StudentPagination(PageNumberPagination):
    page_size = 30