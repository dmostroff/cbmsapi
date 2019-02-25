from rest_framework import serializers, viewsets

from django.contrib.auth.models import User
from cbmsapi.models import ClientPerson
from cbmsapi.models import CcCompany
from cbmsapi.models import CcCard
from cbmsapi.models import ClientBankAccount
from cbmsapi.models import ClientCcAccount
from cbmsapi.models import ClientCreditline
from cbmsapi.models import ClientCharges
from cbmsapi.models import CcBaltransferinfo
from cbmsapi.models import CcTransaction
from cbmsapi.models import CcPoints
from cbmsapi.models import ClientSelfLender
from cbmsapi.models import ClientSetting
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


class ClientPersonNameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientPerson
        fields = ('client_id', 'last_name', 'first_name', 'middle_name')        

class ClientSummarySerializer(serializers.ModelSerializer):

    client_name = serializers.SerializerMethodField('_get_full_name')
    bank_accounts = serializers.SerializerMethodField('_get_client_bankaccounts')
    cc_accounts = serializers.SerializerMethodField('_get_client_ccaccounts')
    creditline = serializers.SerializerMethodField('_get_client_creditline')
    cc_points = serializers.SerializerMethodField('_get_cc_points')
    self_lender = serializers.SerializerMethodField('_get_self_lender')
    # baltransfer = serializers.SerializerMethodField('_get_client_baltransfer')


    def _get_full_name(self, obj):
        try:
            middle_name = ' '+obj.middle_name if obj.middle_name is not None else ''
            retval = '{}{} {}'.format(obj.first_name, middle_name, obj.last_name)
        except:
            retval = ''
        return retval

    def _get_client_bankaccounts(self, obj):
        """
        Get client's bank accounts
        """
        try:
            clientBankAccount = ClientBankAccount.objects.filter(client_id=obj.client_id).order_by('-bank_account_id')[:1].get()
            retval = clientBankAccount.bank_name
        except:
            retval = ''
        return retval

    def _get_client_ccaccounts(self, obj):
        """
        Get client's credit card accounts
        """
        try:
            clientCcAccount = ClientCcAccount.objects.filter(client_id=obj.client_id).order_by('-ccaccount_id')[:1].get()
            retval = clientCcAccount.cc_card.card_name
        except:
            retval = ''
        return retval

    def _get_client_creditline(self, obj):
        try:
            query = ClientCreditline.objects.filter(client_id=obj.client_id).values('credit_amt')[:1]
            retval = query[0]['credit_amt']
        except Exception as e:
            print(str(e))
            retval = 0
        return retval

    def _get_cc_points(self, obj):
        try:
            ccPoints = CcPoints.objects.filter(client_id=obj.client_id)
            ser = CcPointsSerializer(ccPoints, many=True)
            retval = ser.data
        except:
            retval = ''
        return retval

    def _get_self_lender(self, obj):
        try:
            ccPoints = ClientSelfLender.objects.filter(client_id=obj.client_id)
            ser = ClientSelfLenderSerializer(ccPoints, many=True)
            retval = ser.data
        except:
            retval = ''
        return retval

    class Meta:
        model = ClientPerson
        fields = ('client_id', 'client_name', 'bank_accounts', 'cc_accounts', 'creditline', 'cc_points')

class ClientSummaryViewSet(viewsets.ModelViewSet):
    queryset = ClientPerson.objects.all()
    serializer_class = ClientSummarySerializer


class ClientPersonFullSerializer(serializers.ModelSerializer):
    # settings = ClientSetting.objects.filter(client_id = self.model.client_id)
    bank_accounts = serializers.SerializerMethodField('_get_client_bankaccounts')
    cc_accounts = serializers.SerializerMethodField('_get_client_ccaccounts')
    charges = serializers.SerializerMethodField('_get_client_charges')
    baltransfer = serializers.SerializerMethodField('_get_client_baltransfer')
    creditline = serializers.SerializerMethodField('_get_client_creditline')
    cc_points = serializers.SerializerMethodField('_get_cc_points')
    settings = serializers.SerializerMethodField('_get_client_settings')

    def _get_client_bankaccounts(self, obj):
        """
        Get client's bank accounts
        """
        try:
            clientBankAccount = ClientBankAccount.objects.filter(client_id=obj.client_id)
            ser = ClientBankAccountSerializer(clientBankAccount, many=True)
            retval = ser.data
        except:
            retval = ''
        return retval

    def _get_client_ccaccounts(self, obj):
        """
        Get client's credit card accounts
        """
        try:
            clientCcAccount = ClientCcAccount.objects.filter(client_id=obj.client_id)
            ser = ClientCcAccountSerializer(clientCcAccount, many=True)
            retval = ser.data
        except:
            retval = ''
        return retval

    def _get_client_creditline(self, obj):
        """
        Get client's credit card accounts
        """
        try:
            clientCreditline = ClientCreditline.objects.filter(client_id=obj.client_id)
            ser = ClientCreditlineSerializer(clientCreditline, many=True)
            retval = ser.data
        except:
            retval = ''
        return retval

    def _get_client_charges(self, obj):
        """
        Get client's credit card accounts
        """
        try:
            clientCharges = ClientCharges.objects.filter(client_id=obj.client_id)
            ser = ClientChargesSerializer(clientCharges, many=True)
            retval = ser.data
        except:
            retval = ''
        return retval

    def _get_client_baltransfer(self, obj):
        try:
            baltrans = CcBaltransferinfo.objects.filter(client_id=obj.client_id)
            ser = CcBaltransferinfoSerializer(baltrans, many=True)
            retval = ser.data
        except Exception as e:
            print(str(e))
            retval = ''
        return retval

    def _get_cc_points(self, obj):
        try:
            ccPoints = CcPoints.objects.filter(client_id=obj.client_id)
            ser = CcPointsSerializer(ccPoints, many=True)
            retval = ser.data
        except:
            retval = ''
        return retval

    def _get_self_lender(self, obj):
        try:
            ccPoints = ClientSelfLender.objects.filter(client_id=obj.client_id)
            ser = ClientSelfLenderSerializer(ccPoints, many=True)
            retval = ser.data
        except:
            retval = ''
        return retval

    def _get_client_settings(self, obj):
        """
        Get client settings
        """
        try:
            clientSetting = ClientSetting.objects.filter(client_id=obj.client_id)
            settings = ClientSettingSerializer(clientSetting, many=True)
            retval = settings.data
        except:
            retval = ''
        return retval

    class Meta:
        model = ClientPerson
        fields = ('client_id', 'last_name', 'first_name', 'middle_name',
            'dob', 'gender', 'ssn', 'mmn', 'email', 'pwd',
            'phone', 'phone_2', 'phone_cell', 'phone_fax', 'phone_official', 'client_info',
            'bank_accounts', 'cc_accounts', 'charges', 'baltransfer', 'creditline', 'cc_points', 'settings',
            'recorded_on')

class ClientPersonSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientPerson
        fields = ('client_id', 'last_name', 'first_name', 'middle_name',
            'dob', 'gender', 'ssn', 'mmn', 'email', 'pwd',
            'phone', 'phone_2', 'phone_cell', 'phone_fax', 'phone_official', 'client_info',
            'bankaccounts', 'ccaccounts', 'baltransfer', 'ccpoints', 'settings'
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
#--------------------------------
# ClientCcAccount
#--------------------------------
class ClientCcAccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientCcAccount
        fields = ('ccaccount_id', 'client_id', 'cc_card_id', 'cc_card_type', 'name', 'account', 'account_info', 'bank_name', 'bank_account_num', 'cc_login', 'cc_password', 'cc_status', 'annual_fee', 'credit_limit', 'self_lender', 'addtional_card', 'notes', 'ccaccount_info', 'recorded_on')

# ViewSets define the view behavior.
class ClientCcAccountViewSet(viewsets.ModelViewSet):
    queryset = ClientCcAccount.objects.all()
    serializer_class = ClientCcAccountSerializer

#--------------------------------
# ClientCreditline
#--------------------------------
class ClientCreditlineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientCreditline
        fields = ('creditline_id', 'client_id', 'credit_line_date', 'credit_amt', 'credit_status', 'recorded_on')

# ViewSets define the view behavior.
class ClientCreditlineViewSet(viewsets.ModelViewSet):
    queryset = ClientCreditline.objects.all()
    serializer_class = ClientCreditlineSerializer

#--------------------------------
# ClientCharges
#--------------------------------
class ClientChargesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientCharges
        fields = ('charge_id', 'client_id', 'charge_goal', 'charged', 'paid', 'fees', 'due_on_day', 'charge_info', 'recorded_on')

# ViewSets define the view behavior.
class ClientChargesViewSet(viewsets.ModelViewSet):
    queryset = ClientCharges.objects.all()
    serializer_class = ClientChargesSerializer

#--------------------------------
# BalanceTransfer
#--------------------------------
class CcBaltransferinfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CcBaltransferinfo
        fields = ('bal_id', 'client_id', 'ccaccount_id', 'due_date', 'total', 'credit_line', 'recorded_on')

# ViewSets define the view behavior.
class CcBaltransferinfoViewSet(viewsets.ModelViewSet):
    queryset = CcBaltransferinfo.objects.all()
    serializer_class = CcBaltransferinfoSerializer

#--------------------------------
# CcPoints
#--------------------------------
class CcPointsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CcPoints
        fields = ('cc_points_id', 'client_id', 'sold_to', 'sold_on', 'login', 'pwd', 'price', 'source_info', 'recorded_on')

# ViewSets define the view behavior.
class CcPointsViewSet(viewsets.ModelViewSet):
    queryset = CcPoints.objects.all()
    serializer_class = CcPointsSerializer

#--------------------------------
# ClientSelfLender
#--------------------------------
class ClientSelfLenderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientSelfLender
        fields = ('self_lender_id', 'client_id', 'start_date', 'duration', 'pay_from', 'due_on_day', 'pwd', 'recorded_on')

# ViewSets define the view behavior.
class ClientSelfLenderViewSet(viewsets.ModelViewSet):
    queryset = ClientSelfLender.objects.all()
    serializer_class = ClientSelfLenderSerializer

#--------------------------------
# ClientSetting
#--------------------------------
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
# CcTransaction
#--------------------------------
class CcTransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CcTransaction
        fields = ('cctrans_id', 'ccaccount_id', 'transaction_date', 'transaction_type', 'transaction_status', 'credit', 'debit', 'recorded_on')

# ViewSets define the view behavior.
class CcTransactionViewSet(viewsets.ModelViewSet):
    queryset = CcTransaction.objects.all()
    serializer_class = CcTransactionSerializer

