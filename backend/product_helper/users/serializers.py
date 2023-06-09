from djoser.serializers import (
    UserCreateSerializer,
    UserSerializer,
    TokenCreateSerializer
)
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from recipes.models import Recipes
from .models import Follow, User


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Create user serializer
    """
    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['first_name'],
            password=make_password(validated_data.get('password'))
        )
        user.save
        return user


class CustomUserSerializer(UserSerializer):
    """
    User serializer
    """
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, following=obj.id).exists()


class ShortRecipeSerializer(serializers.ModelSerializer):
    """
    Recipe for Follow Serializer
    """
    class Meta:
        model = Recipes
        fields = ('id', 'image', 'name', 'cooking_time')


class FollowSerializer(CustomUserSerializer):
    """
    User subscribes list serilalizer
    """
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed',
                  'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return ShortRecipeSerializer(recipes, many=True).data


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = "__all__"


class FollowerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    following = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        fields = ("user", "following")
        model = Follow

    def validate(self, data):
        method = self.context.method
        user = data.get('user')
        following = data.get('following')
        if method == 'DELETE':
            if not Follow.objects.filter(
                user=user,
                following=following
            ).exists:
                print("Aaaaaaa")
                raise serializers.ValidationError(
                    'You not subscribed to this user'
                )
        # print(method)
        if method == 'POST':
            if user == following:
                raise serializers.ValidationError(
                    'You cant subscribe to yourself.'
                )
            if Follow.objects.filter(
                    user=data['user'],
                    following=data['following']
            ).exists():
                raise serializers.ValidationError(
                    'You have already subscribed to this user.'
                )
        return data


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        user = authenticate(
            email=attrs.get("email"),
            password=attrs.get("password")
        )
        if not user:
            raise serializers.ValidationError(
                "Unable to log in with provided credentials."
            )
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")
        attrs["user"] = user
        return attrs


class CustomTokenCreateSerializer(TokenCreateSerializer):
    def __init__(self, *args, **kwargs):
        super(CustomTokenCreateSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        user = validated_data['user']
        tokens = user.auth_tokens.filter(is_active=True)
        if tokens.exists():
            tokens.delete()

        token = Token.objects.create(user=user)
        return {"auth_token": token.key}
