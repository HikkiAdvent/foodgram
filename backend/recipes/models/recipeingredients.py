from django.db import models


class RecipeIngredient(models.Model):
    "Модель состава блюда."

    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'состав'

    def __str__(self):
        return (
            f'{self.recipe.name}:'
            f'{self.ingredient.name} - '
            f'{self.quantity}{self.ingredient.measurement_unit}'
        )
