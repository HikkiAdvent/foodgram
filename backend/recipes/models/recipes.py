from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Recipe(models.Model):
    """Модель рецептов."""

    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=256,
        verbose_name='название'
    )
    text = models.TextField(
        verbose_name='описание'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='время приготовления',
        help_text='Время приготовления в минутах.'
    )
    image = models.ImageField(
        upload_to='image/',
        verbose_name='изображение',
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='теги'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        verbose_name='ингредиенты'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        default_related_name = 'recipe'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name

    def clean_cooking_time(self):
        if self.cooking_time < 1:
            raise ValidationError(
                {'cooking_time':
                 'Время приготовления не может быть меньше 1 минуты.'}
            )
        return self.cooking_time
