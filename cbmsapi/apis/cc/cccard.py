
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
import datetime

from django.db.utils import IntegrityError, DatabaseError, DataError

from cbmsapi.models import CcCard
from cbmsapi.serializers import CcCardSerializer

class CcCardView(APIView):
    """
    List all CcCard with summary information.
    """

    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,)

    def get(self, request, cc_card_id=None, format=None):
        try:
            if cc_card_id is None:
                data = CcCard.objects.all()
                serializer = CcCardSerializer(data, many=True)
            else:
                data = CcCard.objects.get(pk=cc_card_id)
                serializer = CcCardSerializer(data, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CcCard.DoesNotExist as e1:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e2:
            return Response({'rc': -1, 'msg': str(e2), 'data': cc_card_id} , status=status.HTTP_400_BAD_REQUEST)
        return Response({'rc': -1, 'msg': 'Error'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, cc_card_id=None, format=None):
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = CcCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, cc_card_id=None, format=None):
        if cc_card_id is None:
            pk = request.data["cc_card_id"]
        else:
            pk = cc_card_id
        data = CcCard.objects.get(pk=pk)
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = CcCardSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, cc_card_id=None, format=None):
    #     try:
    #         instance = self.get_object(cc_card_id)
    #         instance.delete()
    #     except Exception as e:
    #         print( repr(e))
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response(status=status.HTTP_204_NO_CONTENT
