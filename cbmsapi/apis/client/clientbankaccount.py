
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
import datetime

from django.db.utils import IntegrityError, DatabaseError, DataError

from cbmsapi.models import ClientPerson
from cbmsapi.serializers import ClientPersonSerializer
from cbmsapi.models import ClientBankAccount
from cbmsapi.serializers import ClientBankAccountSerializer

class ClientBankAccountView(APIView):
    """
    List all ClientBankAccount with summary information.
    """

    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,)

    def get(self, request, bank_account_id=None, format=None):
        try:
            if bank_account_id is None:
                data = ClientBankAccount.objects.all()
                serializer = ClientBankAccountSerializer(data, many=True)
            else:
                data = ClientBankAccount.objects.get(pk=bank_account_id)
                serializer = ClientBankAccountSerializer(data, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ClientBankAccount.DoesNotExist as e1:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e2:
            return Response({'rc': -1, 'msg': str(e2), 'data': bank_account_id} , status=status.HTTP_400_BAD_REQUEST)
        return Response({'rc': -1, 'msg': 'Error'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, bank_account_id=None, format=None):
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = ClientBankAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, bank_account_id=None, format=None):
        if bank_account_id is None:
            pk = request.data["bank_account_id"]
        else:
            pk = bank_account_id
        data = ClientBankAccount.objects.get(pk=pk)
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = ClientBankAccountSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, bank_account_id=None, format=None):
    #     try:
    #         instance = self.get_object(bank_account_id)
    #         instance.delete()
    #     except Exception as e:
    #         print( repr(e))
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response(status=status.HTTP_204_NO_CONTENT

class ClientBankAccountByClientView(APIView):
    """
    List all ClientBankAccount with summary information.
    """

    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,)

    def get(self, request, client_id, format=None):
        try:
            data = ClientBankAccount.objects.filter(client_id=client_id)
            serializer = ClientBankAccountSerializer(data, many=True)
            clientPerson = ClientPerson.objects.get(pk=client_id)
            cpSerializer = ClientPersonSerializer(clientPerson, many=False)
            return Response( {'client': cpSerializer.data, 'bankaccount': serializer.data})
        except ClientBankAccount.DoesNotExist as e1:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e2:
            return Response({'rc': -1, 'msg': str(e2), 'data': client_id} , status=status.HTTP_400_BAD_REQUEST)
        return Response({'rc': -1, 'msg': 'Error'}, status=status.HTTP_400_BAD_REQUEST)


    # def delete(self, request, client_id=None, format=None):
    #     try:
    #         instance = self.get_object(bank_account_id)
    #         instance.delete()
    #     except Exception as e:
    #         print( repr(e))
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response(status=status.HTTP_204_NO_CONTENT
