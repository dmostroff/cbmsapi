
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
import datetime

from django.db.utils import IntegrityError, DatabaseError, DataError

from cbmsapi.models import ClientPerson, ClientCreditlineHistory
from cbmsapi.serializers import ClientPersonSerializer, ClientCreditlineHistorySerializer, ClientCreditlineHistoryEditSerializer

class ClientCreditlineHistoryView(APIView):
    """
    List all ClientCreditlineHistory with summary information.
    """

    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,)

    def get(self, request, creditline_id=None, format=None):
        try:
            if creditline_id is None:
                data = ClientCreditlineHistory.objects.all()
                serializer = ClientCreditlineHistorySerializer(data, many=True)
            else:
                data = ClientCreditlineHistory.objects.get(pk=creditline_id)
                serializer = ClientCreditlineHistoryEditSerializer(data, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ClientCreditlineHistory.DoesNotExist as e1:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e2:
            return Response({'rc': -1, 'msg': str(e2), 'data': creditline_id} , status=status.HTTP_400_BAD_REQUEST)
        return Response({'rc': -1, 'msg': 'Error'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, creditline_id=None, format=None):
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = ClientCreditlineHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, creditline_id=None, format=None):
        if creditline_id is None:
            pk = request.data["creditline_id"]
        else:
            pk = creditline_id
        data = ClientCreditlineHistory.objects.get(pk=pk)
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = ClientCreditlineHistorySerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, creditline_id=None):
        if creditline_id is None:
            return Response(status=status.HTTP_204_NO_CONTENT) 
        try:
            instance = ClientCreditlineHistory.objects.get(pk=creditline_id)
            serializer = ClientCreditlineHistorySerializer(instance, many=False)
            instance.delete()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        except Exception as e:
            print( repr(e))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ClientCreditlineHistoryByClientView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,)

    # queryset = ClientPerson.objects.all()

    def get(self, request, client_id=None, format=None):
        if client_id is not None:
            data = ClientCreditlineHistory.objects.filter(client_id=client_id).order_by('-credit_line_date')
            serializer = ClientCreditlineHistorySerializer(data, many=True)
            clientPerson = ClientPerson.objects.get(pk=client_id)
            cpSerializer = ClientPersonSerializer(clientPerson, many=False)
            return Response( {'client': cpSerializer.data, 'creditline_history': serializer.data})
        else:
            data = ClientCreditlineHistory.objects.all().order_by('-credit_line_date')
            serializer = ClientCreditlineHistorySerializer(data, many=True)
        return Response(serializer.data)
