from rest_framework import serializers, viewsets
from django.contrib.auth.models import User
from datetime import datetime

from cbmsapi.models import AdmSetting
from cbmsapi.models import CcCard
from cbmsapi.models import CcCompany
from cbmsapi.models import CcTransaction
from cbmsapi.models import ClientAddress
from cbmsapi.models import ClientBankAccount
from cbmsapi.models import ClientCcAccount
from cbmsapi.models import ClientCcAction
from cbmsapi.models import ClientCcBalanceTransfer
from cbmsapi.models import ClientCcHistory
from cbmsapi.models import ClientCcPoints
from cbmsapi.models import ClientCcTransaction
from cbmsapi.models import ClientCharges
from cbmsapi.models import ClientCreditlineHistory
from cbmsapi.models import ClientPerson
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
# AdmSetting
#--------------------------------
class AdmSettingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AdmSetting
        fields = ('adm_setting_id', 'prefix', 'keyname', 'keyvalue')

# ViewSets define the view behavior.
class AdmSettingViewSet(viewsets.ModelViewSet):
    queryset = AdmSetting.objects.all()
    serializer_class = AdmSettingSerializer

class AdmSettingKVSerializer( serializers.ModelSerializer):
    class Meta:
        model = AdmSetting
        fields = ('keyname', 'keyvalue')

#--------------------------------
# CcCard
#--------------------------------
class CcCardSerializer(serializers.HyperlinkedModelSerializer):
    company_name = serializers.CharField(source='cc_company.company_name')

    class Meta:
        model = CcCard
        fields = ('cc_card_id', 'cc_company_id', 'company_name', 'card_name', 'version', 'annual_fee', 'first_year_free', 'recorded_on')

# ViewSets define the view behavior.
class CcCardViewSet(viewsets.ModelViewSet):
    queryset = CcCard.objects.all()
    serializer_class = CcCardSerializer

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

#--------------------------------
# ClientAddress
#--------------------------------
class ClientAddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientAddress
        fields = ('address_id', 'client_id', 'address_type', 'address_1', 'address_2', 'city', 'state', 'zip', 'country', 'valid_from', 'valid_to', 'recorded_on')

# ViewSets define the view behavior.
class ClientAddressViewSet(viewsets.ModelViewSet):
    queryset = ClientAddress.objects.all()
    serializer_class = ClientAddressSerializer

#--------------------------------
# ClientBankAccount
#--------------------------------
class ClientBankAccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientBankAccount
        fields = ('bank_account_id', 'client_id', 'bank_name', 'account_num', 'routing_num', 'account_login', 'account_pwd', 'account_status', 'debit_card', 'debit_info', 'recorded_on')

# ViewSets define the view behavior.
class ClientBankAccountViewSet(viewsets.ModelViewSet):
    queryset = ClientBankAccount.objects.all()
    serializer_class = ClientBankAccountSerializer

#--------------------------------
# ClientCcAccount
#--------------------------------
class ClientCcAccountSerializer(serializers.HyperlinkedModelSerializer):
    cc_card_name = serializers.CharField(source='cc_card.card_name')
    cc_status_desc = serializers.SerializerMethodField('_get_cc_status')

    def _get_cc_status(self, obj):
        try:
            retval = AdmSetting.objects.get(prefix='CARDSTATUS', keyname=obj.cc_status).keyvalue
        except Exception as e:
            retval = str(e)
        return retval

    class Meta:
        model = ClientCcAccount
        fields = ('cc_account_id', 'client_id', 'cc_card_id', 'cc_card_name', 'name', 'account', 'account_info', 'cc_login', 'cc_pwd', 'cc_status', 'cc_status_desc', 'annual_fee_waived', 'credit_limit', 'addtional_card', 'notes', 'ccaccount_info', 'recorded_on')

# ViewSets define the view behavior.
class ClientCcAccountViewSet(viewsets.ModelViewSet):
    queryset = ClientCcAccount.objects.all()
    serializer_class = ClientCcAccountSerializer

#--------------------------------
# ClientCcAction
#--------------------------------
class ClientCcActionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientCcAction
        fields = ('cc_action_id', 'client_id', 'cc_account_id', 'ccaction', 'action_type', 'action_status', 'due_date', 'details', 'recorded_on')

# ViewSets define the view behavior.
class ClientCcActionViewSet(viewsets.ModelViewSet):
    queryset = ClientCcAction.objects.all()
    serializer_class = ClientCcActionSerializer

#--------------------------------
# ClientCcBalanceTransfer
#--------------------------------
class ClientCcBalanceTransferSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientCcBalanceTransfer
        fields = ('bal_id', 'client_id', 'cc_account_id', 'due_date', 'total', 'credit_line', 'recorded_on')

# ViewSets define the view behavior.
class ClientCcBalanceTransferViewSet(viewsets.ModelViewSet):
    queryset = ClientCcBalanceTransfer.objects.all()
    serializer_class = ClientCcBalanceTransferSerializer

#--------------------------------
# ClientCcHistory
#--------------------------------
class ClientCcHistorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientCcHistory
        fields = ('cc_hist_id', 'client_id', 'ccaccount_id', 'ccevent', 'ccevent_amt', 'details', 'recorded_on')

# ViewSets define the view behavior.
class ClientCcHistoryViewSet(viewsets.ModelViewSet):
    queryset = ClientCcHistory.objects.all()
    serializer_class = ClientCcHistorySerializer

#--------------------------------
# ClientCcPoints
#--------------------------------
class ClientCcPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientCcPoints
        fields = ('cc_points_id', 'client_id', 'cc_account_id', 'sold_to', 'sold_on', 'sold_points', 'price', 'login', 'pwd', 'source_info', 'recorded_on')

# ViewSets define the view behavior.
class ClientCcPointsViewSet(viewsets.ModelViewSet):
    queryset = ClientCcPoints.objects.all()
    serializer_class = ClientCcPointsSerializer

#--------------------------------
# ClientCcTransaction
#--------------------------------
class ClientCcTransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientCcTransaction
        fields = ('cc_trans_id', 'client_id', 'cc_account_id', 'transaction_date', 'transaction_type', 'transaction_status', 'credit', 'debit', 'recorded_on')

# ViewSets define the view behavior.
class ClientCcTransactionViewSet(viewsets.ModelViewSet):
    queryset = ClientCcTransaction.objects.all()
    serializer_class = ClientCcTransactionSerializer

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
# ClientCreditlineHistory
#--------------------------------
class ClientCreditlineHistorySerializer(serializers.ModelSerializer):
    credit_status_desc = serializers.SerializerMethodField('_get_status_description')

    def _get_status_description(self, obj):
        try:
            retval = AdmSetting.objects.get(prefix='CREDITLINESTATUS', keyname=obj.credit_status).keyvalue
            # retval = AdmSettingKVSerializer( statuses, many=False).data
        except Exception as e:
            retval = str(e)
        return retval

    # def _get_statuses(self, obj):
    #     try:
    #         statuses = AdmSetting.objects.filter(prefix='CREDITLINESTATUS')
    #         retval = AdmSettingKVSerializer( statuses, many=True).data
    #     except Exception as e:
    #         retval = str(e)
        # return retval
    class Meta:
        model = ClientCreditlineHistory
        fields = ('creditline_id', 'client_id', 'cc_account_id', 'credit_line_date', 'credit_amt', 'credit_status', 'credit_status_desc', 'recorded_on')

# ViewSets define the view behavior.
class ClientCreditlineHistoryViewSet(viewsets.ModelViewSet):
    queryset = ClientCreditlineHistory.objects.all()
    serializer_class = ClientCreditlineHistorySerializer

class ClientCreditlineHistoryEditSerializer(serializers.ModelSerializer):
    credit_statuses = serializers.SerializerMethodField('_get_statuses')

    def _get_statuses(self, obj):
        try:
            statuses = AdmSetting.objects.filter(prefix='CREDITLINESTATUS')
            retval = AdmSettingKVSerializer( statuses, many=True).data
        except Exception as e:
            retval = str(e)
        return retval

    class Meta:
        model = ClientCreditlineHistory
        fields = ('creditline_id', 'client_id', 'cc_account_id', 'credit_line_date', 'credit_amt', 'credit_status', 'credit_statuses', 'recorded_on')


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

#--------------------------------
# ClientSelfLender
#--------------------------------
class ClientSelfLenderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientSelfLender
        fields = ('self_lender_id', 'client_id', 'start_date', 'duration', 'pay_from', 'monthly_due_date', 'termination_date', 'login', 'pwd', 'recorded_on')

# ViewSets define the view behavior.
class ClientSelfLenderViewSet(viewsets.ModelViewSet):
    queryset = ClientSelfLender.objects.all()
    serializer_class = ClientSelfLenderSerializer

#--------------------------------
# ClientSetting
#--------------------------------
class ClientSettingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientSetting
        fields = ('client_setting_id', 'client_id', 'prefix', 'keyname', 'keyvalue')

# ViewSets define the view behavior.
class ClientSettingViewSet(viewsets.ModelViewSet):
    queryset = ClientSetting.objects.all()
    serializer_class = ClientSettingSerializer


#-----------------------------------------
#  Additional serializers
#------------------------------------------
class ClientPersonNameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientPerson
        fields = ('client_id', 'last_name', 'first_name', 'middle_name')        

class ClientSummarySerializer(serializers.ModelSerializer):

    client_name = serializers.SerializerMethodField('_get_full_name')
    bank_accounts = serializers.SerializerMethodField('_get_client_bankaccounts')
    cc_accounts = serializers.SerializerMethodField('_get_client_ccaccounts')
    creditline = serializers.SerializerMethodField('_get_client_creditline')
    charges = serializers.SerializerMethodField('_get_client_charges')
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
            clientCcAccount = ClientCcAccount.objects.filter(client_id=obj.client_id)
            ser = ClientCcAccountCardNameSerializer(clientCcAccount, many=True)
            cardsum = [card['card_name'] for card in ser.data]
            retval = '~'.join(cardsum)
            # retval = ser.data
        except Exception as e:
            print(str(e))
            retval = ''
        return retval

    def _get_client_creditline(self, obj):
        try:
            query = ClientCreditlineHistory.objects.filter(client_id=obj.client_id)[:1]
            ser = ClientCreditlineHistorySerializer(query, many=True)
            # retval = ';'.join(['{:8,.2f} as of {:%d %b %Y}'.format(float(credit['credit_amt']), credit['credit_line_date']) for credit in ser.data])
            retval = ';'.join(['${:,.2f} as of {:%d %b %Y}'.format(float(credit['credit_amt']), datetime.strptime(credit['credit_line_date'], "%Y-%m-%d")) for credit in ser.data])
        except Exception as e:
            print(str(e))
            retval = str(e)
        return retval

    def _get_client_charges(self, obj):
        try:
            count = ClientCharges.objects.filter(client_id=obj.client_id).count()
            retval = '{0} charge(s)'.format(count)
        except:
            retval = ''
        return retval

    def _get_cc_points(self, obj):
        try:
            count = ClientCcPoints.objects.filter(client_id=obj.client_id).count()
            retval = '{0} Points(s)'.format(count)
        except:
            retval = ''
        return retval

    def _get_self_lender(self, obj):
        try:
            count = ClientSelfLender.objects.filter(client_id=obj.client_id).count()
            retval = '{0} Self Lender(s)'.format(count)
            # ser = ClientSelfLenderSerializer(ccPoints, many=True).A
            # retval = ser.data
        except:
            retval = ''
        return retval

    class Meta:
        model = ClientPerson
        fields = ('client_id', 'client_name', 'bank_accounts', 'cc_accounts', 'creditline', 'charges'
            , 'cc_points', 'self_lender')

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
        Get client's credit line
        """
        try:
            clientCreditlineHistory = ClientCreditlineHistory.objects.filter(client_id=obj.client_id)
            ser = ClientCreditlineSerializer(clientCreditlineHistory, many=True)
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
            baltrans = ClientCcBalanceTransfer.objects.filter(client_id=obj.client_id)
            ser = ClientCcBalanceTransferSerializer(baltrans, many=True)
            retval = ser.data
        except Exception as e:
            print(str(e))
            retval = ''
        return retval

    def _get_cc_points(self, obj):
        try:
            ccPoints = ClientCcPoints.objects.filter(client_id=obj.client_id)
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


class ClientCcAccountFullSerializer(serializers.ModelSerializer):
    client = ClientPersonSerializer(read_only=False)
    cc_card = CcCardSerializer(read_only=False)

    class Meta:
        model = ClientCcAccount
        fields = ('cc_account_id', 'client', 'cc_card', 'name', 'account', 'account_info', 'cc_login', 'cc_pwd', 'cc_status', 'annual_fee_waived', 'credit_limit', 'addtional_card', 'notes', 'ccaccount_info', 'recorded_on')

class ClientCcAccountSummarySerializer(serializers.ModelSerializer):
    cc_card_name = serializers.CharField(source='cc_card.card_name')
    baltransfer = serializers.SerializerMethodField('_get_baltransfer')
    cc_points = serializers.SerializerMethodField('_get_cc_points')

    def _get_baltransfer(self, obj):
        try:
            baltrans = ClientCcBalanceTransfer.objects.filter(client_id=obj.client_id, cc_account_id=obj.cc_account_id).order_by('-due_date')
            ser = ClientCcBalanceTransferSerializer(baltrans, many=True)
            retval = ser.data
        except Exception as e:
            print(str(e))
            retval = ''
        return retval

    def _get_cc_points(self, obj):
        try:
            ccPoints = ClientCcPoints.objects.filter(client_id=obj.client_id, cc_account_id=obj.cc_account_id).order_by('-sold_on')[:1]
            ser = ClientCcPointsSerializer(ccPoints, many=True)
            retval = ser.data
        except Exception as e:
            print(str(e))
            retval = ''
        return retval


    class Meta:
        model = ClientCcAccount
        fields = ('cc_account_id', 'client_id', 'cc_card_name', 'name', 'account', 'account_info', 'cc_login', 'cc_pwd', 'cc_status', 'annual_fee_waived', 'credit_limit', 'addtional_card', 'notes', 'ccaccount_info'
            , 'baltransfer'
            , 'cc_points'
            , 'recorded_on')


# ViewSets define the view behavior.
class ClientCcAccountCardNameSerializer(serializers.ModelSerializer):
    # cc_card = serializers.StringRelatedField(many=True)
    # cc_card = CcCardSerializer(read_only=False)
    client_name = serializers.SerializerMethodField("_get_client_name")
    card_name = serializers.SerializerMethodField('_get_cc_card_name')
    # account_num = serializers.SerializerMethodField('_get_account_num')
    # card_name = serializers.CharField(source='cc_card.card_name')
    # company_name = serializers.CharField(source='cc_card.cc_company.company_name')
    # card_full_name = serializers.CharField(source='cc_card.card_name + cc_card.cc_card_id')

    def _get_client_name(self, obj):
        try:
            retval = ("{0}, {1} {2}".format(obj.client.last_name
                , obj.client.first_name
                , '' if obj.client.middle_name is None else obj.client.middle_name)).strip()
        except Exception as e:
            retval = str(e)
        return retval

    def _get_cc_card_name(self, obj):
        try:
            retval = "{}:{}".format(obj.cc_card.cc_company.company_name, obj.cc_card.card_name)
        except Exception as e:
            retval = str(e)
        return retval

    # def _get_account_num(self, obj):
    #     try:
            
    #         retval = 

    class Meta:
        model = ClientCcAccount
        fields = ('cc_account_id', 'card_name', 'client_id', 'client_name', 'account', 'credit_limit')

        # fields = ('cc_account_id', 'client', 'cc_card', 'card_name', 'company_name', 'cc_card_type', 'name', 'account', 'account_info', 'bank_name', 'bank_account_num', 'cc_login', 'cc_password', 'cc_status', 'annual_fee', 'credit_limit', 'self_lender', 'addtional_card', 'notes', 'ccaccount_info', 'recorded_on')
class ClientCcAccountCardNameViewSet(viewsets.ModelViewSet):
    queryset = ClientCcAccount.objects.all() # .only('clieclient', 'cc_card', 'client')
    serializer_class = ClientCcAccountCardNameSerializer
