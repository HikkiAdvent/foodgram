from django.contrib import admin

from recipes import models
from users.models import Favorite


class RecipeIngredientsInline(admin.TabularInline):
    model = models.RecipeIngredient
    extra = 1
    min_num = 1


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админка рецептов."""

    list_display = (
        'name',
        'author',
        'get_ingredients',
        'get_favorites_count',
    )
    inlines = (RecipeIngredientsInline,)
    search_fields = ('name', 'author')
    list_display_links = ('name',)
    list_filter = ('tags',)
    filter_horizontal = ('tags',)

    def get_favorites_count(self, obj):
        """Возвращает количество добавлений в избранное."""

        return Favorite.objects.filter(recipe=obj).count()

    get_favorites_count.short_description = 'В избранном'

    def get_ingredients(self, obj):
        """Возвращает строку с перечисленными ингредиентами."""

        return ', '.join(
            [ingredient.name for ingredient in obj.ingredients.all()]
        )
    get_ingredients.short_description = 'Ингредиенты'


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админка для ингредиентов."""

    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_editable = ('measurement_unit',)


@admin.register(models.Tag)
class TagAmin(admin.ModelAdmin):
    """Админка тегов."""

    list_display = ('name', 'slug')
    empty_value_display = 'пусто'
