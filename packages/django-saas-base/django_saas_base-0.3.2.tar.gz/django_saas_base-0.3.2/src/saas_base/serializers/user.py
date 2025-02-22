from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import password_validation
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..models import UserEmail


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ['password', 'groups', 'user_permissions']


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEmail
        exclude = ['user']


class UserPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate_password(self, raw_password: str):
        if self.initial_data["confirm_password"] != raw_password:
            raise ValidationError("Password does not match.")
        password_validation.validate_password(raw_password)
        return raw_password

    def update(self, user: AbstractUser, validated_data):
        raw_password = validated_data["password"]
        user.set_password(raw_password)
        user.save()
        return user
