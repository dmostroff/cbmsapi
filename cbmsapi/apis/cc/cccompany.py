
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
import datetime

from django.db.utils import IntegrityError, DatabaseError, DataError

from cbmsapi.models import CcCompany
from cbmsapi.serializers import CcCompanySerializer

class CcCompanyView(APIView):
    """
    List all CcCompany with summary information.
    """

    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,)

    def get(self, request, cc_company_id=None, format=None):
        try:
            if cc_company_id is None:
                data = CcCompany.objects.all()
                serializer = CcCompanySerializer(data, many=True)
            else:
                data = CcCompany.objects.get(pk=cc_company_id)
                serializer = CcCompanySerializer(data, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CcCompany.DoesNotExist as e1:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e2:
            return Response({'rc': -1, 'msg': str(e2), 'data': cc_company_id} , status=status.HTTP_400_BAD_REQUEST)
        return Response({'rc': -1, 'msg': 'Error'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, cc_company_id=None, format=None):
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = CcCompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, cc_company_id=None, format=None):
        if cc_company_id is None:
            pk = request.data["cc_company_id"]
        else:
            pk = cc_company_id
        data = CcCompany.objects.get(pk=pk)
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = CcCompanySerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, cc_company_id=None, format=None):
    #     try:
    #         instance = self.get_object(cc_company_id)
    #         instance.delete()
    #     except Exception as e:
    #         print( repr(e))
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response(status=status.HTTP_204_NO_CONTENT
