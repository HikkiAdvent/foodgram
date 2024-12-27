from django.db import models


class Follower(models.Model):
    """Модель подписки пользователя на другого пользователя."""

    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE
    )
    followed_user = models.ForeignKey(
        'User',
        related_name='followed',
        on_delete=models.CASCADE,
        verbose_name='подписки'
    )

    class Meta:
        unique_together = ('user', 'followed_user')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.followed_user}'
