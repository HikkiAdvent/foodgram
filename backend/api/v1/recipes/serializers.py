from rest_framework import serializers

from recipes.models.recipes import Recipe
from recipes.models.ingredients import Ingredient
from recipes.models.recipeingredients import RecipeIngredient


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""

    class Meta:
        model = 'recipes.Ingredient'
        fields = ('id', 'amount')


class RecipesSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов."""

    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = 'recipes.Recipe'
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingredients:
            current_ingredient, status = Ingredient.objects.get_or_create(
                **ingredient)
            RecipeIngredient.objects.create(
                achievement=current_ingredient, recipe=recipe)
        return recipe
