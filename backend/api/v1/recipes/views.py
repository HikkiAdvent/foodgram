from rest_framework import generics, viewsets

from api.v1.recipes.serializers import RecipesSerializer
from recipes.models.recipes import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.prefetch_related('tags', 'ingredients').all()
    serializer_class = RecipesSerializer
