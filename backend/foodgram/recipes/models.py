from colorfield.fields import ColorField
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    """Ингредиент."""

    name = models.CharField(
        'Название ингредиента',
        unique=True,
        max_length=200,
        )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200,
        )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['id']

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """Тег."""

    name = models.CharField(
        'Название тега',
        unique=True,
        max_length=200,
        )
    color = ColorField(
        'Цвет',
        unique=True,
        default='#FFFFFF',
        # я добавил валидацию через регулярку, но насколько я понял из
        # документации colorfield он сам валидирует поле как цвет в
        # шестнадцатиричной системе по умолчанию. Возможно понял неправильно.
        # Поле max_length не добавляю - думаю оно избыточно.
        # Все комментарии, естественно, позже удалю)
        validators=[
            RegexValidator(
                regex=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Некорректный формат цвета'),
            ],
        max_length=7,
        )
    slug = models.SlugField(
        'Slug тега',
        unique=True,
        max_length=200,
        )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['id']

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    """Рецепт"""

    name = models.CharField(
        'Название рецепта',
        unique=True,
        max_length=200,
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name="Автор рецепта",
        )
    image = models.ImageField(
        'Фото блюда',
        upload_to='backend-media/recipes/images/',
        )
    text = models.TextField(
        'Рецепт',
        )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name="Ингредиенты",
        through='IngredientRecipe',
        )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Теги",
        through='TagRecipe',
        )
    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(1,
                              "Время не может быть менее 1 минуты"
                              ),
            ],
        verbose_name="Время приготовления, мин"
        )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
        )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    """Ингредиенты в рецепте."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        )
    amount = models.IntegerField(
        validators=[
            MinValueValidator(1,
                              "Количество должно быть числом более 1"
                              )
            ]
        )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_recipe_ingredient',
            ),
        )

    def __str__(self):
        return f"{self.ingredient} для {self.recipe}"


class TagRecipe(models.Model):
    """Связь тега и рецепта."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'tag'),
                name='unique_recipe_tag',
            ),
        )

    def __str__(self):
        return f"{self.tag} для {self.recipe}"


class Follow(models.Model):
    """Подписки на пользователей."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Фолловер',
        )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_follow',
                )
        ]

    def __str__(self) -> str:
        return f'{self.user} подписан на автора {self.following}'


class Favorite(models.Model):
    """Избранные рецепты."""

    recipe = models.ForeignKey(
        Recipe,
        related_name='favorite_recipe',
        on_delete=models.CASCADE
        )

    user = models.ForeignKey(
        User,
        related_name='favorite_user',
        on_delete=models.CASCADE
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user', ],
                name='unique_favorite'
            )
        ]
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self) -> str:
        return f'{self.recipe} в избранном у {self.user}'


class ShoppingList(models.Model):
    """Список покупок."""
    recipe = models.ForeignKey(
        Recipe,
        related_name='shopping_recipe',
        on_delete=models.CASCADE
        )

    user = models.ForeignKey(
        User,
        related_name='shopping_user',
        on_delete=models.CASCADE
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user', ],
                name='unique_shopping_list'
            )
        ]
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списке покупок'

    def __str__(self) -> str:
        return f'{self.recipe} в списке покупок у {self.user}'
