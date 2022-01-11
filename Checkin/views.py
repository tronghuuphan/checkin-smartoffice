from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import Pagination
from .models import Log
from .serializers import LogSerializer


class LogAPIView(APIView):
    def get(self, request):
        log = Log.objects.all()
        serialize = LogSerializer(log, many=True)
        return Response(serialize.data, status=status.HTTP_200_OK)