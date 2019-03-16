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
from cbmsapi.serializers import AdmSettingViewSet
from cbmsapi.serializers import CcCardViewSet
from cbmsapi.serializers import CcCompanyViewSet
from cbmsapi.serializers import CcTransactionViewSet
from cbmsapi.serializers import ClientAddressViewSet
from cbmsapi.serializers import ClientBankAccountViewSet
from cbmsapi.serializers import ClientCcAccountViewSet
from cbmsapi.serializers import ClientCcActionViewSet
from cbmsapi.serializers import ClientCcBalanceTransferViewSet
from cbmsapi.serializers import ClientCcHistoryViewSet
from cbmsapi.serializers import ClientCcPointsViewSet
from cbmsapi.serializers import ClientCcTransactionViewSet
from cbmsapi.serializers import ClientChargesViewSet
from cbmsapi.serializers import ClientCreditlineHistoryViewSet
from cbmsapi.serializers import ClientPersonViewSet
from cbmsapi.serializers import ClientSelfLenderViewSet
from cbmsapi.serializers import ClientSettingViewSet

from cbmsapi.serializers import ClientCcAccountCardNameViewSet
from cbmsapi.serializers import ClientSummaryViewSet

from cbmsapi.apis import login

from cbmsapi.apis.adm import admsetting
from cbmsapi.apis.cc import cccard
from cbmsapi.apis.cc import cccompany
from cbmsapi.apis.cc import cctransaction
from cbmsapi.apis.client import clientaddress
from cbmsapi.apis.client import clientbankaccount
from cbmsapi.apis.client import clientccaccount
from cbmsapi.apis.client import clientccaction
from cbmsapi.apis.client import clientccbalancetransfer
from cbmsapi.apis.client import clientcchistory
from cbmsapi.apis.client import clientccpoints
from cbmsapi.apis.client import clientcctransaction
from cbmsapi.apis.client import clientcharges
from cbmsapi.apis.client import clientcreditlinehistory
from cbmsapi.apis.client import clientperson
from cbmsapi.apis.client import clientselflender
from cbmsapi.apis.client import clientsetting

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

    re_path( 'adm/setting/(?P<adm_setting_id>[1-9][0-9]*)?/?$', admsetting.AdmSettingView.as_view()),
    # Cc
    re_path( 'cc/card/(?P<cc_card_id>[1-9][0-9]*)?/?$', cccard.CcCardView.as_view()),
    re_path( 'cc/company/(?P<cc_company_id>[1-9][0-9]*)?/?$', cccompany.CcCompanyView.as_view()),
    re_path( 'cc/transaction/(?P<cctrans_id>[1-9][0-9]*)?/?$', cctransaction.CcTransactionView.as_view()),
    # Client
    re_path( 'client/address/(?P<address_id>[1-9][0-9]*)?/?$', clientaddress.ClientAddressView.as_view()),
    re_path( 'client/bank/account/(?P<bank_account_id>[1-9][0-9]*)?/?$', clientbankaccount.ClientBankAccountView.as_view()),
    re_path( 'client/cc/account/(?P<cc_account_id>[1-9][0-9]*)?/?$', clientccaccount.ClientCcAccountView.as_view()),
    re_path( 'client/cc/action/(?P<cc_action_id>[1-9][0-9]*)?/?$', clientccaction.ClientCcActionView.as_view()),
    re_path( 'client/cc/balance/transfer/(?P<bal_id>[1-9][0-9]*)?/?$', clientccbalancetransfer.ClientCcBalanceTransferView.as_view()),
    re_path( 'client/cc/history/(?P<cc_hist_id>[1-9][0-9]*)?/?$', clientcchistory.ClientCcHistoryView.as_view()),
    re_path( 'client/cc/points/(?P<cc_points_id>[1-9][0-9]*)?/?$', clientccpoints.ClientCcPointsView.as_view()),
    re_path( 'client/cc/transaction/(?P<cc_trans_id>[1-9][0-9]*)?/?$', clientcctransaction.ClientCcTransactionView.as_view()),
    re_path( 'client/charges/(?P<charge_id>[1-9][0-9]*)?/?$', clientcharges.ClientChargesView.as_view()),
    re_path( 'client/creditline/history/(?P<creditline_id>[1-9][0-9]*)?/?$', clientcreditlinehistory.ClientCreditlineHistoryView.as_view()),
    re_path( 'client/person/(?P<client_id>[1-9][0-9]*)?/?$', clientperson.ClientPersonView.as_view()),
    re_path( 'client/self/lender/(?P<self_lender_id>[1-9][0-9]*)?/?$', clientselflender.ClientSelfLenderView.as_view()),
    re_path( 'client/setting/(?P<client_setting_id>[1-9][0-9]*)?/?$', clientsetting.ClientSettingView.as_view()),
    re_path( 'client/(?P<client_id>[1-9][0-9]*)/setting/(?P<client_setting_id>[1-9][0-9]*)?/?$', clientsetting.ClientSettingView.as_view()),
    # token
    path( 'token/pair/', jwt_views.token_obtain_pair, name='token_obtain_pair'),
]
