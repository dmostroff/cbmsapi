import sys
from django.http import JsonResponse, HttpResponse
from jsonrpc.backend.django import api
from jsonrpc import JSONRPCResponseManager
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt import serializers as jwt_serializers
from cbmsapi.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


# restframework version of login
class LoginView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        retval = {'rc': 0, 'msg': 'OK', 'data': None}
        tokenSerializer = jwt_serializers.TokenObtainPairSerializer()
        try:
            tokenPair = tokenSerializer.validate(request.data)
            # tokenPair = tokenSerializer.validate(kwargs)
        except ValidationError:
            retval = {'rc': -1, 'msg': 'Invalid user/password', 'data': request.data}
            return JsonResponse(data=retval, status=status.HTTP_401_UNAUTHORIZED)
        except KeyError:
            retval = {'rc': -1, 'msg': 'Invalid parameter', 'data': repr(sys.exc_info()[1])}
            return JsonResponse(data=retval, status=status.HTTP_401_UNAUTHORIZED)
        except:
            retval = {'rc': -1, 'msg': repr(sys.exc_info()[0]), 'data': repr(sys.exc_info()[1])}
            print("Oops!",sys.exc_info()[0],"occured.")
            return JsonResponse(data=retval, status=status.HTTP_403_FORBIDDEN)
            # return retval
        user = tokenSerializer.user
        serializer = UserSerializer
        data = serializer(user, many=False).data
        if 'password' in data:
            del data['password']
        data['token'] = tokenPair
        retval['data'] = data
        return JsonResponse(data=retval, status=status.HTTP_200_OK)

## json rpc version
@api.dispatcher.add_method
def login(request, *args, **kwargs):
    retval = {'rc': 0, 'msg': 'OK', 'data': None}
    tokenSerializer = jwt_serializers.TokenObtainPairSerializer()
    try:
        tokenPair = tokenSerializer.validate(kwargs)
    except ValidationError:
        retval = {'rc': -1, 'msg': 'Invalid user/password', 'data': request.data}
        return retval

    except:
        print("Oops!",sys.exc_info()[0],"occured.")
        retval = {'rc': -1, 'msg': repr(sys.exc_info()[0]), 'data': repr(sys.exc_info()[1])}
        return retval

    user = tokenSerializer.user
    serializer = UserSerializer
    data = serializer(user, many=False).data
    if 'password' in data:
        del data['password']
    data['token'] = tokenPair
    retval['data'] = data
    return retval