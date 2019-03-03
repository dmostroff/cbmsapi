from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
import datetime

from cbmsapi.models import CcCompany
from cbmsapi.serializers import CcCompanySerializer
from rest_framework import mixins
from rest_framework import generics

class CcCompanyView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    
    queryset = CcCompany.objects.all()

    def get(self, request, format=None):
        data = CcCompany.objects.all()
        serializer = CcCompanySerializer(data, many=True)
        return Response(serializer.data)

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

class CcCompanyDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = CcCompany.objects.all()
    serializer_class = CcCompanySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)