
from accounts.models import Task
from django.contrib.auth import models
from rest_framework import fields, serializers
from rest_framework.serializers import Serializer
from django.contrib.auth.models import User


class UserSearlizers(serializers.ModelSerializer):
    username=serializers.CharField(max_length=200)
    password=serializers.CharField(max_length=200)

    email=serializers.EmailField(max_length=200)
    class Meta:
        model=User
        fields=["username","email","password"]
    def validate(self, attrs):
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(
                {'email':("Email Already in use")}
            )
        if User.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError(
                {'username':("Username Already in use")}
            )
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ['username', 'password']
        
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields="__all__"