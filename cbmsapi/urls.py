"""cbmsapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework_simplejwt import views as jwt_views
from jsonrpc.backend.django import api

from cbmsapi import views
from cbmsapi.serializers import CcCardViewSet, CcCompanyViewSet, ClientCcaccountViewSet, ClientSettingViewSet, ClientBankAccountViewSet
from cbmsapi.apis import clients, login, cccompany
from cbmsapi.apis import cccard

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')
# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register(r'cccard', CcCardViewSet)
router.register(r'cccompany', CcCompanyViewSet)
router.register(r'client_ccaccount', ClientCcaccountViewSet)

urlpatterns = [
    path('api', include(router.urls)),
    path('admin/', admin.site.urls),
    path('hello/', views.hello),
    path('help/', views.help),
    path('login/', login.LoginView.as_view(), name="login"),
    path('api/jsonrpc/', include(api.urls), name='jsonrpc'),
    re_path( 'client/(?P<client_id>[0-9]+)?/?$', clients.ClientPersonView.as_view(), name='clientlist'),
    path( 'client/bankaccount/', clients.ClientBankAccountView.as_view()),
    path( 'client/ccaccount/', clients.ClientCCAccountView.as_view()),
    path( 'client/setting/', clients.ClientSettingView.as_view()),
    path( 'client/setting/<client_id>/', clients.ClientSettingView.as_view()),
    # cc cards
    path( 'cccard/', cccard.CcCardList.as_view(), name="cccardlist"),
    path( 'token/pair/', jwt_views.token_obtain_pair, name='token_obtain_pair'),
]
