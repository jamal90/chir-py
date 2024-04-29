from rest_framework import serializers

from app.models import Tweet, Following
from django.contrib.auth.models import User
import bleach


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class TweetSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(write_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'content', 'created_at', 'user_id', 'user']

    def create(self, validated_data):
        user_id = validated_data.pop('user_id', None)
        user = User.objects.get(pk=user_id)
        return Tweet.objects.create(**validated_data, user=user)

    @staticmethod
    def validate_content(value):
        if not value:
            raise serializers.ValidationError("Content cannot be empty")
        if len(value) < 2:
            raise serializers.ValidationError("Content cannot be less than 2 characters")

        # todo: make it configurable from external config service (consider using consul for configuration store
        if len(value) > 1024:
            raise serializers.ValidationError("Content cannot be more than 1024 characters")

        sanitized_content = bleach.clean(value,
                                         tags=['p', 'b', 'i', 'u', 'strong', 'em', 'a'],
                                         attributes={'a': ['href', 'title']})
        return sanitized_content


class FollowingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    following = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Following
        fields = ['id', 'user', 'following', 'created_at']
