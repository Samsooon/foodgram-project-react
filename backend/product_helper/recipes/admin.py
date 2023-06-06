from django.contrib import admin

from .models import (Favorite, Ingredient, Recipes, RecipesIngredient,
                     RecipesTag, Tag)


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author',
                    'amount_favorites', 'amount_tags',
                    'amount_ingredients')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-empty-'

    def amount_favorites(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    def amount_tags(self, obj):
        return ([i[0] for i in obj.tags.values_list('name')])

    def amount_ingredients(self, obj):
        return ([i[0] for i in obj.ingredients.values_list('name')])


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)
    empty_value_display = '-empty-'


admin.site.register(Tag)
admin.site.register(RecipesTag)
admin.site.register(RecipesIngredient)
