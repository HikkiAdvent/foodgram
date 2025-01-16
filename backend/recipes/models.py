import random
import re
import string

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.timezone import now
from django.forms import ValidationError

User = get_user_model()


class Tag(models.Model):
    name = models.CharField('Название', max_length=32, unique=True)
    slug = models.SlugField('Слаг', max_length=32, unique=True)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def clean(self):
        if self.slug and not re.match(r'^[a-zA-Z0-9_-]+$', self.slug):
            raise ValidationError({'slug': '''Slug должен содержать только
                                   буквы цифры, дефисы и подчеркивания.'''})

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=128, unique=True)
    measurement_unit = models.CharField('Единица измерения', max_length=64)

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes', verbose_name='Автор')
    name = models.CharField('Название', max_length=256)
    image = models.ImageField('Картинка', upload_to='recipes/images/')
    text = models.TextField('Текст')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient',
                                         verbose_name='Ингредиенты')
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    cooking_time = models.PositiveIntegerField(
        'Время приготовления', validators=[
            MinValueValidator(
                1, 'Время приготовления не должно быть меньше 1 минуты'
            )
        ])
    pub_date = models.DateTimeField(
        default=now,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name

    def get_favorites_count(self):
        return self.favorites.count()


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_ingredients',
                               verbose_name='Рецепт')
    ingredients = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                    related_name='recipe_ingredients',
                                    verbose_name='Ингредиент')
    amount = models.PositiveIntegerField(
        'Количество', default=1, validators=[MinValueValidator(
            1, 'Количество ингредиентов не может быть меньше 1'
        )])

    class Meta:
        verbose_name = 'ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        return f'{self.recipe} - {self.ingredients.name}'


class ShortLink(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE)
    short_code = models.CharField(max_length=10, unique=True)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = self.generate_short_code()
        super().save(*args, **kwargs)

    def generate_short_code(self):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=10))
