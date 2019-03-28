
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
import datetime

from django.db.utils import IntegrityError, DatabaseError, DataError

from cbmsapi.models import ClientCcAccount
from cbmsapi.serializers import ClientCcAccountSerializer, ClientCcAccountEditSerializer

class ClientCcAccountView(APIView):
    """
    List all ClientCcAccount with summary information.
    """

    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,)

    def get(self, request, cc_account_id=None, format=None):
        try:
            if cc_account_id is None:
                data = ClientCcAccount.objects.all()
                serializer = ClientCcAccountSerializer(data, many=True)
            else:
                data = ClientCcAccount.objects.get(pk=cc_account_id)
                serializer = ClientCcAccountSerializer(data, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ClientCcAccount.DoesNotExist as e1:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e2:
            return Response({'rc': -1, 'msg': str(e2), 'data': cc_account_id} , status=status.HTTP_400_BAD_REQUEST)
        return Response({'rc': -1, 'msg': 'Error'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, cc_account_id=None, format=None):
        request.data["recorded_on"] = datetime.datetime.now().utcnow()
        if 'cc_account_info' not in request.data or request.data['cc_account_info'] is None:
            request.data['cc_account_info'] = "{}"
        # if request.data['client']['client_info'] is None:
        #     request.data['client']['client_info'] = "{}"

        clientCcAccount = ClientCcAccount(
            cc_account_id = request.data['cc_account_id'],
            client_id = request.data['client']['client_id'],
            cc_card_id = request.data['cc_card']['cc_card_id'],
            name = request.data['name'],
            account = request.data['account'],
            account_info = request.data['account_info'],
            cc_login = request.data['cc_login'],
            cc_pwd = request.data['cc_pwd'],
            cc_status = request.data['cc_status'],
            annual_fee_waived = 'Y' if request.data['annual_fee_waived'] else 'N',
            credit_limit = request.data['credit_limit'],
            # addtional_card = request.data['additional_card'],
            notes = request.data['notes'],
            # ccaccount_info = request.data['cc_account_info'],
            recorded_on = request.data['recorded_on']
            )
        try:
            clientCcAccount.save()
            serializer = ClientCcAccountSerializer(clientCcAccount)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(str(e))
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # if 'client_id' not in request.data:
        #     request.data['client_id'] = request.data['client']['client_id']
        # if 'cc_card_id' not in request.data:
        #     request.data['cc_card_id'] = request.data['cc_card']['cc_card_id']
        # serializer = ClientCcAccountSerializer(data=request.data)
        # if serializer.is_valid():
        #     try:
        #         if 'client_id' not in serializer.data or serializer.data['client_id'] is None:
        #             serializer.data['client_id'] = request.data['client']['client_id']
        #         if 'cc_card_id' not in serializer.data or serializer.data['cc_card_id'] is None:
        #             serializer.data['cc_card_id'] = request.data['cc_card']['cc_card_id']
        #         serializer.save()
        #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        #     except Exception as e:
        #         print(str(e))
        #         return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

    # def delete(self, request, cc_account_id=None, format=None):
    #     try:
    #         instance = self.get_object(cc_account_id)
    #         instance.delete()
    #     except Exception as e:
    #         print( repr(e))
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response(status=status.HTTP_204_NO_CONTENT
