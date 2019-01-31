
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from cbmsapi.models import CcCard
from cbmsapi.serializers import CcCardSerializer

class CcCardView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    
    queryset = CcCard.objects.all()

    def get(self, request, format=None):
        data = CcCard.objects.all()
        serializer = CcCardSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CcCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
