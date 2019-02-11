
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from cbmsapi.models import CcCard
from cbmsapi.serializers import CcCardSerializer
from rest_framework import mixins
from rest_framework import generics


class CcCardList(generics.ListCreateAPIView):
    queryset = CcCard.objects.all()
    serializer_class = CcCardSerializer


class CcCardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CcCard.objects.all()
    serializer_class = CcCardSerializer


# class CcCardList(mixins.ListModelMixin
#     , mixins.CreateModelMixin
#     , generics.GenericAPIView):
#     """
#     List all snippets, or create a new snippet.
#     """
    
#     queryset = CcCard.objects.all()
#     serializer_class = CcCardSerializer

#     def get(self, request, *args. **kwargs):
#         return self.list( request, *args. **kwargs)

#     def post(self, request, *args. **kwargs):
#         return self.post( request, *args. **kwargs)

# class CcCardDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = CcCard.objects.all()
#     serializer_class = CcCardSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)