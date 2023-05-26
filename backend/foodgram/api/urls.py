from django.urls import include, path
from rest_framework import routers

from api.views import (CustomUserViewSet, IngredientViewSet, RecipeViewSet,
                       TagViewSet, favorite)

router_v1 = routers.DefaultRouter()

router_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')
router_v1.register(r'tags', TagViewSet, basename='tags')
router_v1.register(r'users', CustomUserViewSet)
router_v1.register(r'recipes', RecipeViewSet, basename='recipes')

function_urls = [
    path('recipes/<int:recipe_id>/favorite/', favorite, name='favorite'),
]

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include(function_urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
