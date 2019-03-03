
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from cbmsapi.models import CcCard
from cbmsapi.serializers import CcCardSerializer
from rest_framework import mixins
from rest_framework import generics


class CcCardView( APIView):
    def get(self, request, format=None):
        data = CcCard.objects.all()
        serializer = CcCardSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, cc_card_id=None, format=None):
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = CcCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, cc_card_id=None, format=None):
        if cc_card_id is None:
            pk = request.data["cc_card_id"]
        else:
            pk = cc_card_id
        data = CcCard.objects.get(pk=pk)
        request.data["recorded_on"] = datetime.datetime.now().isoformat()
        serializer = CcCardSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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