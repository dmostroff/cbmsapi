from rest_framework import serializers, viewsets

from django.contrib.auth.models import User
from cbmsapi.models import ClientPerson
from cbmsapi.models import CcCompany
from cbmsapi.models import CcCard
from cbmsapi.models import ClientBankAccount
from cbmsapi.models import ClientCcAccount
from cbmsapi.models import ClientCreditlineHistory
from cbmsapi.models import ClientCharges
from cbmsapi.models import ClientCcBalanceTransfer
from cbmsapi.models import ClientCcTransaction
from cbmsapi.models import ClientCcPoints
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
            cardsum = []
            for card in ser.data:
                cardsum.append(card['card_name'])
            retval = '~'.join(cardsum)
            # retval = ser.data
        except Exception as e:
            print(str(e))
            retval = ''
        return retval

    def _get_client_creditline(self, obj):
        try:
            query = ClientCreditlineHistory.objects.filter(client_id=obj.client_id).values('credit_amt')[:1]
            retval = query[0]['credit_amt']
        except Exception as e:
            print(str(e))
            retval = 0
        return retval

    def _get_client_charges(self, obj):
        try:
            retval = ClientCharges.objects.filter(client_id=obj.client_id).count()
            # ser = CcPointsSerializer(ccPoints, many=True)
            # retval = ser.data
        except:
            retval = ''
        return retval

    def _get_cc_points(self, obj):
        try:
            retval = ClientCcPoints.objects.filter(client_id=obj.client_id).count()
            # ser = CcPointsSerializer(ccPoints, many=True)
            # retval = ser.data
        except:
            retval = ''
        return retval

    def _get_self_lender(self, obj):
        try:
            retval = ClientSelfLender.objects.filter(client_id=obj.client_id).count()
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
        fields = ('bank_account_id', 'client', 'bank_name', 'account_num', 'routing_num', 'account_login', 'account_pwd', 'account_status', 'debit_card', 'debit_info', 'recorded_on')

# ViewSets define the view behavior.
class ClientBankAccountViewSet(viewsets.ModelViewSet):
    queryset = ClientBankAccount.objects.all()
    serializer_class = ClientBankAccountSerializer
#--------------------------------
# ClientCcAccount
#--------------------------------
class ClientCcAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientCcAccount
        fields = ('cc_account_id', 'client', 'cc_card', 'name', 'account', 'account_info', 'cc_login', 'cc_pwd', 'cc_status', 'annual_fee_waived', 'credit_limit', 'addtional_card', 'notes', 'ccaccount_info', 'recorded_on')
    
    # def create(self, validated_data):
    #     data = validated_data.pop('person')
    #     ccaccount, created = models.ClientCcAccount.objects.update_or_create(
    #         pk=ccaccount.get('id'),
    #         defaults=ccaccount
    #     )
    #     validated_data['person'] = person
    #     person_extension = models.PersonExtension.objects.create(
    #         **validated_data
    #     )
    #     return person_extension

    # def update(self, instance, validated_data):
    #     person_data = validated_data.get('person')
    #     instance.person.name = person_data.get(
    #         'name',
    #         instance.person.name
    #     )
    #     instance.person.save()
    #     instance.extra_data = validated_data.get(
    #         'extra_data',
    #         instance.extra_data
    #     )
    #     instance.save()
    #     return instance

class ClientCcAccountViewSet(viewsets.ModelViewSet):
    queryset = ClientCcAccount.objects.all()
    serializer_class = ClientCcAccountSerializer

class ClientCcAccountFullSerializer(serializers.ModelSerializer):
    client = ClientPersonSerializer(read_only=False)
    cc_card = CcCardSerializer(read_only=False)

    class Meta:
        model = ClientCcAccount
        fields = ('cc_account_id', 'client', 'cc_card', 'name', 'account', 'account_info', 'cc_login', 'cc_pwd', 'cc_status', 'annual_fee_waived', 'credit_limit', 'addtional_card', 'notes', 'ccaccount_info', 'recorded_on')


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

#--------------------------------
# ClientCreditline
#--------------------------------
class ClientCreditlineHistorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientCreditlineHistory
        fields = ('creditline_id', 'client', 'cc_account_id', 'credit_line_date', 'credit_amt', 'credit_status', 'recorded_on')

# ViewSets define the view behavior.
class ClientCreditlineHistoryViewSet(viewsets.ModelViewSet):
    queryset = ClientCreditlineHistory.objects.all()
    serializer_class = ClientCreditlineHistorySerializer

#--------------------------------
# ClientCharges
#--------------------------------
class ClientChargesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientCharges
        fields = ('charge_id', 'client', 'charge_goal', 'charged', 'paid', 'fees', 'due_on_day', 'charge_info', 'recorded_on')

# ViewSets define the view behavior.
class ClientChargesViewSet(viewsets.ModelViewSet):
    queryset = ClientCharges.objects.all()
    serializer_class = ClientChargesSerializer

#--------------------------------
# BalanceTransfer
#--------------------------------
class ClientCcBalanceTransferSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientCcBalanceTransfer
        fields = ('bal_id', 'client', 'cc_account', 'due_date', 'total', 'credit_line', 'recorded_on')

# ViewSets define the view behavior.
class ClientCcBalanceTransferViewSet(viewsets.ModelViewSet):
    queryset = ClientCcBalanceTransfer.objects.all()
    serializer_class = ClientCcBalanceTransferSerializer

#--------------------------------
# ClientCcPoints
#--------------------------------
class ClientCcPointsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientCcPoints
        fields = ('cc_points_id', 'client', 'cc_account_id', 'sold_to', 'sold_on', 'login', 'pwd', 'price', 'source_info', 'recorded_on')

# ViewSets define the view behavior.
class ClientCcPointsViewSet(viewsets.ModelViewSet):
    queryset = ClientCcPoints.objects.all()
    serializer_class = ClientCcPointsSerializer

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
class ClientSettingSparseViewSet(viewsets.ModelViewSet):
    queryset = ClientSetting.objects.all()
    serializer_class = ClientSettingSparseSerializer
    

#--------------------------------
# CcTransaction
#--------------------------------
class ClientCcTransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientCcTransaction
        fields = ('cc_trans_id', 'client', 'cc_account_id', 'transaction_date', 'transaction_type', 'transaction_status', 'credit', 'debit', 'recorded_on')

# ViewSets define the view behavior.
class ClientCcTransactionViewSet(viewsets.ModelViewSet):
    queryset = ClientCcTransaction.objects.all()
    serializer_class = ClientCcTransactionSerializer

