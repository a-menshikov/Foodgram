from django.contrib import admin
from recipes.models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Панель администратора для ингредиентов."""
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_filter = ('name', )
