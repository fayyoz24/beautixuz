# users/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
import re

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_phone_number(self, value):
        value = value.strip()
        if not re.match(r'^\+998\d{9}$', value):
            raise serializers.ValidationError("Phone number must start with +998 and be exactly 13 characters.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
