from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
import datetime

from django.db.utils import IntegrityError, DatabaseError, DataError

from cbmsapi.models import ClientPerson
from cbmsapi.serializers import ClientSummarySerializer

class ClientSummaryView(APIView):
    def get(self, request, client_id=None, format=None):
        try:
            if client_id is None:
                data = ClientPerson.objects.all()
                serializer = ClientSummarySerializer(data, many=True)
            else:
                data = ClientPerson.objects.get(pk=client_id)
                serializer = ClientSummarySerializer(data, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ClientPerson.DoesNotExist as e1:
            return Response( { 'rc': -1, 'msg': 'Not Found', 'data': client_id}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response( { 'rc': -1, 'msg': str(e), 'data': client_id}, status=status.HTTP_404_NOT_FOUND)
