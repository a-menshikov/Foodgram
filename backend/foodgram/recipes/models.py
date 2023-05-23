from django.db import models


class Ingredient(models.Model):
    """Ингредиенты."""
    name = models.CharField('Название ингредиента', unique=True,
                            max_length=200)
    measurement_unit = models.CharField('Единица измерения', max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'
