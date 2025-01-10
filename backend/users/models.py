from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator, RegexValidator


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    email = models.EmailField('Электронная почта', unique=True,
                              max_length=254, blank=False,
                              null=False, validators=[EmailValidator()],)
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='''Введите корректный юзернейм.
                Разрешены буквы, цифры и символы: @ . + - _''',
            )
        ],
        error_messages={
            'unique': "Пользователь с таким юзернеймом уже существует.",
            'blank': "Это поле обязательно для заполнения.",
        }
    )

    first_name = models.CharField(
        'Имя',
        max_length=150,
        error_messages={
            'blank': "Это поле обязательно для заполнения.",
        }
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        error_messages={
            'blank': "Это поле обязательно для заполнения.",
        }
    )
    password = models.CharField(
        'Пароль',
        max_length=150,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE,
                               related_name='favorites', verbose_name='Рецепт')

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = 'избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='shopping_carts',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE,
                               related_name='shopping_carts',
                               verbose_name='Рецепт')

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = 'список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Пользователь')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='Автор')

    class Meta:
        unique_together = ('user', 'author')
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user.username} - {self.author.username}'
