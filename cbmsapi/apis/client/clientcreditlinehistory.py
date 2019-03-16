
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
import datetime

from django.db.utils import IntegrityError, DatabaseError, DataError

from cbmsapi.models import ClientCreditlineHistory
from cbmsapi.serializers import ClientCreditlineHistorySerializer

class ClientCreditlineHistoryView(APIView):
    """
    List all ClientCreditlineHistory with summary information.
    """

    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,)

    def get(self, request, creditline_id=None, format=None):
        try:
            if client_id is None:
                data = ClientCreditlineHistory.objects.all()
                serializer = ClientCreditlineHistorySerializer(data, many=True)
            else:
                data = ClientCreditlineHistory.objects.get(pk=creditline_id)
                serializer = ClientCreditlineHistorySerializer(data, many=False)
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

    # def delete(self, request, creditline_id=None, format=None):
    #     try:
    #         instance = self.get_object(creditline_id)
    #         instance.delete()
    #     except Exception as e:
    #         print( repr(e))
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response(status=status.HTTP_204_NO_CONTENT
