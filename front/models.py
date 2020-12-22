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
    credit = models.IntegerField()
    debit = models.IntegerField()
    # Field name made lowercase.
    isdollar = models.IntegerField(db_column='isDollar')
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
    amount = models.IntegerField(blank=True, null=True)
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
    interest = models.TextField(blank=True, null=True)

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
    interest = models.TextField(blank=True, null=True)
    plan = models.DateField()

    class Meta:
        managed = False
        db_table = 'TimedSavingAccount'


class Transactions(models.Model):
    amount = models.IntegerField()
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


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        'DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


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
