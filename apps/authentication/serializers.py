from typing import Any

from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.services import generate_jwt_token

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    """
    login serializer. Using username and password
    """
    username_field = get_user_model().USERNAME_FIELD
    password = serializers.CharField(write_only=True)

    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField(write_only=True)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """
        validate username and password. generate token
        :param attrs:
        :return: attrs
        """
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
            "request": self.context["request"]
        }

        user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(user):
            raise exceptions.AuthenticationFailed()

        token_obj = generate_jwt_token(user)

        return {
            'access_token': str(token_obj.access_token),
            'refresh_token': str(token_obj),
        }


class RegisterSerializer(serializers.ModelSerializer):
    """
    Register serializer to create user and generate JWT tokens for the user
    """
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            'password',
            'first_name',
            'last_name',
            'phone_number',
            'access_token',
            'refresh_token',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_phone_number(self, value) -> str:
        if User.objects.filter(phone_number=value).exists():
            raise ValidationError("This phone number is already registered.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        # Generate JWT tokens
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        validated_data['access_token'] = str(refresh.access_token)
        validated_data['refresh_token'] = str(refresh)

        return user


class CustomTokenRefreshSerializer(serializers.Serializer):
    """
    Custom token refresh serializer to return access token with refresh token
    """
    refresh_token = serializers.CharField()
    access_token = serializers.CharField(read_only=True)

    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        refresh_token = RefreshToken(attrs["refresh_token"])
        return {
            "access_token": str(refresh_token.access_token)
        }
