from django.db import models


class ShoppingList(models.Model):
    """Модель для списка покупок пользователя."""

    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        'recipes.Ingredient',
        on_delete=models.CASCADE,
        related_name='shopping_lists',
        verbose_name='ингредиенты'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество'
    )
    measurement_unit = models.CharField(
        max_length=64,
        verbose_name='Единица измерения',
        blank=True, null=True
    )

    class Meta:
        unique_together = ('user', 'ingredient')
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return (
            f'{self.user.username} - '
            f'{self.ingredient.name}: {self.quantity}'
        )

    def save(self, *args, **kwargs):
        if not self.measurement_unit and self.ingredient:
            self.measurement_unit = self.ingredient.measurement_unit
        super().save(*args, **kwargs)
