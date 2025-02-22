import random
import string
import typing as t
from email.utils import formataddr
from django.db import transaction
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..models import UserEmail

SIGNUP_CODE = 'saas:signup_code'

ERRORS = {
    "email": _("This email address is already associated with an existing account."),
    "username": _("This username is already associated with an existing account."),
    "code": _("Code does not match or expired."),
}


class EmailCode:
    def __init__(self, email: str, code: str, user=None):
        self.email = email
        self.code = code
        self.user = user

    def recipient(self):
        if self.user:
            return formataddr((self.user.username, self.email))
        return self.email


class SignupRequestCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email: str):
        try:
            UserEmail.objects.get(email=email)
            raise ValidationError(ERRORS["email"])
        except UserEmail.DoesNotExist:
            return email

    def create(self, validated_data) -> EmailCode:
        email = validated_data["email"]
        code = ''.join(random.sample(string.ascii_uppercase, 6))
        cache_key = f"{SIGNUP_CODE}:{email}:{code}"
        cache.set(cache_key, 1, timeout=300)
        return EmailCode(email, code)


class SignupCreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, validators=[UnicodeUsernameValidator()])
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email: str):
        try:
            UserEmail.objects.get(email=email)
            raise ValidationError(ERRORS["email"])
        except UserEmail.DoesNotExist:
            return email

    def validate_username(self, username: str):
        cls: t.Type[User] = get_user_model()
        try:
            cls.objects.get(username=username)
            raise ValidationError(ERRORS["username"])
        except cls.DoesNotExist:
            return username

    def validate_password(self, raw_password: str):
        user = User(
            username=self.initial_data["username"],
            email=self.initial_data["email"],
        )
        password_validation.validate_password(raw_password, user)
        return raw_password

    def create(self, validated_data) -> EmailCode:
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        cls: t.Type[User] = get_user_model()
        with transaction.atomic():
            user = cls.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=False,
            )
            UserEmail.objects.create(user=user, email=email, primary=True, verified=False)

        code = ''.join(random.sample(string.ascii_uppercase, 6))
        cache_key = f"{SIGNUP_CODE}:{email}:{code}"
        cache.set(cache_key, 1, timeout=300)
        return EmailCode(email, code, user)


class SignupConfirmCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True, max_length=6)

    def validate_code(self, code: str):
        email = self.initial_data["email"]
        code = code.upper()
        cache_key = f"{SIGNUP_CODE}:{email}:{code}"
        has_code: str = cache.get(cache_key)
        if not has_code:
            raise ValidationError(ERRORS["code"])

        cache.delete(cache_key)
        try:
            return UserEmail.objects.select_related('user').get(email=email)
        except UserEmail.DoesNotExist:
            raise ValidationError(ERRORS["code"])

    def create(self, validated_data) -> User:
        user_email = validated_data["code"]
        with transaction.atomic():
            user_email.verified = True
            user = user_email.user
            user.is_active = True
            user_email.save()
            user.save()
        return user


class SignupConfirmPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, validators=[UnicodeUsernameValidator()])
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True, max_length=6)
    password = serializers.CharField(required=True)

    def validate_username(self, username: str):
        cls: t.Type[User] = get_user_model()
        try:
            cls.objects.get(username=username)
            raise ValidationError(ERRORS["username"])
        except cls.DoesNotExist:
            return username

    def validate_password(self, raw_password: str):
        password_validation.validate_password(raw_password)
        return raw_password

    def validate_code(self, code: str):
        email = self.initial_data["email"]
        code = code.upper()
        cache_key = f"{SIGNUP_CODE}:{email}:{code}"
        has_code: str = cache.get(cache_key)
        if not has_code:
            raise ValidationError(ERRORS["code"])
        return code

    def create(self, validated_data) -> User:
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        cls: t.Type[User] = get_user_model()
        with transaction.atomic():
            user = cls.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=True,
            )
            UserEmail.objects.create(user=user, email=email, primary=True, verified=True)

        code = validated_data["code"]
        cache_key = f"{SIGNUP_CODE}:{email}:{code}"
        cache.delete(cache_key)
        return user
