from django.db import models


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        max_length=32,
        verbose_name='тег',
        unique=True
    )
    slug = models.SlugField(
        max_length=32,
        unique=True,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
