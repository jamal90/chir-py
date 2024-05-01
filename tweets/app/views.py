from django.db.models import Prefetch, Case, When
from django.forms import BooleanField
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import generics, status

from app.models import User, Tweet, Following
from app.serializers import TweetSerializer, FollowingSerializer, UserFollowingSerializer


class TweetViewSet(ModelViewSet):
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tweet.objects.filter(user__id=self.request.user.id).all()


class FollowingListCreateApiView(generics.ListCreateAPIView):
    serializer_class = FollowingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Following.objects.filter(user__id=self.request.user.id).all()


class UserFollowingListApiView(generics.ListCreateAPIView):
    serializer_class = UserFollowingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        logged_in_user = self.request.user

        # exclude the current user from the list
        users_list = User.objects.exclude(user__id=self.request.user.id)

        return users_list.annotate(
            is_following=Case(
                When(followers__user=logged_in_user, then=True),
                default=False,
                output_field=BooleanField()
            )
        )


class FeedsApiView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        # todo - to handle pagination

        user_id = request.user.id
        if user_id is None:
            return Response({'error': 'user_id is missing'}, status=status.HTTP_400_BAD_REQUEST)

        # get the user ids followed by the current user
        following_ids = Following.objects.filter(user__id=user_id).values_list('following_id', flat=True)

        # top 20 tweets from followed users
        tweets = Tweet.objects.filter(user__id__in=following_ids).order_by('-id')[:20]

        # Use Prefetch to optimize the query
        tweets = Tweet.objects.prefetch_related(
            Prefetch('user', queryset=User.objects.filter(id__in=following_ids))
        ).filter(id__in=tweets).order_by('-id')

        serialized = TweetSerializer(tweets, many=True)
        return Response(serialized.data)
