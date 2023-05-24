from api.serializers import IngredientSerializer, TagSerializer
from api.viewsets import ListRetriveViewSet
from recipes.models import Ingredient, Tag
from rest_framework import filters


class IngredientViewSet(ListRetriveViewSet):
    """Ингредиенты."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class TagViewSet(ListRetriveViewSet):
    """Теги."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
