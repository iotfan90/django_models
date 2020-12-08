from abc import ABC

from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from .constant import *
from django.utils.six import text_type


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        self.user = authenticate(**{
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        })

        if self.user is None:
            raise serializers.ValidationError(ACCOUNT_NOT_FOUND)
        # if not self.user.is_active:
        #     raise serializers.ValidationError(EMAIL_NOT_VERIFIED)
        # if not self.user.is_phone_verified:
        #     raise serializers.ValidationError(PHONE_NOT_VERIFIED)

        refresh = self.get_token(self.user)

        return {
            'email': self.user.email,
            'refresh': text_type(refresh),
            'access': text_type(refresh.access_token),
        }


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active',
                  'phone_number', 'date_joined')


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()


class IDSerializer(serializers.ModelSerializer):

    class Meta:
        model = ID
        fields = ('id', 'id_name', 'id_type', 'id_role', 'id_entities', 'updated_at', 'status', 'info')


class CreateIDSerializer(serializers.Serializer):
    id_name = serializers.CharField()
    id_type = serializers.CharField()
    id_role = serializers.ListField()
    id_info = serializers.CharField()
    status = serializers.CharField()


class EntitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Entities
        fields = ('id', 'entity_id', 'entity_name', 'entity_type', 'start_date', 'end_date')


class CreateEntitySerializer(serializers.Serializer):
    entity_id = serializers.CharField()
    entity_name = serializers.CharField()
    entity_type = serializers.CharField()


class ModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = COAModel
        fields = ('id', 'model_name', 'status')


class CreateModelSerializer(serializers.Serializer):
    model_name = serializers.CharField()
    status = serializers.CharField()


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Accounts
        fields = ('id', 'account_id', 'description', 'info', 'account_type', 'sub_type', 'activity')


class CreateAccountSerializer(serializers.Serializer):
    account_id = serializers.CharField()
    description = serializers.CharField()
    info = serializers.CharField()
    account_type = serializers.CharField()
    sub_type = serializers.CharField()
    activity = serializers.CharField()


class JournalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Journals
        fields = ('id', 'journal_id', 'journal_name', 'info', 'avail_entities')


class CreateJournalSerializer(serializers.Serializer):
    journal_id = serializers.CharField()
    journal_name = serializers.CharField()
    info = serializers.CharField()
    avail_entities = serializers.CharField()


class PlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plans
        fields = ('id', 'plan_id', 'type', 'info', 'total', 'rows', 'year')


class CreatePlanSerializer(serializers.Serializer):
    plan_id = serializers.CharField()
    type = serializers.CharField()
    info = serializers.CharField()
    total = serializers.CharField()
    rows = serializers.CharField()
    year = serializers.CharField()

