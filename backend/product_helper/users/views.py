from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Follow, User
from .pagination import CustomPageNumberPagination
from .serializers import (CustomUserCreateSerializer, CustomUserSerializer,
                          FollowSerializer, PasswordSerializer)


class CustomUserViewSet(UserViewSet):
    """
    ViewSet for users
    """
    queryset = User.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomUserCreateSerializer
        return CustomUserSerializer

    @action(
        methods=["get"], detail=False, permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.user is None:
            return Response(
                {'error': 'user no authorised'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = get_object_or_404(User, pk=request.user.id)
        serializer = CustomUserSerializer(user, context={'request': request})
        return Response(serializer.data)

    @action(["post"], detail=False)
    def set_password(self, request, *args, **kwargs):
        user = self.request.user
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response({"status": "password set"})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class FollowView(APIView):
    """
    APIView for add and delete subscription for author
    """
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, user_id):
        # user_id = self.kwargs.get()
        if user_id == request.user.id:
            return Response(
                {'error': 'You can not subscribe for yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Follow.objects.filter(
            user=request.user,
            following_id=user_id
        ).exists():
            return Response(
                {'error': 'You already subscribed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Follow.objects.create(
            user=request.user,
            following_id=user_id
        )
        return Response(
            self.serializer_class(
                get_object_or_404(User, id=user_id),
                context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, user_id):
        subscription = Follow.objects.filter(
            user=request.user,
            following_id=user_id,
        )
        if subscription.exists():
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'You not subscribed on this user'},
            status=status.HTTP_400_BAD_REQUEST
        )


class FollowListView(ListAPIView):
    """
    APIView for list view of subscription
    """
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return User.objects.filter(author__user=self.request.user)
