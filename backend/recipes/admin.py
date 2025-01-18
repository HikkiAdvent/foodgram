from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from recipes import models


class RecipeAdminForm(forms.ModelForm):
    favorites_count = forms.IntegerField(
        label='Добавления в избранное',
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    class Meta:
        model = models.Recipe
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['favorites_count'].initial = (
                self.instance.get_favorites_count()
            )


class RecipeIngredientsInline(admin.TabularInline):
    model = models.RecipeIngredient
    extra = 1


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админка рецептов."""

    form = RecipeAdminForm
    list_display = (
        'name',
        'author',
        'get_ingredients'
    )
    inlines = (RecipeIngredientsInline,)
    search_fields = ('name', 'author')
    list_display_links = ('name',)
    list_filter = ('tags',)
    filter_horizontal = ('tags',)

    def save_related(self, request, form, formsets, change):
        """Проверяем, что рецепт содержит хотя бы один ингредиент."""

        super().save_related(request, form, formsets, change)
        if not form.instance.ingredients.exists():
            raise ValidationError(
                'Рецепт должен содержать хотя бы один ингредиент.'
            )

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
