# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Account(models.Model):
    id = models.OneToOneField(
        'Accounttype', models.DO_NOTHING, db_column='id', primary_key=True)
    state = models.IntegerField()
    # Field name made lowercase.
    enablechecks = models.IntegerField(db_column='enableChecks')
    # Field name made lowercase.
    issingle = models.IntegerField(db_column='isSingle')
    credit = models.FloatField()
    debit = models.FloatField()
    # Field name made lowercase.
    isdollar = models.BooleanField(db_column='isDollar')
    # Field name made lowercase.
    usercui = models.ForeignKey(
        'Singleuser', models.DO_NOTHING, db_column='userCui', blank=True, null=True)
    # Field name made lowercase.
    userbusiness = models.ForeignKey(
        'Businessuser', models.DO_NOTHING, db_column='userBusiness', blank=True, null=True)
    checks = models.IntegerField()
    # Field name made lowercase.
    enableauthchecks = models.IntegerField(db_column='enableAuthChecks')

    class Meta:
        managed = False
        db_table = 'Account'


class Accountcheck(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    account = models.ForeignKey(
        Account, models.DO_NOTHING, db_column='account')
    # Field name made lowercase.
    chargeddate = models.DateField(
        db_column='chargedDate', blank=True, null=True)
    charged = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'AccountCheck'


class Accounttype(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    saving = models.ForeignKey(
        'Savingaccount', models.DO_NOTHING, db_column='saving', blank=True, null=True)
    # Field name made lowercase.
    timedsaving = models.ForeignKey(
        'Timedsavingaccount', models.DO_NOTHING, db_column='timedSaving', blank=True, null=True)
    monetary = models.ForeignKey(
        'Monetaryaccount', models.DO_NOTHING, db_column='monetary', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'AccountType'


class Authcheck(models.Model):
    id = models.OneToOneField(
        Accountcheck, models.DO_NOTHING, db_column='id', primary_key=True)
    authorized = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'AuthCheck'


class Businessuser(models.Model):
    # Field name made lowercase.
    comercialname = models.CharField(
        db_column='comercialName', primary_key=True, max_length=50)
    # Field name made lowercase.
    businesstype = models.CharField(
        db_column='businessType', max_length=50, blank=True, null=True)
    name = models.CharField(max_length=30)
    agent = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    phone = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'BusinessUser'


class Loanquotas(models.Model):
    loan = models.ForeignKey('Loans', models.DO_NOTHING, db_column='loan')
    date = models.DateField()
    # Field name made lowercase.
    paydate = models.DateField(db_column='payDate', blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    account = models.ForeignKey(
        Account, models.DO_NOTHING, db_column='account', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'LoanQuotas'


class Loans(models.Model):
    amount = models.FloatField()
    plan = models.IntegerField()
    interest = models.IntegerField()
    description = models.TextField()
    # Field name made lowercase.
    canceledquotas = models.IntegerField(db_column='canceledQuotas')
    authorized = models.IntegerField()
    # Field name made lowercase.
    usercui = models.ForeignKey(
        'Singleuser', models.DO_NOTHING, db_column='userCui', blank=True, null=True)
    # Field name made lowercase.
    userbusiness = models.ForeignKey(
        Businessuser, models.DO_NOTHING, db_column='userBusiness', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Loans'


class Monetaryaccount(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    description = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'MonetaryAccount'


class Providerspay(models.Model):
    # Field name made lowercase.
    payaccount = models.CharField(db_column='payAccount', max_length=6)
    # Field name made lowercase.
    payname = models.CharField(db_column='payName', max_length=20)
    amount = models.FloatField(blank=True, null=True)
    # Field name made lowercase.
    ismensualpayplan = models.BooleanField(db_column='isMensualPayPlan')
    # Field name made lowercase.
    userbusiness = models.ForeignKey(
        Businessuser, models.DO_NOTHING, db_column='userBusiness', blank=True, null=True)
    account = models.ForeignKey(
        Account, models.DO_NOTHING, db_column='account')

    class Meta:
        managed = False
        db_table = 'ProvidersPay'


class Savingaccount(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    interest = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SavingAccount'


class Singleuser(models.Model):
    cui = models.BigIntegerField(primary_key=True)
    nit = models.BigIntegerField()
    name = models.CharField(max_length=30)
    birth = models.DateField()
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    phone = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SingleUser'
        unique_together = (('cui', 'username'),)


class Spreadspay(models.Model):
    # Field name made lowercase.
    payaccount = models.CharField(db_column='payAccount', max_length=6)
    # Field name made lowercase.
    payname = models.CharField(db_column='payName', max_length=20)
    amount = models.FloatField(blank=True, null=True)
    # Field name made lowercase.
    ismensualpayplan = models.BooleanField(db_column='isMensualPayPlan')
    # Field name made lowercase.
    userbusiness = models.ForeignKey(
        Businessuser, models.DO_NOTHING, db_column='userBusiness', blank=True, null=True)
    account = models.ForeignKey(
        Account, models.DO_NOTHING, db_column='account')

    class Meta:
        managed = False
        db_table = 'SpreadsPay'


class Cards(models.Model):
    id = models.IntegerField(primary_key=True)
    brand = models.CharField(max_length=50, blank=True, null=True)
    # Field name made lowercase.
    credit = models.FloatField(db_column='credit')
    lowlimit = models.FloatField(db_column='lowLimit')
    highlimit = models.FloatField(db_column='highLimit')
    # Field name made lowercase.
    usercui = models.ForeignKey(
        'Singleuser', models.DO_NOTHING, db_column='userCui', blank=True, null=True)
    # Field name made lowercase.
    userbusiness = models.ForeignKey(
        Businessuser, models.DO_NOTHING, db_column='userBusiness', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Cards'


class Thirdaccount(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    # Field name made lowercase.
    usercui = models.ForeignKey(
        Singleuser, models.DO_NOTHING, db_column='userCui', blank=True, null=True)
    # Field name made lowercase.
    userbusiness = models.ForeignKey(
        Businessuser, models.DO_NOTHING, db_column='userBusiness', blank=True, null=True)
    # Field name made lowercase.
    thirdcui = models.BigIntegerField(
        db_column='thirdCui', blank=True, null=True)
    # Field name made lowercase.
    thirdbusiness = models.CharField(
        db_column='thirdBusiness', max_length=50, blank=True, null=True)
    # Field name made lowercase.
    accounttype = models.CharField(
        db_column='accountType', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ThirdAccount'


class Timedsavingaccount(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    interest = models.FloatField(blank=True, null=True)
    plan = models.DateField()

    class Meta:
        managed = False
        db_table = 'TimedSavingAccount'


class Transactions(models.Model):
    amount = models.FloatField()
    description = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField()
    # Field name made lowercase.
    originaccount = models.ForeignKey(
        Account, models.DO_NOTHING, db_column='originAccount')
    # Field name made lowercase.
    destaccount = models.CharField(db_column='destAccount', max_length=6)
    # Field name made lowercase.
    isthird = models.IntegerField(db_column='isThird')

    class Meta:
        managed = False
        db_table = 'Transactions'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
