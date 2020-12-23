from django.db import models


class Account(models.Model):
    id = models.OneToOneField(
        'Accounttype', models.DO_NOTHING, db_column='id', primary_key=True)
    state = models.IntegerField()
    # Field name made lowercase.
    enablechecks = models.BooleanField(db_column='enableChecks')
    # Field name made lowercase.
    issingle = models.BooleanField(db_column='isSingle')
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

    class Meta:
        managed = False
        db_table = 'Account'


class Accountcheck(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    account = models.ForeignKey(
        Account, models.DO_NOTHING, db_column='account')

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


class Monetaryaccount(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    description = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'MonetaryAccount'


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


class Thirdaccount(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    # Field name made lowercase.
    usercui = models.ForeignKey(
        Singleuser, models.DO_NOTHING, db_column='userCui', blank=True, null=True)
    # Field name made lowercase.
    userbusiness = models.ForeignKey(
        Businessuser, models.DO_NOTHING, db_column='userBusiness', blank=True, null=True)
    # Field name made lowercase.
    thirdcui = models.CharField(
        db_column='thirdCui', max_length=13, blank=True, null=True)
    # Field name made lowercase.
    thirdbusiness = models.CharField(
        db_column='thirdBusiness', max_length=50, blank=True, null=True)

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
