from rest_framework import serializers, viewsets

from django.contrib.auth.models import User
from cbmsapi.models import ClientPerson
from cbmsapi.models import CcCompany
from cbmsapi.models import CcCard

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
class CcCardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CcCard
        fields = ('cc_card_id', 'cc_company_id', 'card_name', 'version', 'annual_fee', 'first_year_free', 'recorded_on')

# ViewSets define the view behavior.
class CcCardViewSet(viewsets.ModelViewSet):
    queryset = CcCard.objects.all()
    serializer_class = CcCardSerializer
