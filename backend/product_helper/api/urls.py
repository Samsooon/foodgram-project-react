from django.urls import include, path
from rest_framework.routers import DefaultRouter
from recipes.views import IngredientsViewSet, TagViewSet, RecipeViewSet


router_v1 = DefaultRouter()
router_v1.register('recipes', RecipeViewSet, basename='recipe')
router_v1.register('ingredients', IngredientsViewSet, basename='ingredients')
router_v1.register('tags', TagViewSet, basename='tags')

urlpatterns = [
   # path(
   #    "recipes/<int:recipe_id>/favorite/",
   #    FavoriteViewSet.as_view(),
   # ),
   path('', include(router_v1.urls)),
]
