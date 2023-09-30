from rest_framework import serializers
from User_app.models import User


class RegisterUserParamsSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()
    phone = serializers.IntegerField()
    gender = serializers.CharField()
    image = serializers.FileField()

    class Meta:
        model = User
        fields = ("username", "password", "email", "phone", "gender", "image")


class LoginUserParamsSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ("username", "password")


class UserForgotPasswordParamsSerializer(serializers.ModelSerializer):
    phone = serializers.IntegerField()
    token = serializers.CharField(required=False)
    new_password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ("phone", "token", "new_password")


class CheckTokenParamsSerializer(serializers.ModelSerializer):
    phone = serializers.IntegerField()
    token = serializers.CharField()

    class Meta:
        model = User
        fields = ("phone", "token")


class UserResetPasswordParamsSerializer(serializers.ModelSerializer):
    old_password = serializers.IntegerField()
    new_password = serializers.CharField()

    class Meta:
        model = User
        fields = ("old_password", "new_password")
