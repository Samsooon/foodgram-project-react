from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .models import Follow, User
from .pagination import CustomPageNumberPagination
from .serializers import (CustomUserCreateSerializer, CustomUserSerializer,
                          FollowSerializer, PasswordSerializer,
                          FollowerSerializer)


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
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        methods=["delete", "post"],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id):
        user = request.user
        following = get_object_or_404(User, pk=id)
        follow = Follow.objects.filter(user=user, following=following)
        data = {
            "user": user.id,
            "following": following.id,
        }
        serializer = FollowerSerializer(data=data, context=request)
        if request.method == "POST":
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_201_CREATED
                )
        if request.method == "DELETE":
            if serializer.is_valid(raise_exception=False):
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowListView(ListAPIView):
    """
    APIView for list view of subscription
    """
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return User.objects.filter(author__user=self.request.user)
