from rest_framework import serializers
# ---
from Comment_app.models import Comments


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"


class CommentParamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ("post", "content")


class CommentUpdateParamsSerializer(serializers.ModelSerializer):
    comment_id = serializers.IntegerField()

    class Meta:
        model = Comments
        fields = ("comment_id", "content")
