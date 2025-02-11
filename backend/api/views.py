from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import Ingredient, Recipe, RecipeIngredient, ShortLink, Tag
from users.models import Favorite, ShoppingCart, Subscription
from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    AvatarSerializer, IngredientSerializer,
    RecipeRequestSerializer, RecipeResponseSerializer, SetPasswordSerializer,
    TagSerializer, UserListSerializer,
    UserProfileSerializer, UserRegistrationSerializer,
    SubscribeSerializer, ShortRecipeSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        if self.action in ('retrieve', 'me'):
            return UserProfileSerializer
        if self.action == 'subscriptions':
            return SubscribeSerializer
        return UserRegistrationSerializer

    def get_queryset(self):
        if self.action == 'subscriptions':
            user = self.request.user
            return User.objects.filter(following__user=user)
        return User.objects.all()

    @action(
        detail=False,
        methods=['get'],
        url_path='me',
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        serializer = self.get_serializer_class()(user)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['post'],
        url_path='set_password',
        permission_classes=[permissions.IsAuthenticated]
    )
    def set_password(self, request):
        serializer = SetPasswordSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=204)

    @action(
        detail=False,
        methods=['put'],
        url_path='me/avatar',
        permission_classes=[permissions.IsAuthenticated],
    )
    def upload_avatar(self, request):
        """Обновление аватара пользователя."""
        serializer = AvatarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.avatar = serializer.validated_data['avatar']
        user.save()
        avatar_url = request.build_absolute_uri(
            user.avatar.url) if user.avatar else None
        return Response({"avatar": avatar_url},
                        status=status.HTTP_200_OK)

    @upload_avatar.mapping.delete
    def delete_avatar(self, request):
        """Удаление аватара пользователя."""
        user = request.user
        if user.avatar:
            user.avatar.delete(save=False)
            user.avatar = None
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            "detail": "Аватар не найден."},
            status=status.HTTP_404_NOT_FOUND)

    @action(
        detail=True,
        methods=['post'],
        url_path='subscribe',
        permission_classes=[permissions.IsAuthenticated]
    )
    def add_subscription(self, request, pk=None):
        """Добавление подписки на пользователя"""
        serializer = SubscribeSerializer(
            data=request.data,
            context={
                'request': request,
                'pk': pk
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @add_subscription.mapping.delete
    def remove_subscription(self, request, pk=None):
        """Удаление подписки от пользователя"""
        author = self.get_object()
        user = request.user
        subscription = Subscription.objects.filter(
            user=user,
            author=author
        )
        if subscription.exists():
            subscription.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {'detail': 'Вы не подписаны на этого пользователя.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False,
        methods=['get'],
        url_path='subscriptions',
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscriptions(self, request):
        return self.list(request)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (
        IsAuthorOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return RecipeRequestSerializer
        return RecipeResponseSerializer

    def _add_relation(self, request, recipe, model):
        """Вспомогательная функция для добавления связи."""
        user = request.user
        relation, created = model.objects.get_or_create(
            user=user,
            recipe=recipe
        )
        if created:
            serializer = ShortRecipeSerializer(
                recipe, context={'request': request}
            )
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            {'detail': 'Рецепт уже добавлен в список.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def _remove_relation(self, request, recipe, model):
        """Вспомогательная функция для удаления связи."""
        user = request.user
        relation = model.objects.filter(user=user, recipe=recipe)
        if relation.exists():
            relation.delete()
            return Response(
                {'detail': 'Рецепт удален из списка.'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {'detail': 'Рецепт не найден в списке.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def _handle_relation(
            self,
            request,
            model,
            action_type,
    ):
        """Функция для обработки действий избранного/корзины."""
        recipe = self.get_object()
        if action_type == 'add':
            return self._add_relation(request, recipe, model)
        elif action_type == 'remove':
            return self._remove_relation(request, recipe, model)
        return Response(
            {'detail': 'Неверный тип действия'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=True,
        methods=['get'],
        url_path='get-link'
    )
    def create_short_link(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        short_link, created = ShortLink.objects.get_or_create(recipe=recipe)
        short_url = request.build_absolute_uri(
            f'/api/recipes/links/{short_link.short_code}/'
        )
        return Response({'short-link': short_url}, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post'],
        url_path='shopping_cart',
        permission_classes=[permissions.IsAuthenticated]
    )
    def add_to_shopping_cart(self, request, pk=None):
        """Добавление рецепта в корзину покупок."""
        return self._handle_relation(request, ShoppingCart, 'add')

    @add_to_shopping_cart.mapping.delete
    def remove_from_shopping_cart(self, request, pk=None):
        """Удаление рецепта из корзины покупок."""
        return self._handle_relation(request, ShoppingCart, 'remove')

    @action(
        detail=True,
        methods=['post'],
        url_path='favorite',
        permission_classes=[permissions.IsAuthenticated]
    )
    def add_to_favorite(self, request, pk=None):
        """Добавление рецепта в избранное."""
        return self._handle_relation(request, Favorite, 'add',)

    @add_to_favorite.mapping.delete
    def remove_from_favorite(self, request, pk=None):
        """Удаление рецепта из избранного."""
        return self._handle_relation(request, Favorite, 'remove')

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart',
    )
    def download_shopping_cart(self, request):
        shopping_cart_items = ShoppingCart.objects.filter(user=request.user)
        ingredients_data = self._get_ingredients_data(shopping_cart_items)
        ingredients_text = self._generate_ingredients_text(ingredients_data)
        response = HttpResponse(
            ingredients_text,
            content_type='text/plain'
        )
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.txt"'
        )
        return response

    def _get_ingredients_data(self, shopping_cart_items):
        """Получить данные об ингредиентах из корзины."""
        return (
            RecipeIngredient.objects
            .filter(recipe__in=[item.recipe for item in shopping_cart_items])
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(total_amount=Sum('amount'))
            .order_by('ingredient__name')
        )

    def _generate_ingredients_text(self, ingredients_data):
        """Генерация текстового списка покупок из данных ингредиентов."""
        ingredients_text = 'Список покупок:\n\n'
        for ingredient in ingredients_data:
            ingredient_name = ingredient['ingredient__name']
            measurement_unit = ingredient['ingredient__measurement_unit']
            total_amount = ingredient['total_amount']
            ingredients_text += (
                f'{ingredient_name} ({measurement_unit}) - {total_amount}\n'
            )
        return ingredients_text


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter
    pagination_class = None
