
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
import datetime

from cbmsapi.models import ClientSelfLender
from cbmsapi.serializers import ClientSelfLenderSerializer

class ClientSelfLenderView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    
    queryset = ClientSelfLender.objects.all()

    def get(self, request, format=None):
        data = ClientSelfLender.objects.all()
        serializer = ClientSelfLenderSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, self_lender_id=None, format=None):
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = ClientSelfLenderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, self_lender_id=None, format=None):
        if self_lender_id is None:
            pk = request.data["self_lender_id"]
        else:
            pk = self_lender_id
        data = ClientSelfLender.objects.get(pk=pk)
        request.data["recorded_on"] = data.recorded_on = datetime.datetime.now().isoformat()
        serializer = ClientSelfLenderSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
