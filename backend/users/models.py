from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from foodgram_backend.constants import USER_CHARFIELD_LENGTH
from users.mixins import UserRecipeMixin
from users.validators import me_validator


class User(AbstractUser):
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )
    email = models.EmailField(
        'Электронная почта',
        unique=True,
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=USER_CHARFIELD_LENGTH,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message=(
                    'Введите корректный юзернейм. '
                    'Разрешены буквы, цифры и символы: @ . + - _'
                )
            ),
            me_validator
        ],
        error_messages={
            'unique': 'Пользователь с таким юзернеймом уже существует.',
            'blank': 'Это поле обязательно для заполнения.',
        }
    )
    first_name = models.CharField(
        'Имя',
        max_length=USER_CHARFIELD_LENGTH,
        error_messages={
            'blank': "Это поле обязательно для заполнения.",
        }
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=USER_CHARFIELD_LENGTH,
        error_messages={
            'blank': 'Это поле обязательно для заполнения.',
        }
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']


class Favorite(UserRecipeMixin):
    class Meta(UserRecipeMixin.Meta):
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingCart(UserRecipeMixin):
    class Meta(UserRecipeMixin.Meta):
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author_%(class)s'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='prevent_self_subscription'
            )
        ]
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user.username} - {self.author.username}'
