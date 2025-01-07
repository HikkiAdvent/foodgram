from django.db import models


class ShoppingList(models.Model):
    """Модель для списка покупок пользователя."""

    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )
    recipes = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        related_name='shopping_lists',
        verbose_name='рецепты'
    )

    class Meta:
        unique_together = ('user', 'recipes')
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return (
            f'{self.user.username} - '
            f'{self.recipes.name}'
        )
