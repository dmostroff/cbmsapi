from rest_framework import serializers, viewsets

from django.contrib.auth.models import User
from cbmsapi.models import ClientPerson
from cbmsapi.models import CcCompany
from cbmsapi.models import CcCard
from cbmsapi.models import ClientCcAccount
from cbmsapi.models import ClientSetting
from cbmsapi.models import CcBaltransferinfo
from cbmsapi.models import ClientBankAccount
#--------------------------------
# User
#--------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#--------------------------------
# ClientPerson
#--------------------------------
class ClientPersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientPerson
        fields = ('client_id', 'last_name', 'first_name', 'middle_name', 'dob', 'gender', 'ssn', 'mmn', 'email', 'pwd', 'phone', 'phone_2', 'phone_cell', 'phone_fax', 'phone_official', 'client_info', 'recorded_on')


# ViewSets define the view behavior.
class ClientPersonViewSet(viewsets.ModelViewSet):
    queryset = ClientPerson.objects.all()
    serializer_class = ClientPersonSerializer


class CcBaltransferinfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CcBaltransferinfo
        fields = ('bal_id', 'client_id', 'ccaccount_id', 'due_date', 'total', 'credit_line', 'recorded_on')

# ViewSets define the view behavior.
class CcBaltransferinfoViewSet(viewsets.ModelViewSet):
    queryset = CcBaltransferinfo.objects.all()
    serializer_class = CcBaltransferinfoSerializer
class ClientPersonNameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientPerson
        fields = ('client_id', 'last_name', 'first_name', 'middle_name')        

class ClientPersonFullSerializer(serializers.ModelSerializer):
    # settings = ClientSetting.objects.filter(client_id = self.model.client_id)
    bankaccounts = serializers.SerializerMethodField('_get_client_bankaccounts')
    ccaccounts = serializers.SerializerMethodField('_get_client_ccaccounts')
    settings = serializers.SerializerMethodField('_get_client_settings')
    baltransfer = serializers.SerializerMethodField('_get_client_baltransfer')

    def _get_client_bankaccounts(self, obj):
        """
        Get client's bank accounts
        """
        try:
            clientBankAccount = ClientBankAccount.objects.filter(client_id=obj.client_id)
            accounts = ClientBankAccountSerializer(clientBankAccount, many=True)
            retval = accounts.data
        except:
            retval = ''
        return retval

    def _get_client_ccaccounts(self, obj):
        """
        Get client's credit card accounts
        """
        try:
            ClientCcAccount = ClientCcAccount.objects.filter(client_id=obj.client_id)
            accounts = ClientCcaccountSerializer(ClientCcAccount, many=True)
            retval = accounts.data
        except:
            retval = ''
        return retval


    def _get_client_settings(self, obj):
        """
        Get client settings
        """
        try:
            clientSetting = ClientSetting.objects.filter(client_id=obj.client_id)
            settings = ClientSettingSparseSerializer(clientSetting, many=True)
            retval = settings.data
        except:
            retval = ''
        return retval

    def _get_client_baltransfer(self, obj):
        """
        Get user role description
        """
        try:
            baltrans = CcBaltransferinfo.objects.filter(client_id=obj.client_id)
            settings = CcBaltransferinfoSerializer(baltrans, many=True)
            retval = settings.data
        except Exception as e:
            print(str(e))
            retval = ''
        return retval

    # def get_settings:

    class Meta:
        model = ClientPerson
        fields = ('client_id', 'last_name', 'first_name', 'middle_name',
            'dob', 'gender', 'ssn', 'mmn', 'email', 'pwd',
            'phone', 'phone_2', 'phone_cell', 'phone_fax', 'phone_official', 'client_info',
            'bankaccounts', 'ccaccounts', 'settings', 'baltransfer',
            'recorded_on')


#--------------------------------
# CcCompany
#--------------------------------
class CcCompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CcCompany
        fields = ('cc_company_id', 'company_name', 'url', 'contact', 'address_1', 'address_2', 'city', 'state', 'zip', 'country', 'phone', 'phone_2', 'phone_cell', 'phone_fax', 'company_info', 'recorded_on')

# ViewSets define the view behavior.
class CcCompanyViewSet(viewsets.ModelViewSet):
    queryset = CcCompany.objects.all()
    serializer_class = CcCompanySerializer

#--------------------------------
# CcCard
#--------------------------------
class CcCardSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='cc_company.company_name')
    # company_name = serializers.RelatedField(source='cc_company', read_only='True')
    class Meta:
        model = CcCard
        fields = ('cc_card_id', 'cc_company_id', 'company_name', 'card_name', 'version', 'annual_fee', 'first_year_free', 'recorded_on')

# ViewSets define the view behavior.
class CcCardViewSet(viewsets.ModelViewSet):
    queryset = CcCard.objects.all()
    serializer_class = CcCardSerializer


#--------------------------------
# ClientCcAccount
#--------------------------------
class ClientCcaccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientCcAccount
        fields = ('ccaccount_id', 'client_id', 'cc_card_id', 'cc_card_type', 'name', 'account', 'account_info', 'bank_name', 'bank_account_num', 'cc_login', 'cc_password', 'cc_status', 'annual_fee', 'credit_limit', 'self_lender', 'addtional_card', 'notes', 'ccaccount_info', 'recorded_on')

# ViewSets define the view behavior.
class ClientCcaccountViewSet(viewsets.ModelViewSet):
    queryset = ClientCcAccount.objects.all()
    serializer_class = ClientCcaccountSerializer

class ClientSettingSerializer(serializers.HyperlinkedModelSerializer):
    client = ClientPersonSerializer(read_only=False)
    class Meta:
        model = ClientSetting
        fields = ('client_setting_id', 'client', 'prefix', 'keyname', 'keyvalue')

# ViewSets define the view behavior.
class ClientSettingViewSet(viewsets.ModelViewSet):
    queryset = ClientSetting.objects.all()
    serializer_class = ClientSettingSerializer

class ClientSettingSparseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientSetting
        fields = ('client_setting_id', 'client_id', 'prefix', 'keyname', 'keyvalue')

# ViewSets define the view behavior.
class ClientSettingViewSet(viewsets.ModelViewSet):
    queryset = ClientSetting.objects.all()
    serializer_class = ClientSettingSerializer    
    
#--------------------------------
# ClientBankAccount
#--------------------------------
class ClientBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientBankAccount
        fields = ('bank_account_id', 'client_id', 'bank_name', 'account_num', 'account_login', 'account_password', 'routing_number', 'account_status', 'recorded_on')

# ViewSets define the view behavior.
class ClientBankAccountViewSet(viewsets.ModelViewSet):
    queryset = ClientBankAccount.objects.all()
    serializer_class = ClientBankAccountSerializer
