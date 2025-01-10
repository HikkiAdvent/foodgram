from django.contrib import admin

from recipes import models


class RecipeIngredientsInline(admin.TabularInline):
    model = models.RecipeIngredient
    extra = 1


@admin.register(models.Recipe)
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


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админка для ингредиентов."""
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_editable = ('measurement_unit',)


@admin.register(models.Tag)
class TagAmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    empty_value_display = 'пусто'
