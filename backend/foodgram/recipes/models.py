from django.db import models
from colorfield.fields import ColorField


class Ingredient(models.Model):
    """Ингредиент."""
    name = models.CharField('Название ингредиента', unique=True,
                            max_length=200)
    measurement_unit = models.CharField('Единица измерения', max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['id']

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """Тег."""
    name = models.CharField('Название тега', unique=True,
                            max_length=200)
    color = ColorField('Цвет', unique=True, default='#FF0000')
    slug = models.SlugField('Slug тега', unique=True,
                            max_length=200)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['id']

    def __str__(self):
        return f'{self.name}'
