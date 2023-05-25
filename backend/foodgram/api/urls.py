from api.views import (CustomUserViewSet, IngredientViewSet, RecipeViewSet,
                       TagViewSet)
from django.urls import include, path
from rest_framework import routers

router_v1 = routers.DefaultRouter()

router_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')
router_v1.register(r'tags', TagViewSet, basename='tags')
router_v1.register(r'users', CustomUserViewSet)
router_v1.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
