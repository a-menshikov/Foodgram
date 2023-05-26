from django.urls import include, path
from rest_framework import routers

from api.views import (CustomUserViewSet, IngredientViewSet,
                       ListSubscribeViewSet, RecipeViewSet, TagViewSet,
                       download_shopping_cart, favorite, shopping, subscribe)

router_v1 = routers.DefaultRouter()

router_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')
router_v1.register(r'tags', TagViewSet, basename='tags')
router_v1.register(r'users/subscriptions', ListSubscribeViewSet,
                   basename='get_subscribe')
router_v1.register(r'users', CustomUserViewSet)
router_v1.register(r'recipes', RecipeViewSet, basename='recipes')

function_urls = [
    path('recipes/download_shopping_cart/', download_shopping_cart,
         name='download_shopping_cart'),
    path('recipes/<int:recipe_id>/favorite/', favorite, name='favorite'),
    path('users/<int:user_id>/subscribe/', subscribe, name='subscribe'),
    path('recipes/<int:recipe_id>/shopping_cart/', shopping, name='shopping'),

]

urlpatterns = [
    path('', include(function_urls)),
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
