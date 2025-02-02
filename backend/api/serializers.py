from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.fields import Base64ImageField
from recipes.models import Ingredient, Recipe, RecipeIngredient, ShortLink, Tag
from users.models import Favorite, ShoppingCart, Subscription

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name', 'password')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Электронная почта уже существует.'
            )
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Имя пользователя уже существует.'
            )
        if value.lower() == 'me':
            raise serializers.ValidationError(
                f'Никней не может быть {value}'
            )
        return value

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name', 'avatar')


class UserProfileSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    avatar = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'is_subscribed',
                  'first_name', 'last_name', 'avatar')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return Subscription.objects.filter(
                user=self.context.get('request').user,
                author=obj
            ).exists()
        return False


class AvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=True)

    class Meta:
        model = User
        fields = ('avatar',)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class ShortLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortLink
        fields = ('recipe', 'short_code')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer()

    class Meta:
        model = RecipeIngredient
        fields = ('ingredients', 'amount')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        ingredient_data = representation.pop('ingredients')
        return {
            'id': ingredient_data['id'],
            'name': ingredient_data['name'],
            'measurement_unit': ingredient_data['measurement_unit'],
            'amount': representation['amount']
        }

    def validate_amount(self, value):
        try:
            value = int(value)
        except ValueError:
            raise serializers.ValidationError(
                'Количество должно быть целым числом'
            )
        if value < 1:
            raise serializers.ValidationError(
                'Количество ингредиентов не может быть меньше 1'
            )
        return value


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(read_only=True, many=True,
                                             source='recipe_ingredients')
    tags = TagSerializer(read_only=True, many=True)
    image = Base64ImageField()
    author = UserProfileSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags',
                  'ingredients', 'author',
                  'name', 'text',
                  'cooking_time', 'image',
                  'is_favorited', 'is_in_shopping_cart')

    def validate_tags(self):
        tags_data = self.context['request'].data.get('tags')
        if not tags_data or not isinstance(tags_data, list):
            raise serializers.ValidationError(
                {'tags': 'Поле tags не может быть пустым'})
        if len(tags_data) != len(set(tags_data)):
            raise serializers.ValidationError(
                {'tags': 'Теги не могут повторяться'})
        invalid_tags = [tag_id for tag_id in tags_data
                        if not Tag.objects.filter(id=tag_id).exists()]
        if invalid_tags:
            invalid_tags_str = ', '.join(map(str, invalid_tags))
            raise serializers.ValidationError(
                {'tags': f'Теги с id {invalid_tags_str} не существуют'})

    def validate_ingredients(self):
        ingredients_data = self.context['request'].data.get('ingredients')
        if ingredients_data is None:
            raise serializers.ValidationError(
                {'ingredients': 'Поле ingredients отсутствует'})
        if not isinstance(ingredients_data, list) or not ingredients_data:
            raise serializers.ValidationError(
                {'ingredients': 'Поле ingredients не может быть пустым'})

        ingredient_ids = set()
        for ingredient in ingredients_data:
            ingredient_id = ingredient.get('id')
            amount = ingredient.get('amount')
            try:
                amount = int(amount)
            except (ValueError, TypeError):
                raise serializers.ValidationError(
                    {'ingredients':
                     'Количество ингредиента должно быть целым числом'}
                )

            if amount < 1:
                raise serializers.ValidationError(
                    {'ingredients':
                     'Количество ингредиента должно быть больше 0'}
                )

            if ingredient_id in ingredient_ids:
                raise serializers.ValidationError(
                    {'ingredients':
                     f'Ингредиент с id {ingredient_id} уже добавлен'}
                )
            ingredient_ids.add(ingredient_id)

            if not Ingredient.objects.filter(id=ingredient_id).exists():
                raise serializers.ValidationError(
                    {'ingredients':
                     f'Ингредиент с id {ingredient_id} не найден'}
                )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return Favorite.objects.filter(
                user=request.user,
                recipe=obj
            ).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return ShoppingCart.objects.filter(
                user=request.user,
                recipe=obj).exists()
        return False


class SetPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        user = self.context['request'].user
        current_password = attrs.get('current_password')
        if not user.check_password(current_password):
            raise serializers.ValidationError('Текущий пароль неверен.')
        return attrs

    def save(self):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()


class RecipeSubscribeSerializer(serializers.Serializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(UserProfileSerializer):
    recipes = RecipeSubscribeSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserProfileSerializer.Meta):
        model = User
        fields = (
            UserProfileSerializer.Meta.fields
            + ('recipes', 'recipes_count')
        )

    def get_recipes_count(self, obj):
        """Получить количество рецептов пользователя."""
        return obj.recipes.count()

    def validate(self, data):
        """Проверка, не подписан ли пользователь на самого себя."""
        user = self.context['request'].user
        author = self.instance
        if user.id == author.id:
            raise serializers.ValidationError(
                'Вы не можете подписаться на себя.'
            )
        if not User.objects.filter(id=author.id).exists():
            raise serializers.ValidationError('Такого автора нет.')
        if Subscription.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError('Вы уже подписаны на автора.')
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        recipes_limit = (
            self.context.get('request')
            .query_params.get('recipes_limit', None)
        )
        recipes_limit = (
            int(recipes_limit)
            if recipes_limit is not None else None
        )
        if recipes_limit:
            recipes = instance.recipes.all()[:recipes_limit]
        else:
            recipes = instance.recipes.all()
        representation['recipes'] = RecipeSubscribeSerializer(
            recipes,
            many=True
        ).data
        return representation

    def create(self, validated_data):
        """Переопределение метода для создания подписки"""
        user = self.context['request'].user
        author = validated_data.get('author')
        subscription = Subscription.objects.create(user=user, author=author)
        return subscription
