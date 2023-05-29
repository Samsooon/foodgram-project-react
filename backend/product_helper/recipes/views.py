from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from .models import (Recipes, Ingredient, Tag,
                     Favorite, ShoppingCart, RecipesIngredient)
from .serializers import (IngredientSerializer, TagSerializer,
                          FavoriteSerializer, RecipeCreateSerializer,
                          RecipeListSerializer, ShoppingCartSerializer)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPageNumberPagination
from .permissions import IsAuthorOrReadOnly


class IngredientsViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    viewsets.GenericViewSet
):
    """
    APIView for Ingredients.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = [IngredientFilter, ]
    search_fields = ('^name',)


class TagViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    viewsets.GenericViewSet
):
    """
    APIView for Tags.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Complex ViewSet for recipes.
    """
    queryset = Recipes.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeCreateSerializer

    @staticmethod
    def post_method_actions(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method_actions(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipes, id=pk)
        model_obj = get_object_or_404(model, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.post_method_actions(
                request=request,
                pk=pk,
                serializers=FavoriteSerializer
            )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_method_actions(
            request=request,
            pk=pk,
            model=Favorite
        )

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.post_method_actions(
                request=request,
                pk=pk,
                serializers=ShoppingCartSerializer
            )
        if request.method == 'DELETE':
            return self.delete_method_actions(
                request=request,
                pk=pk,
                model=ShoppingCart
            )

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        return_dict = {}
        ingredients = RecipesIngredient.objects.filter(
            recipe__carts__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit', 'amount'
        )
        for item in ingredients:
            name = item[0]
            if name not in return_dict:
                return_dict[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
                }
            else:
                return_dict[name]['amount'] += item[2]
        pdfmetrics.registerFont(
            TTFont('Handicraft', 'data/Handicraft.ttf', 'UTF-8')
        )
        response = HttpResponse(content_type='applications/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.pdf"')
        page = canvas.Canvas(response)
        page.setFont('Helvetica', size=30)
        page.drawString(200, 800, 'Shopping list')
        page.setFont('Handicraft', size=20)
        height = 750
        for i, (name, data) in enumerate(return_dict.items(), 1):
            page.drawString(75, height, (f'{i}. {name} - {data["amount"]} '
                                         f'{data["measurement_unit"]}'))
            height -= 25

        page.showPage()
        page.save()
        return response
