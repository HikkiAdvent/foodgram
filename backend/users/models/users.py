from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя."""

    subscriptions = models.ManyToManyField(
        'User',
        through='Follower',
    )
    favorites = models.ManyToManyField(
        'recipes.Recipe',
        through='Favorite'
    )
    shopping_list = models.ManyToManyField(
        'recipes.Ingredient',
        through='ShoppingList'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
