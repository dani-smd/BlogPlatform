from rest_framework import serializers
from User_app.models import User


class ShowUserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "email", "phone_number", "gender", "user_image")


class UpdateUserProfileParamsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    phone = serializers.IntegerField(required=False)
    gender = serializers.CharField(required=False)
    image = serializers.FileField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "phone", "gender", "image")