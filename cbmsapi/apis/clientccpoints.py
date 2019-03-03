
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
import datetime

from cbmsapi.models import ClientCcPoints
from cbmsapi.serializers import ClientCcPointsSerializer

class ClientCcPointsView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    
    queryset = ClientCcPoints.objects.all()

    def get(self, request, format=None):
        data = ClientCcPoints.objects.all()
        serializer = CcPointsSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CcPointsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
