from rest_framework import permissions
from rest_framework_simplejwt import authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from django.db.utils import IntegrityError, DatabaseError, DataError
# from psycopg2 import IntegrityError, DatabaseError, DataError

from cbmsapi.models import ClientPerson, ClientBankAccount, ClientCcAccount, ClientSetting
from cbmsapi.serializers import ClientPersonSerializer
from cbmsapi.serializers import ClientBankAccountSerializer, ClientCcaccountSerializer, ClientSettingSerializer
from cbmsapi.serializers import ClientSettingSparseSerializer, ClientPersonFullSerializer

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

class ClientBankAccountView(APIView):
    """
    CRUD client bank accounts.
    """
    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,)

    # queryset = ClientPerson.objects.all()

    def get(self, request, client_id=None, format=None):
        if client_id is None:
            data = ClientBankAccount.objects.all()
        else:
            data = ClientBankAccount.objects.filter(client_id = client_id)
        serializer = ClientBankAccountSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClientBankAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

class ClientCCAccountView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,)

    # queryset = ClientPerson.objects.all()

    def get(self, request, client_id=None, format=None):
        if client_id is None:
            data = ClientCcAccount.objects.all()
        else:
            data = ClientCcAccount.objects.filter(client_id = client_id)
        serializer = ClientCcAccountSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClientCcaccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        


class ClientSettingView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,)

    # queryset = ClientPerson.objects.all()

    def get(self, request, client_id=None, format=None):
        if client_id is not None:
            data = ClientSetting.objects.filter(client_id=client_id)
        else:
            data = ClientSetting.objects.all()
        serializer = ClientSettingSparseSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        client = ClientPerson.objects.get(pk=request.data["client_id"])
        clientSetting = ClientSetting()
        clientSetting.client = client;
        clientSetting.prefix = request.data["prefix"];
        clientSetting.keyname = request.data["keyname"];
        clientSetting.keyvalue = request.data["keyvalue"];
        try:
            clientSetting.save();
            serializer = ClientSettingSerializer(clientSetting)
            return Response( {'rc': 0, 'msg': "OK", 'data': serializer.data}, status=status.HTTP_201_CREATED);

        except IntegrityError as e1:
            clientSetting1 = ClientSetting.objects.filter(client_id=request.data['client_id'], prefix=request.data['prefix'], keyname=request.data['keyname'])[0]
            if clientSetting1.keyvalue != request.data["keyvalue"]:
                clientSetting1.keyvalue = request.data["keyvalue"]
                clientSetting1.save()
                serializer = ClientSettingSerializer(clientSetting1)
                return Response( {'rc': 0, 'msg': "OK", 'data': serializer.data}, status=status.HTTP_200_OK);
            else:
                serializer = ClientSettingSerializer(clientSetting1)
                return Response( {'rc': -1, 'msg': str(e1), 'data': serializer.data}, status=status.HTTP_200_OK);
                
        except DataError as e3:
            return Response( {'rc': -1, 'msg': str(e3), 'data': request.data}, status=status.HTTP_400_BAD_REQUEST);
        except DatabaseError as e4:
            return Response( {'rc': -1, 'msg': str(e4), 'data': request.data}, status=status.HTTP_400_BAD_REQUEST);
        except Exception as e2:
            return Response( {'rc': -1, 'msg': str(e2), 'data': request.data}, status=status.HTTP_400_BAD_REQUEST);
            # clientSetting = ClientSetting.objects.get( client_id=request.data["client_id"])
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                        
        # serializer = ClientSettingSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
