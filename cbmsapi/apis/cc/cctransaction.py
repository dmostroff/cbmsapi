
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
import datetime

from django.db.utils import IntegrityError, DatabaseError, DataError

from cbmsapi.models import CcTransaction
from cbmsapi.serializers import CcTransactionSerializer

class CcTransactionView(APIView):
    """
    List all CcTransaction with summary information.
    """

    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,)

    def get(self, request, cctrans_id=None, format=None):
        try:
            if cctrans_id is None:
                data = CcTransaction.objects.all()
                serializer = CcTransactionSerializer(data, many=True)
            else:
                data = CcTransaction.objects.get(pk=cctrans_id)
                serializer = CcTransactionSerializer(data, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CcTransaction.DoesNotExist as e1:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e2:
            return Response({'rc': -1, 'msg': str(e2), 'data': cctrans_id} , status=status.HTTP_400_BAD_REQUEST)
        return Response({'rc': -1, 'msg': 'Error'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, cctrans_id=None, format=None):
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = CcTransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, cctrans_id=None, format=None):
        if cctrans_id is None:
            pk = request.data["cctrans_id"]
        else:
            pk = cctrans_id
        data = CcTransaction.objects.get(pk=pk)
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = CcTransactionSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, cctrans_id=None, format=None):
    #     try:
    #         instance = self.get_object(cctrans_id)
    #         instance.delete()
    #     except Exception as e:
    #         print( repr(e))
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response(status=status.HTTP_204_NO_CONTENT
