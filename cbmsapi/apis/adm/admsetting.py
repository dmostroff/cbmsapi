
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
import datetime

from django.db.utils import IntegrityError, DatabaseError, DataError

from cbmsapi.models import AdmSetting
from cbmsapi.serializers import AdmSettingSerializer

class AdmSettingView(APIView):
    """
    List all AdmSetting with summary information.
    """

    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,)

    def get(self, request, adm_setting_id=None, format=None):
        try:
            if adm_setting_id is None:
                data = AdmSetting.objects.all()
                serializer = AdmSettingSerializer(data, many=True)
            else:
                data = AdmSetting.objects.get(pk=adm_setting_id)
                serializer = AdmSettingSerializer(data, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AdmSetting.DoesNotExist as e1:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e2:
            return Response({'rc': -1, 'msg': str(e2), 'data': adm_setting_id} , status=status.HTTP_400_BAD_REQUEST)
        return Response({'rc': -1, 'msg': 'Error'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, adm_setting_id=None, format=None):
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = AdmSettingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, adm_setting_id=None, format=None):
        if adm_setting_id is None:
            pk = request.data["adm_setting_id"]
        else:
            pk = adm_setting_id
        data = AdmSetting.objects.get(pk=pk)
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = AdmSettingSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, adm_setting_id=None, format=None):
    #     try:
    #         instance = self.get_object(adm_setting_id)
    #         instance.delete()
    #     except Exception as e:
    #         print( repr(e))
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response(status=status.HTTP_204_NO_CONTENT

class AdmSettingPrefixView(APIView):
    """
    List all AdmSetting with summary information.
    """

    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,)

    def get(self, request, prefix=None, keyname=None, format=None):
        try:
            if prefix is None and keyname is None:
                data = AdmSetting.objects.all()
                serializer = AdmSettingSerializer(data, many=True)
            elif keyname is None:
                data = AdmSetting.objects.filter(prefix=prefix)
                serializer = AdmSettingSerializer(data, many=True)
            else:
                data = AdmSetting.objects.get(prefix=prefix, keyname=keyname)
                serializer = AdmSettingSerializer(data, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AdmSetting.DoesNotExist as e1:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e2:
            return Response({'rc': -1, 'msg': str(e2), 'data': {'prefix': prefix, 'keyname': keyname}}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'rc': -1, 'msg': 'Error'}, status=status.HTTP_400_BAD_REQUEST)


class AdmSettingGetPrefixView(APIView):
    """
    List all AdmSetting with summary information.
    """

    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,)

    def get(self, request, format=None):
        try:
            data = AdmSetting.objects.order_by('prefix').values('prefix').distinct()
            res = list(data)
            retval = [v['prefix'] for v in res ]
            return Response(retval, status=status.HTTP_200_OK)
        except Exception as e2:
            return Response({'rc': -1, 'msg': str(e2), 'data': None}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'rc': -1, 'msg': 'Error'}, status=status.HTTP_400_BAD_REQUEST)

