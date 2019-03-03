from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from cbmsapi.models import ClientCreditlineHistory
from cbmsapi.serializers import ClientCreditlineHistorySerializer

class ClientCreditlineHistoryView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,)

    # queryset = ClientPerson.objects.all()

    def get(self, request, client_id=None, format=None):
        if client_id is None:
            data = ClientCreditlineHistory.objects.all()
        else:
            data = ClientCreditlineHistory.objects.filter(client_id = client_id)
        serializer = ClientCreditLineHistorySerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, creditline_id=None, format=None):
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = ClientCreditlineHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, creditline_id=None, format=None):
        if client_id is None:
            pk = request.data["creditline_id"]
        else:
            pk = creditline_id
        data = ClientCreditlineHistory.objects.get(pk=pk)
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = ClientCreditlineHistorySerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


