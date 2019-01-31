import sys
from django.http import JsonResponse
from jsonrpc.backend.django import api
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt import serializers as jwt_serializers
from cbmsapi.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

@api.dispatcher.add_method
def login(request, *args, **kwargs):
    retval = {'rc': 0, 'msg': 'OK', 'data': None}
    tokenSerializer = jwt_serializers.TokenObtainPairSerializer()
    try:
        tokenPair = tokenSerializer.validate(kwargs)
    except ValidationError:
        retval['rc'] = -1
        retval['msg'] = 'Invalid user/password'
        retval['data'] = kwargs
        return retval
    except:
        print("Oops!",sys.exc_info()[0],"occured.")
        retval['rc'] = -1
        retval['msg'] = sys.exc_info()[0]
        retval['data'] = sys.exc_info()[1]
        return retval
    user = tokenSerializer.user
    serializer = UserSerializer
    data = serializer(user, many=False).data
    if 'password' in data:
        del data['password']
    data['token'] = tokenPair
    retval['data'] = data
    return retval