from rest_framework import serializers
# ---
from Blog_app.models import PostRate


class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostRate
        fields = ("id", "post", "rate")