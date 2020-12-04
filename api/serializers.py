from abc import ABC

from .models import User, ID
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

