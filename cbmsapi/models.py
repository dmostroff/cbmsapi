# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.postgres.fields import JSONField
from encrypted_model_fields.fields import EncryptedCharField
from rest_framework.settings import api_settings
from django.db import models

class AdmSetting(models.Model):
    adm_setting_id = models.AutoField(primary_key=True)
    prefix = models.CharField(max_length=32)
    keyname = models.TextField()
    keyvalue = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'adm_setting'
        unique_together = (('prefix', 'keyname'),)


class CcCard(models.Model):
    cc_card_id = models.AutoField(primary_key=True)
    cc_company = models.ForeignKey('CcCompany', on_delete=models.CASCADE)
    card_name = models.TextField(unique=True, blank=True, null=True)
    version = models.TextField(blank=True, null=True)
    annual_fee = models.DecimalField(max_digits=152, decimal_places=0, blank=True, null=True)
    first_year_free = models.BooleanField(blank=True, null=True)
    recorded_on = models.DateTimeField()

    class Meta:
        db_table = 'cc_card'


class CcCompany(models.Model):
    cc_company_id = models.AutoField(primary_key=True)
    company_name = models.TextField(unique=True)
    url = models.TextField(blank=True, null=True)
    contact = models.TextField(blank=True, null=True)
    address_1 = models.TextField(blank=True, null=True)
    address_2 = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=3, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    phone_2 = models.CharField(max_length=20, blank=True, null=True)
    phone_cell = models.CharField(max_length=20, blank=True, null=True)
    phone_fax = models.CharField(max_length=20, blank=True, null=True)
    company_info = JSONField() # models.TextField(blank=True, null=True)  # This field type is a guess.
    recorded_on = models.DateTimeField()

    class Meta:
        db_table = 'cc_company'


class CcTransaction(models.Model):
    cctrans_id = models.AutoField(primary_key=True)
    ccaccount_id = models.IntegerField(blank=True, null=True)
    transaction_date = models.DateTimeField()
    transaction_type = models.CharField(max_length=32)
    transaction_status = models.CharField(max_length=32, blank=True, null=True)
    credit = models.DecimalField(max_digits=152, decimal_places=0, blank=True, null=True)
    debit = models.DecimalField(max_digits=152, decimal_places=0, blank=True, null=True)
    recorded_on = models.DateTimeField()

    class Meta:
        db_table = 'cc_transaction'
        unique_together = (('transaction_date', 'transaction_type'),)


class ClientAddress(models.Model):
    address_id = models.AutoField(primary_key=True)
    client = models.ForeignKey('ClientPerson', on_delete=models.CASCADE)
    address_type = models.CharField(max_length=32)
    address_1 = models.TextField(blank=True, null=True)
    address_2 = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=3, blank=True, null=True)
    valid_from = models.DateField(blank=True, null=True)
    valid_to = models.DateField(blank=True, null=True)
    recorded_on = models.DateTimeField()

    class Meta:
        db_table = 'client_address'
        unique_together = (('address_id', 'address_id'), ('client', 'address_type', 'valid_from'),)


class ClientBankAccount(models.Model):
    bank_account_id = models.AutoField(primary_key=True)
    client = models.ForeignKey('ClientPerson', on_delete=models.CASCADE)
    bank_name = models.TextField()
    account_num = models.TextField(unique=True)
    routing_num = models.TextField(blank=True, null=True)
    account_login = models.TextField(blank=True, null=True)
    account_pwd = models.TextField(blank=True, null=True)
    account_status = models.CharField(max_length=32, blank=True, null=True)
    debit_card = models.TextField(blank=True, null=True)
    debit_info = models.TextField(blank=True, null=True)
    recorded_on = models.DateTimeField()

    class Meta:
        db_table = 'client_bank_account'


class ClientCcAccount(models.Model):
    cc_account_id = models.AutoField(primary_key=True)
    client = models.ForeignKey('ClientPerson', on_delete=models.CASCADE)
    cc_card = models.ForeignKey(CcCard, on_delete=models.CASCADE)
    name = models.TextField()
    account = EncryptedCharField(max_length=32)
    account_info = models.TextField()
    cc_login = models.TextField(blank=True, null=True)
    cc_pwd = models.TextField(blank=True, null=True)
    cc_status = models.CharField(max_length=32, blank=True, null=True)
    annual_fee_waived = models.CharField(max_length=1, blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    addtional_card = models.BooleanField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    ccaccount_info = JSONField(blank=True, null=True) # models.TextField(blank=True, null=True)  # This field type is a guess.
    recorded_on = models.DateTimeField()

    class Meta:
        db_table = 'client_cc_account'
        unique_together = (('client', 'cc_card'),)


class ClientCcAction(models.Model):
    cc_action_id = models.AutoField(primary_key=True)
    client = models.ForeignKey('ClientPerson', on_delete=models.CASCADE)
    cc_account_id = models.IntegerField()
    ccaction = models.TextField(blank=True, null=True)
    action_type = models.CharField(max_length=32, blank=True, null=True)
    action_status = models.CharField(max_length=32, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    recorded_on = models.DateTimeField()

    class Meta:
        db_table = 'client_cc_action'


class ClientCcBalanceTransfer(models.Model):
    bal_id = models.AutoField(primary_key=True)
    client = models.ForeignKey('ClientPerson', on_delete=models.CASCADE)
    cc_account_id = models.IntegerField()
    due_date = models.DateField(blank=True, null=True)
    total = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    credit_line = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    recorded_on = models.DateTimeField()

    class Meta:
        db_table = 'client_cc_balance_transfer'


class ClientCcHistory(models.Model):
    cc_hist_id = models.AutoField(primary_key=True)
    client = models.ForeignKey('ClientPerson', on_delete=models.CASCADE)
    ccaccount_id = models.IntegerField()
    ccevent = models.TextField()
    ccevent_amt = models.DecimalField(max_digits=15, decimal_places=2)
    details = models.TextField(blank=True, null=True)
    recorded_on = models.DateTimeField()

    class Meta:
        db_table = 'client_cc_history'
        unique_together = (('client', 'ccaccount_id', 'ccevent', 'recorded_on'),)


class ClientCcPoints(models.Model):
    cc_points_id = models.AutoField(primary_key=True)
    client = models.ForeignKey('ClientPerson', on_delete=models.CASCADE)
    cc_account_id = models.IntegerField()
    sold_to = models.TextField()
    sold_on = models.DateTimeField()
    sold_points = models.IntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    login = models.TextField()
    pwd = models.TextField()
    source_info = JSONField()
    recorded_on = models.DateTimeField()

    class Meta:
        db_table = 'client_cc_points'
        unique_together = (('client', 'cc_account_id', 'sold_to', 'sold_on'),)

class ClientCcTransaction(models.Model):
    cc_trans_id = models.AutoField(primary_key=True)
    client = models.ForeignKey('ClientPerson', on_delete=models.CASCADE)
    cc_account_id = models.IntegerField()
    transaction_date = models.DateTimeField()
    transaction_type = models.CharField(max_length=32)
    transaction_status = models.TextField(blank=True, null=True)
    credit = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    debit = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    recorded_on = models.DateTimeField()

    class Meta:
        db_table = 'client_cc_transaction'
        unique_together = (('client', 'cc_account_id', 'transaction_date', 'transaction_type'),)


class ClientCharges(models.Model):
    charge_id = models.AutoField(primary_key=True)
    client = models.ForeignKey('ClientPerson', on_delete=models.CASCADE)
    charge_goal = models.DecimalField(max_digits=15, decimal_places=2)
    charged = models.DecimalField(max_digits=15, decimal_places=2)
    paid = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fees = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    due_on_day = models.IntegerField(blank=True, null=True)
    charge_info = models.TextField(blank=True, null=True)
    recorded_on = models.DateTimeField()

    class Meta:
        db_table = 'client_charges'


class ClientCreditlineHistory(models.Model):
    creditline_id = models.AutoField(primary_key=True)
    client = models.ForeignKey('ClientPerson', on_delete=models.CASCADE)
    cc_account = models.ForeignKey(ClientCcAccount, models.DO_NOTHING)
    credit_line_date = models.DateField()
    credit_amt = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    credit_status = models.TextField(blank=True, null=True)
    recorded_on = models.DateTimeField()

    class Meta:
        db_table = 'client_creditline_history'
        unique_together = (('client', 'cc_account', 'credit_line_date'),)


class ClientPerson(models.Model):
    client_id = models.AutoField(primary_key=True)
    last_name = models.TextField()
    first_name = models.TextField()
    middle_name = models.TextField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    ssn = models.CharField(max_length=9, blank=True, null=True)
    mmn = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    pwd = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    phone_2 = models.CharField(max_length=20, blank=True, null=True)
    phone_cell = models.CharField(max_length=20, blank=True, null=True)
    phone_fax = models.CharField(max_length=20, blank=True, null=True)
    phone_official = models.CharField(max_length=20, blank=True, null=True)
    client_info = JSONField() # models.TextField(blank=True, null=True)  # This field type is a guess.
    recorded_on = models.DateTimeField()

    class Meta:
        db_table = 'client_person'
        unique_together = (('client_id', 'client_id'), ('last_name', 'first_name', 'middle_name'),)


class ClientSelfLender(models.Model):
    self_lender_id = models.AutoField(primary_key=True)
    client = models.ForeignKey('ClientPerson', on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    pay_from = models.TextField(blank=True, null=True)
    monthly_due_date = models.IntegerField()
    termination_date = models.DateField()
    login = models.TextField(blank=True, null=True)
    pwd = models.TextField(blank=True, null=True)
    recorded_on = models.DateTimeField()

    class Meta:
        db_table = 'client_self_lender'
        unique_together = (('client', 'start_date', 'duration'),)


class ClientSetting(models.Model):
    client_setting_id = models.AutoField(primary_key=True)
    client = models.ForeignKey('ClientPerson', on_delete=models.CASCADE)
    prefix = models.CharField(max_length=32)
    keyname = models.TextField()
    keyvalue = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'client_setting'
        unique_together = (('client', 'prefix', 'keyname'),)
