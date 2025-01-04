from django.db import models


class RecipeIngredient(models.Model):
    "Модель состава блюда."

    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='рецепт'
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        verbose_name='ингредиенты'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='количество'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return (
            f'Рецепт {self.recipe.name}: '
            f'{self.ingredient.name} - '
            f'{self.amount}{self.ingredient.measurement_unit}'
        )
