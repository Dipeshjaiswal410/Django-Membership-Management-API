from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'phone_number', 'membership_type', 'membership_start_date', 'membership_expiry_date')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'phone_number', 'password', 'password_confirmation', 'membership_type')

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation', None)
        password = validated_data.pop('password')
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(phone_number=data['phone_number'], password=data['password'])
        if not user:
            raise AuthenticationFailed('Invalid credentials')
        
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }

class MembershipExpiryDateSerializer(serializers.ModelSerializer):
    membership_expiry_date = serializers.DateField()

    class Meta:
        model = CustomUser  
        fields = ('membership_expiry_date',)  

