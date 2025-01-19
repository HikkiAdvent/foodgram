from django.db import models


class UserRecipeMixin(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='%(class)ss'
    )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='%(class)ss'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'
