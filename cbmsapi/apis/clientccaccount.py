from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
import datetime

from cbmsapi.models import ClientCcAccount
from cbmsapi.serializers import ClientCcAccountSerializer
from cbmsapi.serializers import ClientCcAccountFullSerializer
from cbmsapi.serializers import ClientCcAccountSummarySerializer

class ClientCcAccountView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    
    queryset = ClientCcAccount.objects.all()

    def get(self, request, cc_account_id=None, format=None):
        if cc_account_id is None:
            data = ClientCcAccount.objects.all()
            serializer = ClientCcAccountSerializer(data, many=True)
        else:
            data = ClientCcAccount.objects.get(pk=cc_account_id)
            serializer = ClientCcAccountSerializer(data, many=False)
        return Response(serializer.data)

    def post(self, request, cc_account_id=None, format=None):
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = ClientCcAccountSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, cc_account_id=None, format=None):
        if cc_account_id is None:
            pk = request.data["cc_account_id"]
        else:
            pk = cc_account_id
        data = ClientCcAccount.objects.get(pk=pk)
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = ClientCcAccountSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientCcAccountCardNameView(APIView):
    """
    Full listing of Credit Card Client Account
    """

    queryset = ClientCcAccount.objects.all()

    def get(self, request, ):
        queryset = ClientCcAccount.objects.all()
        serializer = ClientCcAccountFullSerializer(queryset, many=True)
        return Response(serializer.data)

class ClientCcAccountFullView(APIView):
    """
    Full listing of Credit Card Client Account
    """

    queryset = ClientCcAccount.objects.all()

    def get(self, request, client_id=None, cc_account_id=None):
        if client_id is None:
            queryset = ClientCcAccount.objects.all()
        elif cc_account_id is None:
            queryset = ClientCcAccount.objects.filter(client_id=client_id)
        else:
            queryset = ClientCcAccount.objects.filter(client_id=client_id, cc_account_id=cc_account_id)
        serializer = ClientCcAccountFullSerializer(queryset, many=True)
        return Response(serializer.data)

class ClientCcAccountSummaryView(APIView):
    """
    Summary listing of Credit Card Client Account
    """

    queryset = ClientCcAccount.objects.all()

    def get(self, request, client_id=None, cc_account_id=None):
        if client_id is None:
            queryset = ClientCcAccount.objects.all()
        elif cc_account_id is None:
            queryset = ClientCcAccount.objects.filter(client_id=client_id)
        else:
            queryset = ClientCcAccount.objects.filter(client_id=client_id, cc_account_id=cc_account_id)
        serializer = ClientCcAccountSummarySerializer(queryset, many=True)
        return Response(serializer.data)
