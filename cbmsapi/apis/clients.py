from rest_framework import permissions
from rest_framework_simplejwt import authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from django.db.utils import IntegrityError, DatabaseError, DataError
# from psycopg2 import IntegrityError, DatabaseError, DataError

from cbmsapi.models import ClientPerson, ClientBankAccount, ClientCcAccount, ClientCreditline, ClientSetting
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
        if client_id is None:
            data = ClientPerson.objects.all()
        else:
            data = ClientPerson.objects.filter(client_id = client_id)
        serializer = ClientPersonSummarySerializer(data, many=True)
        return Response(serializer.data)

class ClientPersonView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,)

    # queryset = ClientPerson.objects.all()

    def get(self, request, client_id=None, format=None):
        if client_id is None:
            data = ClientPerson.objects.all()
        else:
            data = ClientPerson.objects.filter(client_id = client_id)
        serializer = ClientPersonFullSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClientPersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
