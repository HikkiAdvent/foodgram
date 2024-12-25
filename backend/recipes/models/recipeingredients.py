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
