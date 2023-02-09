"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
)
from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from drf_spectacular.utils import extend_schema_field


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'password', 'username']
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True,
                                     'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'name']
        read_only_fields = ['id']


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': _('Email lub hasło jest błędne')
    }
