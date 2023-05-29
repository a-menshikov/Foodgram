import base64
import re

from django.core.files.base import ContentFile
from djoser.serializers import UserSerializer
from recipes.models import (Favorite, Follow, Ingredient, IngredientRecipe,
                            Recipe, ShoppingList, Tag)
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from users.models import User


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        fields = (
            'id',
            'name',
            'measurement_unit',
            )
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
        fields = (
            'id',
            'name',
            'color',
            'slug',
            )
        model = Tag


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователя."""

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            )
        model = User


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов в рецепте для чтения."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
        )

    class Meta:
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
            )
        model = IngredientRecipe


class IngredientRecipeWriteSerializer(serializers.Serializer):
    """Сериализатор ингредиентов в рецепте для записи."""

    id = serializers.IntegerField()
    amount = serializers.IntegerField(min_value=1)


class Base64ImageField(serializers.ImageField):
    """Поле изображения."""

    def to_internal_value(self, data):
        """Декодирует изображение."""
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта."""

    is_favorited = serializers.BooleanField(read_only=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = IngredientRecipeSerializer(source='ingredientrecipe_set',
                                             many=True, read_only=True)

    class Meta:
        exclude = ('pub_date',)
        model = Recipe


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта для записи."""

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = CustomUserSerializer(
        read_only=True, default=CurrentUserDefault())
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField()
    ingredients = IngredientRecipeWriteSerializer(
        many=True,
        source='ingredientinrecipe_set',
    )

    class Meta:
        exclude = ('pub_date',)
        read_only_fields = (
            'author',
            )
        model = Recipe

    def get_is_favorited(self, obj):
        """Проверить на избранное."""
        return Favorite.objects.filter(user=self.context['request'].user,
                                       recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """Проверить на список покупок."""
        return ShoppingList.objects.filter(user=self.context['request'].user,
                                           recipe=obj).exists()

    def to_representation(self, instance):
        """Изменение представления."""
        serializer = RecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
            )
        return serializer.data

    def _add_ingredients(self, recipe, ingredients):
        """Добавить список ингредиентов рецепта."""
        data = []
        for ingredient in ingredients:
            data.append(IngredientRecipe(
                recipe=recipe,
                ingredient_id=ingredient['id'],
                amount=ingredient['amount']
            ))
        IngredientRecipe.objects.bulk_create(data)

    def create(self, validated_data):
        """Создание нового объекта."""
        ingredients = validated_data.pop('ingredientinrecipe_set')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            recipe.tags.add(tag)
        self._add_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        """Редактирование объекта."""
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)
        ingredients = validated_data.pop('ingredientinrecipe_set')
        tags = validated_data.pop('tags')
        tags_lst = []
        for tag in tags:
            tags_lst.append(tag)
        instance.tags.set(tags_lst)
        instance.ingredients.clear()
        instance.save()
        self._add_ingredients(instance, ingredients)
        return instance


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор избранного."""

    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
            )
        model = Favorite

    def validate(self, data):
        """Валидация данных."""
        if (self.context['request'].method == "POST"
                and Favorite.objects.filter(
                    user=self.context['request'].user,
                    recipe_id=self.context['recipe_id']
        ).exists()):
            raise serializers.ValidationError(
                'Вы уже добавили в избранное!'
            )
        return data


class RecipeShortSerializer(serializers.ModelSerializer):
    """Упрощённый сериализатор рецепта"""
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    image = serializers.ImageField(read_only=True)
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""

    email = serializers.ReadOnlyField(source='following.email')
    id = serializers.ReadOnlyField(source='following.id')
    username = serializers.ReadOnlyField(source='following.username')
    first_name = serializers.ReadOnlyField(source='following.first_name')
    last_name = serializers.ReadOnlyField(source='following.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            )
        model = Follow

    def validate(self, data):
        """Валидация данных."""
        if self.context['request'].method == "POST" and Follow.objects.filter(
                user=self.context['request'].user,
                following_id=self.context['user_id']
        ).exists():
            raise serializers.ValidationError(
                'Такая подписка уже есть.'
            )
        if (self.context['request'].method == "POST"
                and self.context['request'].user.id
                == self.context['user_id']):
            raise serializers.ValidationError(
                'На себя нельзя подписаться.'
            )
        if (self.context['request'].method == "DELETE" and not
            Follow.objects.filter(
                user=self.context['request'].user,
                following_id=self.context['user_id']
        ).exists()):
            raise serializers.ValidationError(
                'Такой подписки нет.'
            )
        return data

    def get_recipes(self, obj):
        """Получить связанные рецепты."""
        recipes_limit = self.context['request'].query_params.get(
            'recipes_limit'
        )
        queryset = obj.following.recipes.all()
        if recipes_limit:
            queryset = queryset[:int(recipes_limit)]
        serializer = RecipeShortSerializer(queryset, many=True)
        return serializer.data

    def get_is_subscribed(self, obj):
        """Проверить подписку."""
        return Follow.objects.filter(user=self.context['request'].user,
                                     following=obj.following).exists()

    def get_recipes_count(self, obj):
        """Получить счетчит рецептов."""
        return obj.following.recipes.count()


class ShoppingCardSerializer(serializers.ModelSerializer):
    """Сериализатор списка покупок."""

    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = ShoppingList

    def validate(self, data):
        """Валидация данных."""
        if (self.context['request'].method == "POST"
                and ShoppingList.objects.filter(
                    user=self.context['request'].user,
                    recipe_id=self.context['recipe_id']
        ).exists()):
            raise serializers.ValidationError(
                'Уже добавлен в список покупок.'
            )
        return data
