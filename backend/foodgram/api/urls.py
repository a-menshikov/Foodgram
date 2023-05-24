from rest_framework import routers
from django.urls import include, path
from api.views import IngredientViewSet, TagViewSet

router_v1 = routers.DefaultRouter()

router_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')
router_v1.register(r'tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(router_v1.urls)),
]
