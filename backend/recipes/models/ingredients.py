from django.db import models


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        max_length=128,
        verbose_name='ингредиент'
    )
    measurement_unit = models.CharField(
        max_length=64,
        verbose_name='единица измерения'
    )
