from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from recipes.models.recipes import Recipe
from recipes.models.ingredients import Ingredient
from recipes.models.recipeingredients import RecipeIngredient
from recipes.models.tags import Tag
from api.v1.recipes.fields import (
    Base64ImageField, RecipeIngredientCreateSerializer,
    RecipeIngredientSerializer
)

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тэгов."""

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipesSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов."""

    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=User.objects.get(username='admin'),
    )
    ingredients = RecipeIngredientCreateSerializer(
        many=True,
        write_only=True
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def get_is_favorited(self, obj):
        return obj in User.objects.get(username='valerij').favorites.all()  # self.context['request'].user.favorites.all()

    def get_is_in_shopping_cart(self, obj):
        return obj in User.objects.get(username='valerij').shopping_list.all()  # self.context['request'].user.shopping_list.all()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['tags'] = TagSerializer(
            instance.tags.all(),
            many=True
        ).data
        data['ingredients'] = RecipeIngredientSerializer(
            instance.recipeingredient_set.all(),
            many=True
        ).data
        return data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            current_ingredient = get_object_or_404(
                Ingredient,
                id=ingredient.get('id')
            )
            RecipeIngredient.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=ingredient.get('amount')
            )
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.image = validated_data.get('image', instance.image)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.tags.set(tags)
        RecipeIngredient.objects.filter(recipe=instance).delete()
        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(id=ingredient['id'])
            RecipeIngredient.objects.create(
                ingredient=current_ingredient,
                recipe=instance,
                amount=ingredient['amount']
            )
        instance.save()
        return instance


class ShoppingListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка покупок"""

