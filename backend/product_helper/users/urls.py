from django.urls import include, path
from rest_framework.routers import DefaultRouter
from djoser.views import (
    TokenCreateView, TokenDestroyView
)

from .views import CustomUserViewSet, FollowListView, FollowView

router_v1 = DefaultRouter()
router_v1.register('users', CustomUserViewSet, basename='users')


urlpatterns = [
    path('users/subscriptions/',
         FollowListView.as_view(),
         name='subscriptions'),
    path('users/<int:user_id>/subscribe/',
         FollowView.as_view(),
         name='subscribe'),
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/token/login/', TokenCreateView.as_view(), name='token_create'),
    path('auth/token/logout/', TokenDestroyView.as_view(), name='token_destroy')
]
