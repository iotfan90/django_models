from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=30, blank=True)
    otp = models.CharField(max_length=30, blank=True)
    email_verification_code = models.CharField(max_length=10, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    class Meta:
        db_table = 'users'


class ID(models.Model):
    id_name = models.CharField(max_length=30, blank=True)
    id_type = models.CharField(max_length=30, blank=True)
    id_role = models.CharField(max_length=30, blank=True)
    id_entities = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    status = models.CharField(max_length=30, blank=True)
    info = models.CharField(max_length=200)

    class Meta:
        db_table = 'id'


class Entities(models.Model):
    entity_id = models.CharField(max_length=50, blank=True)
    entity_name = models.CharField(max_length=30, blank=True)
    entity_type = models.CharField(max_length=30, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'entities'


class COAModel(models.Model):
    model_name = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=30, null=True)

    class Meta:
        db_table = 'coa_model'


class Accounts(models.Model):
    account_id = models.CharField(max_length=30, null=True)
    description = models.CharField(max_length=200, null=True)
    info = models.CharField(max_length=500, null=True)
    account_type = models.CharField(max_length=30, null=True)
    sub_type = models.CharField(max_length=30, null=True)
    activity = models.CharField(max_length=30, null=True)

    class Meta:
        db_table = 'accounts'


class Journals(models.Model):
    journal_id = models.CharField(max_length=30, null=True)
    journal_name = models.CharField(max_length=100, null=True)
    info = models.CharField(max_length=500, null=True)
    avail_entities = models.CharField(max_length=30, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'journals'


class Plans(models.Model):
    plan_id = models.CharField(max_length=30, null=True)
    type = models.CharField(max_length=100, null=True)
    total = models.CharField(max_length=30, null=True)
    rows = models.CharField(max_length=30, null=True)
    year = models.CharField(max_length=30, null=True)
    info = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'plans'


class TransIDs(models.Model):
    trans_num = models.CharField(max_length=30, null=True)
    trans_user = models.CharField(max_length=30, null=True)
    type = models.CharField(max_length=30, null=True)
    reference = models.CharField(max_length=30, null=True)
    version = models.CharField(max_length=30, null=True)
    status = models.CharField(max_length=30, null=True)
    amount = models.CharField(max_length=30, null=True)
    debit = models.CharField(max_length=30, null=True)
    credit = models.CharField(max_length=30, null=True)
    info = models.TextField(blank=True, null=True)
    entity = models.CharField(max_length=30, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'trans_ids'


class TransTypes(models.Model):
    type = models.CharField(max_length=30, null=True)
    financial = models.CharField(max_length=30, null=True)
    journals = models.CharField(max_length=30, null=True)
    info = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'trans_types'


class ContactInfo(models.Model):
    contact_id = models.CharField(max_length=30, null=True)
    name = models.CharField(max_length=30, null=True)
    title = models.CharField(max_length=30, null=True)
    type = models.CharField(max_length=30, null=True)
    value = models.CharField(max_length=30, null=True)
    location = models.CharField(max_length=30, null=True)
    info = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'contact_info'
