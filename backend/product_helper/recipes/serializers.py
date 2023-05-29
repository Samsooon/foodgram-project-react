from .models import (Recipes, Tag, Ingredient,
                     RecipesIngredient, Favorite, ShoppingCart)
from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.serializers import CustomUserSerializer, ShortRecipeSerializer
import base64

from django.core.files.base import ContentFile

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    """
    Image Serializer.
    """
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('id', 'name', 'color', 'slug')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for geting an amount of ingredients
    """
    id = serializers.ReadOnlyField(
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipesIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for Ingredients.
    """
    class Meta:
        model = Ingredient
        fields = ('__all__')


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Serializer for favorites list
    """
    class Meta:
        model = Favorite
        fields = ('recipe', 'user')

    def validate(self, data):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipe = data['recipe']
        if Favorite.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            raise serializers.ValidationError({
                'error': 'Recipe already in favorites'
            })
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShortRecipeSerializer(
            instance.recipe, context=context).data


class AddIngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for adding Ingredients to Recipe.
    """
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = RecipesIngredient
        fields = ('id', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):
    """
    Serializer to display recipes
    """
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_ingredients(self, obj):
        queryset = RecipesIngredient.objects.filter(recipe=obj)
        return [{'id': item.id, 'name': item.ingredient.name,
                 'measurement_unit': item.ingredient.measurement_unit,
                 'amount': item.amount} for item in queryset]

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """
    Adding Recipe Serializers.
    """
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = AddIngredientSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipes
        fields = ('id', 'author',
                  'ingredients', 'tags',
                  'image', 'name',
                  'text', 'cooking_time')

    def validate(self, data):
        ingredients = data['ingredients']
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError({
                    'ingredients': 'Ingredients should be unique'
                })
            ingredients_list.append(ingredient_id)
            amount = ingredient['amount']
            if int(amount) <= 0:
                raise serializers.ValidationError({
                    'amount': 'amount can not to be negative'
                })
        tags = data['tags']
        if not tags:
            raise serializers.ValidationError({
                'tags': 'Need to be at least one tag'
            })
        tag_list = []
        for tag in tags:
            if tag in tag_list:
                raise serializers.ValidationError({
                    'tags': 'tag should be unique'
                })
            tag_list.append(tag)
        cooking_time = data['cooking_time']
        if int(cooking_time) <= 0:
            raise serializers.ValidationError({
                'cooking_time': 'cooking time can not to be negative'
            })
        return data

    def create_tags(self, tags, recipe):
        for tag in tags:
            recipe.tags.add(tag)

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            RecipesIngredient.objects.create(
                recipe=recipe, ingredient=ingredient['id'],
                amount=ingredient['amount']
            )

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipes.objects.create(author=author, **validated_data)
        self.create_tags(tags, recipe)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def to_representation(self, instance):  # -
        request = self.context.get('request')
        context = {'request': request}
        return RecipeListSerializer(instance, context=context).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """
    Serializer for shopping list
    """
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShortRecipeSerializer(
            instance.recipe, context=context).data
