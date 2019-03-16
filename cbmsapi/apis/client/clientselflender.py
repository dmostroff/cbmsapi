
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
import datetime

from django.db.utils import IntegrityError, DatabaseError, DataError

from cbmsapi.models import ClientSelfLender
from cbmsapi.serializers import ClientSelfLenderSerializer

class ClientSelfLenderView(APIView):
    """
    List all ClientSelfLender with summary information.
    """

    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,)

    def get(self, request, self_lender_id=None, format=None):
        try:
            if client_id is None:
                data = ClientSelfLender.objects.all()
                serializer = ClientSelfLenderSerializer(data, many=True)
            else:
                data = ClientSelfLender.objects.get(pk=self_lender_id)
                serializer = ClientSelfLenderSerializer(data, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ClientSelfLender.DoesNotExist as e1:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e2:
            return Response({'rc': -1, 'msg': str(e2), 'data': self_lender_id} , status=status.HTTP_400_BAD_REQUEST)
        return Response({'rc': -1, 'msg': 'Error'}, status=status.HTTP_400_BAD_REQUEST)

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
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = ClientSelfLenderSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, self_lender_id=None, format=None):
    #     try:
    #         instance = self.get_object(self_lender_id)
    #         instance.delete()
    #     except Exception as e:
    #         print( repr(e))
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response(status=status.HTTP_204_NO_CONTENT
