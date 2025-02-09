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
        if request:
            if request.user.is_authenticated:
                return Subscription.objects.filter(
                    user=request.user,
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


class RecipeIngredientRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()


class RecipeRequestSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientRequestSerializer(
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()
    author = UserProfileSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags',
                  'ingredients', 'author',
                  'name', 'text',
                  'cooking_time', 'image',)

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            author=self.context['request'].user,
            **validated_data
        )
        recipe.tags.set(tags_data)
        self.add_ingredients_to_recipe(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        """Обновление рецепта."""
        tags_data = validated_data.pop('tags', [])
        ingredients_data = validated_data.pop('ingredients', [])
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.image = validated_data.get('image', instance.image)
        if tags_data:
            instance.tags.set(tags_data)
        if ingredients_data:
            self.add_ingredients_to_recipe(instance, ingredients_data)
        instance.save()
        return instance

    def add_ingredients_to_recipe(self, recipe, ingredients_data):
        """Добавляет или обновляет ингредиенты для рецепта."""
        ingredient_ids = [ingredient['id'] for ingredient in ingredients_data]
        ingredients = Ingredient.objects.filter(id__in=ingredient_ids)
        ingredient_dict = (
            {ingredient.id: ingredient for ingredient in ingredients}
        )
        recipe.ingredients.clear()
        recipe_ingredients = [
            RecipeIngredient(
                recipe=recipe,
                ingredients=ingredient_dict[ingredient_data['id']],
                amount=ingredient_data['amount']
            )
            for ingredient_data in ingredients_data
            if ingredient_data['id'] in ingredient_dict
        ]
        RecipeIngredient.objects.bulk_create(recipe_ingredients)

    def validate_tags(self, value):
        if not value or not isinstance(value, list):
            raise serializers.ValidationError(
                {'tags': 'Поле tags не может быть пустым'})
        if len(value) != len(set(value)):
            raise serializers.ValidationError(
                {'tags': 'Теги не могут повторяться'})
        invalid_tags = [tag_id for tag_id in value
                        if not Tag.objects.filter(id=tag_id.id).exists()]
        if invalid_tags:
            invalid_tags_str = ', '.join(map(str, invalid_tags))
            raise serializers.ValidationError(
                {'tags': f'Теги с id {invalid_tags_str} не существуют'})
        return value

    def validate_ingredients(self, value):
        if value is None:
            raise serializers.ValidationError(
                {'ingredients': 'Поле ingredients отсутствует'})
        if not isinstance(value, list) or not value:
            raise serializers.ValidationError(
                {'ingredients': 'Поле ingredients не может быть пустым'})

        ingredient_ids = set()
        for ingredient in value:
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
            return value

    def to_representation(self, instance):
        return (
            RecipeResponseSerializer(context=self.context)
            .to_representation(instance)
        )


class RecipeResponseSerializer(serializers.ModelSerializer):
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


class RecipeSubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(UserProfileSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserProfileSerializer.Meta):
        fields = (
            UserProfileSerializer.Meta.fields + ('recipes', 'recipes_count')
        )
        read_only_fields = fields

    def get_recipes_count(self, obj):
        """Получить количество рецептов пользователя."""
        return obj.recipes.count()

    def get_recipes(self, obj):
        """Получить рецепты пользователя с учетом лимита."""
        print(self.context)
        request = self.context['request']
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit is not None:
            try:
                recipes_limit = int(recipes_limit)
            except ValueError:
                recipes_limit = None
        recipes = obj.recipes.all()
        if recipes_limit:
            recipes = recipes[:recipes_limit]
        return RecipeSubscribeSerializer(recipes, many=True).data

    def validate(self, data):
        user = self.context['request'].user
        author_id = int(self.context['pk'])
        try:
            author_user = User.objects.get(id=author_id)
        except User.DoesNotExist:
            raise serializers.ValidationError('Такого автора нет.')
        if user.id == author_id:
            raise serializers.ValidationError(
                'Вы не можете подписаться на себя.'
            )
        if Subscription.objects.filter(
            user=user,
            author=author_user
        ).exists():
            raise serializers.ValidationError('Вы уже подписаны на автора.')
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        author = User.objects.get(id=int(self.context['pk']))
        subscription = Subscription.objects.create(user=user, author=author)
        return subscription.author
