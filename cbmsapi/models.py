from django.db import models


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
    client_info = models.TextField(blank=True, null=True)  # This field type is a guess.
    recorded_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'client_person'
        unique_together = (('client_id', 'client_id'), ('last_name', 'first_name', 'middle_name'),)


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
    company_info = models.TextField(blank=True, null=True)  # This field type is a guess.
    recorded_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cc_company'


class CcCard(models.Model):
    cc_card_id = models.AutoField(primary_key=True)
    cc_company = models.ForeignKey('CcCompany', on_delete=models.CASCADE)
    card_name = models.TextField(unique=True, blank=True, null=True)
    version = models.TextField(blank=True, null=True)
    annual_fee = models.DecimalField(max_digits=152, decimal_places=0, blank=True, null=True)
    first_year_free = models.BooleanField(blank=True, null=True)
    recorded_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cc_card'


class ClientCcaccount(models.Model):
    ccaccount_id = models.AutoField(primary_key=True)
    client = models.ForeignKey('ClientPerson', on_delete=models.CASCADE, blank=True, null=True)
    cc_card = models.ForeignKey(CcCard, models.DO_NOTHING, blank=True, null=True)
    cc_card_type = models.TextField(blank=True, null=True)
    name = models.TextField()
    account = models.CharField(max_length=32)
    account_info = models.TextField()
    bank_name = models.TextField()
    bank_account_num = models.TextField(blank=True, null=True)
    cc_login = models.TextField(blank=True, null=True)
    cc_password = models.TextField(blank=True, null=True)
    cc_status = models.CharField(max_length=32, blank=True, null=True)
    annual_fee = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    self_lender = models.DateField(blank=True, null=True)
    addtional_card = models.BooleanField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    ccaccount_info = models.TextField(blank=True, null=True)  # This field type is a guess.
    recorded_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'client_ccaccount'
        unique_together = (('account', 'name'),)


class CcAction(models.Model):
    ccaction_id = models.AutoField(primary_key=True)
    ccaccount = models.ForeignKey('ClientCcaccount', models.DO_NOTHING, blank=True, null=True)
    ccaction = models.TextField(blank=True, null=True)
    action_type = models.CharField(max_length=32, blank=True, null=True)
    action_status = models.CharField(max_length=32, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    recorded_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cc_action'