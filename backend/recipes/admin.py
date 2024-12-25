from django.contrib import admin

from recipes.models.recipes import Recipe
from recipes.models.recipeingredients import RecipeIngredient
from recipes.models.ingredients import Ingredient
from recipes.models.tags import Tag


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админка рецептов."""

    list_display = (
        'name',
        'author',
    )
    inlines = (RecipeIngredientsInline,)
    search_fields = ('name', 'author')
    list_display_links = ('name',)
    list_filter = ('tags',)
    filter_horizontal = ('tags',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админка для ингредиентов."""
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_editable = ('measurement_unit',)


@admin.register(Tag)
class TagAmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    empty_value_display = 'пусто'
