from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import generics, status
from .models import User, Following, Tweet

from app.models import Tweet, Following
from app.serializers import TweetSerializer, FollowingSerializer


class TweetViewSet(ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer


class FollowingListCreateApiView(generics.ListCreateAPIView):
    queryset = Following.objects.all()
    serializer_class = FollowingSerializer


class FeedsApiView(APIView):
    @staticmethod
    def get(request):

        # todo - to handle pagination

        user_id = request.query_params.get('user_id')
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
