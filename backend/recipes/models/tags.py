from django.db import models


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        max_length=32,
        verbose_name='тэг',
        unique=True
    )
    slug = models.SlugField(
        max_length=32,
        unique=True,
        null=True,
        blank=True
    )
