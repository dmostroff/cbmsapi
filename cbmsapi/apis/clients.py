from rest_framework import permissions
from rest_framework_simplejwt import authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
import datetime

from django.db.utils import IntegrityError, DatabaseError, DataError
# from psycopg2 import NotFound

from cbmsapi.models import ClientPerson
from cbmsapi.serializers import ClientPersonSerializer
from cbmsapi.serializers import ClientPersonSummarySerializer
from cbmsapi.serializers import ClientPersonFullSerializer

class ClientPersonListView(APIView):
    """
    List all clients with summary information.
    """
    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,)

    # queryset = ClientPerson.objects.all()

    def get(self, request, client_id=None, format=None):
        try:
            if client_id is None:
                data = ClientPerson.objects.all()
            else:
                data = ClientPerson.objects.filter(client_id = client_id)
            serializer = ClientPersonSummarySerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ClientPerson.NotFound as e:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        return Response({'rc': -1, 'msg': 'Error'}, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, client_id=None, format=None):
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = ClientPersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, client_id=None, format=None):
        if client_id is None:
            pk = request.data["client_id"]
        else:
            pk = client_id
        data = ClientPerson.objects.get(pk=pk)
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = ClientPersonSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientPersonView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,)

    # queryset = ClientPerson.objects.all()

    def get(self, request, client_id=None, format=None):
        try:
            if client_id is None:
                data = ClientPerson.objects.all()
                serializer = ClientPersonFullSerializer(data, many=True)
            else:
                data = ClientPerson.objects.get(pk=client_id)
                serializer = ClientPersonFullSerializer(data, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ClientPerson.DoesNotExist as e1:
            return Response( { 'rc': -1, 'msg': 'Not Found', 'data': client_id}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response( { 'rc': -1, 'msg': str(e), 'data': client_id}, status=status.HTTP_404_NOT_FOUND)


    def post(self, request, format=None):
        serializer = ClientPersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

