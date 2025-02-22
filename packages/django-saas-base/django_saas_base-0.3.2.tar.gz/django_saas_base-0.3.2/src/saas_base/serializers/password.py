import random
import string
import typing as t
from django.utils.translation import gettext as _
from django.core.cache import cache
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..models import UserEmail

CACHE_PREFIX = 'saas:password_code'


class PasswordLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    @staticmethod
    def invalid_errors():
        errors = {"password": [_("Invalid username or password.")]}
        return ValidationError(errors)

    @staticmethod
    def get_user(username: str):
        cls: t.Type[AbstractUser] = get_user_model()
        try:
            return cls.objects.get(username=username)
        except cls.DoesNotExist:
            if '@' not in username:
                return None
            try:
                obj = UserEmail.objects.select_related("user").get(email=username)
                if obj.verified and obj.primary:
                    return obj.user
            except UserEmail.DoesNotExist:
                return None
        return None

    def create(self, validated_data):
        user = self.get_user(validated_data["username"])
        if not user:
            raise self.invalid_errors()

        password = validated_data["password"]
        if user.check_password(password):
            return user
        raise self.invalid_errors()

    def update(self, instance, validated_data):
        raise RuntimeError("This method is not allowed.")


class PasswordForgetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    @staticmethod
    def save_password_code(obj: UserEmail) -> str:
        code = ''.join(random.sample(string.ascii_uppercase, 6))
        key = f"{CACHE_PREFIX}:{obj.email}:{code}"
        cache.set(key, obj.user_id, timeout=300)
        return code

    def create(self, validated_data) -> UserEmail:
        email = validated_data["email"]
        try:
            obj = UserEmail.objects.get(email=email)
        except UserEmail.DoesNotExist:
            raise ValidationError({"email": [_("Invalid email address.")]})
        return obj


class PasswordResetSerializer(PasswordForgetSerializer):
    code = serializers.CharField(required=True, max_length=6)
    password = serializers.CharField(required=True)

    def validate_password(self, raw_password):
        password_validation.validate_password(raw_password)
        return raw_password

    def create(self, validated_data):
        obj = super().create(validated_data)

        code = validated_data["code"]
        key = f"{CACHE_PREFIX}:{obj.email}:{code}"
        user_id = cache.get(key)
        if not user_id or obj.user_id != user_id:
            raise ValidationError({"code": [_("Code does not match or expired.")]})

        raw_password = validated_data['password']
        user: AbstractUser = obj.user
        user.set_password(raw_password)
        user.save()

        cache.delete(key)
        return obj
