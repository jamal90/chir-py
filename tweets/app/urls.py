from django.urls import path, include
from rest_framework import routers
from .views import TweetViewSet, FollowingListCreateApiView, FeedsApiView, UserFollowingListApiView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'v1/tweets', TweetViewSet, basename='tweets')

urlpatterns = [
    path('', include(router.urls)),
    path('v1/followings', FollowingListCreateApiView.as_view(), name='followings'),
    path('v1/feeds', FeedsApiView.as_view(), name='feeds'),
    path('v1/user-followings', UserFollowingListApiView.as_view(), name='user-followings'),
]