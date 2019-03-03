
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
import datetime

from cbmsapi.models import ClientCcBalanceTransfer
from cbmsapi.serializers import ClientCcBalanceTransferSerializer

class ClientCcBalanceTransferView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    
    queryset = ClientCcBalanceTransfer.objects.all()

    def get(self, request, format=None):
        data = ClientCcBalanceTransfer.objects.all()
        serializer = ClientCcBalanceTransferSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, bal_id=None, format=None):
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = ClientCcBalanceTransferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, bal_id=None, format=None):
        if bal_id is None:
            pk = request.data["bal_id"]
        else:
            pk = bal_id
        data = ClientCcBalanceTransfer.objects.get(pk=pk)
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = ClientCcBalanceTransferSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
