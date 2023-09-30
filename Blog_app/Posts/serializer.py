from rest_framework import serializers
# ---
from Blog_app.models import Posts


class PostParamsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False)
    content = serializers.CharField(required=False)
    auther = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Posts
        fields = ("id", "title", "content", "auther")