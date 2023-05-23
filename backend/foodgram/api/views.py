from api.serializers import IngredientSerializer
from api.viewsets import ListRetriveViewSet
from recipes.models import Ingredient
from rest_framework import filters


class IngredientViewSet(ListRetriveViewSet):
    """Ингредиенты."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
