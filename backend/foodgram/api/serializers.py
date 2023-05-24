from rest_framework import serializers
from recipes.models import Ingredient, Tag
import re


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""
    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    def validate_slug(self, value):
        """Проверка соответствия слага тега."""
        if not re.fullmatch(r'^[-a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                'Slug тега не соотвествует формату',
            )
        return value

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag
