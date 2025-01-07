from rest_framework import viewsets

from api.v1.recipes.serializers import (
    RecipesSerializer, IngredientSerializer, TagSerializer
)
from api.v1.recipes.mixins import CRUDMixin
from recipes.models.recipes import Recipe
from recipes.models.ingredients import Ingredient
from recipes.models.tags import Tag


class RecipeViewSet(CRUDMixin):
    queryset = Recipe.objects.prefetch_related(
        'tags',
        'ingredients',
    ).all()
    serializer_class = RecipesSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
