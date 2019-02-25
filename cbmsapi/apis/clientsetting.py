
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from cbmsapi.models import ClientSetting
from cbmsapi.serializers import ClientSettingSerializer, ClientSettingSparseSerializer

class ClientSettingxView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    
    queryset = ClientSetting.objects.all()

    def get(self, request, format=None):
        data = ClientSetting.objects.all()
        serializer = ClientSettingSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClientSettingSerializer(data=request.data)
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
