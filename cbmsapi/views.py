from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from jsonrpc.backend.django import api

import datetime

@api.dispatcher.add_method
def ping(request, *args, **kwargs):
    return args, kwargs

# @api_view(['GET'])
def hello(request):
	now = datetime.datetime.now()
	contents='<html><head><meta http-equiv="refresh" content="30" /></head><body><h2>Welcome to {}</h2><h4>It is now {}.</h4></body></html>'
	return HttpResponse(contents.format('cbmsapi', now))

def help(request):
	return HttpResponse('<html><body>Help</body></html>')
