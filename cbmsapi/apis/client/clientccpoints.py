
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
import datetime

from django.db.utils import IntegrityError, DatabaseError, DataError

from cbmsapi.models import ClientCcPoints
from cbmsapi.serializers import ClientCcPointsSerializer

class ClientCcPointsView(APIView):
    """
    List all ClientCcPoints with summary information.
    """

    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,)

    def get(self, request, cc_points_id=None, format=None):
        try:
            if client_id is None:
                data = ClientCcPoints.objects.all()
                serializer = ClientCcPointsSerializer(data, many=True)
            else:
                data = ClientCcPoints.objects.get(pk=cc_points_id)
                serializer = ClientCcPointsSerializer(data, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ClientCcPoints.DoesNotExist as e1:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e2:
            return Response({'rc': -1, 'msg': str(e2), 'data': cc_points_id} , status=status.HTTP_400_BAD_REQUEST)
        return Response({'rc': -1, 'msg': 'Error'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, cc_points_id=None, format=None):
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = ClientCcPointsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, cc_points_id=None, format=None):
        if cc_points_id is None:
            pk = request.data["cc_points_id"]
        else:
            pk = cc_points_id
        data = ClientCcPoints.objects.get(pk=pk)
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = ClientCcPointsSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, cc_points_id=None, format=None):
    #     try:
    #         instance = self.get_object(cc_points_id)
    #         instance.delete()
    #     except Exception as e:
    #         print( repr(e))
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response(status=status.HTTP_204_NO_CONTENT
