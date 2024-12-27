from django.db import models


class Favorite(models.Model):
    """Модель для связи пользователя с его избранными рецептами."""

    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        related_name='favorited',
        verbose_name='рецепт',
    )

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = 'Израбранное'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в избранное'
