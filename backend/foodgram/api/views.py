from api.serializers import (CustomUserSerializer, IngredientSerializer,
                             TagSerializer)
from api.viewsets import ListRetriveViewSet
from djoser.conf import settings
from djoser.views import UserViewSet
from recipes.models import Ingredient, Tag
from rest_framework import filters
from users.models import User
from rest_framework.decorators import action


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


class CustomUserViewSet(UserViewSet):
    """Пользователи."""
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_serializer_class(self):
        if self.action == "create":
            if settings.USER_CREATE_PASSWORD_RETYPE:
                return settings.SERIALIZERS.user_create_password_retype
            return settings.SERIALIZERS.user_create
        if self.action == "set_password":
            if settings.SET_PASSWORD_RETYPE:
                return settings.SERIALIZERS.set_password_retype
            return settings.SERIALIZERS.set_password
        return self.serializer_class

    @action(["get"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)
