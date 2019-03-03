
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from cbmsapi.models import ClientBankAccount
from cbmsapi.serializers import ClientBankAccountSerializer

class ClientBankAccountView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    
    queryset = ClientBankAccount.objects.all()

    def get(self, request, format=None):
        data = ClientBankAccount.objects.all()
        serializer = ClientBankAccountSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, bank_account_id=None, format=None):
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = ClientBankAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, bank_account_id=None, format=None):
        if cc_company_id is None:
            pk = request.data["bank_account_id"]
        else:
            pk = cc_company_id
        data = ClientBankAccount.objects.get(pk=pk)
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = ClientBankAccountSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
