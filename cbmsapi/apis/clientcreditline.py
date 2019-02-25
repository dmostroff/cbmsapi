from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from cbmsapi.models import ClientCreditline
from cbmsapi.serializers import ClientCreditlineSerializer

class ClientCreditlineView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.JWTAuthentication,)

    # queryset = ClientPerson.objects.all()

    def get(self, request, client_id=None, format=None):
        if client_id is None:
            data = ClientCreditline.objects.all()
        else:
            data = ClientCreditline.objects.filter(client_id = client_id)
        serializer = ClientCreditlineSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClientCreditlineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

