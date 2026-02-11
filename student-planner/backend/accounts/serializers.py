from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model=User
        fields=['id','username','email','password']

    def create(self, validated_data):
        user= User.objects.create_user(**validated_data)
        # UserProfile.objects.create(user=user)
        return user

class OTPVerifySerailizer(serializers.Serializer):
    username=serializers.CharField()
    otp= serializers.CharField(max_length=6)