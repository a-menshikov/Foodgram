from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe


class RecipeFilter(filters.FilterSet):
    """Фильтрсет для фильтрации рецептов."""

    is_favorited = filters.Filter(field_name='is_favorited')
    is_in_shopping_cart = filters.Filter(field_name='is_in_shopping_cart')
    author = filters.Filter(field_name='author__id')
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = [
            'is_favorited',
            'is_in_shopping_cart',
            'author',
            'tags',
        ]


class IngredientFilter(filters.FilterSet):
    """Фильтрсет для фильтрации ингредиентов."""
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)
