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
from cbmsapi.serializers import CcCardViewSet
from cbmsapi.serializers import CcCompanyViewSet

from cbmsapi.serializers import ClientSummaryViewSet
from cbmsapi.serializers import ClientBankAccountViewSet
from cbmsapi.serializers import ClientCcAccountViewSet
from cbmsapi.serializers import ClientCcAccountCardNameViewSet
from cbmsapi.serializers import ClientCreditlineHistoryViewSet
from cbmsapi.serializers import ClientChargesViewSet
from cbmsapi.serializers import ClientCcTransactionViewSet
from cbmsapi.serializers import ClientCcBalanceTransferViewSet
from cbmsapi.serializers import ClientCcPointsViewSet
from cbmsapi.serializers import ClientSelfLenderViewSet
from cbmsapi.serializers import ClientSettingViewSet

from cbmsapi.apis import login
from cbmsapi.apis import cccompany
from cbmsapi.apis import cccard
from cbmsapi.apis import clients
from cbmsapi.apis import clientbankaccount
from cbmsapi.apis import clientccaccount
from cbmsapi.apis import clientcreditlinehistory
from cbmsapi.apis import clientcharges
from cbmsapi.apis import clientccbalancetransfer
from cbmsapi.apis import clientccpoints
from cbmsapi.apis import clientselflender
from cbmsapi.apis import clientsetting

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
router.register('cccard', CcCardViewSet)
router.register('cccompany', CcCompanyViewSet)
router.register('client_ccaccount', ClientCcAccountViewSet)
router.register('ccaccount/name', ClientCcAccountCardNameViewSet)
router.register('clientsummary', ClientSummaryViewSet)
router.register('cctransaction', ClientCcTransactionViewSet)
router.register('ccpoints', ClientCcPointsViewSet)
router.register('clientsettings', ClientSettingViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('hello/', views.hello),
    path('help/', views.help),
    re_path('pingtest/(?P<mystring>.+)?/?$', views.pingtest),
    path('login/', login.LoginView.as_view(), name="login"),
    path('api/jsonrpc/', include(api.urls), name='jsonrpc'),

    # client
    re_path( 'client/(?P<client_id>[0-9]+)?/?$', clients.ClientPersonView.as_view(), name='clientlist'),
    re_path( 'client/bankaccount/(?P<bank_account_id>[1-9][0-9]*)?/?$', clientbankaccount.ClientBankAccountView.as_view()),
    re_path( 'client/ccaccount/(?P<cc_account_id>[1-9][0-9]*)?/?$', clientccaccount.ClientCcAccountView.as_view()),
    re_path( 'client/cc/account/(?P<client_id>[0-9]+)?/?(?P<cc_account_id>[0-9]+)?/?$', clientccaccount.ClientCcAccountFullView.as_view()),
    re_path( 'client/creditline/(?P<creditline_id>[1-9][0-9]*)?/?$', clientcreditlinehistory.ClientCreditlineHistoryView.as_view()),
    re_path( 'client/cc/balance/(?P<bal_id>[1-9][0-9]*)?/?$', clientccbalancetransfer.ClientCcBalanceTransferView.as_view()),
    re_path( 'client/setting/(?P<client_id>[1-9][0-9]*)?/?$', clientsetting.ClientSettingView.as_view()),
    # cc cards
    re_path( 'company/(?P<cc_company_id>[1-9][0-9]*)?/?$', cccompany.CcCompanyView.as_view(), name="cccompany"),
    re_path( 'cccard/(?P<cc_card_id>[1-9][0-9]*)?/?$', cccard.CcCardView.as_view(), name="cccardlist"),
    # token
    path( 'token/pair/', jwt_views.token_obtain_pair, name='token_obtain_pair'),
]
