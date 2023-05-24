from django.contrib import admin
from recipes.models import Ingredient, Tag


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Панель администратора для ингредиентов."""
    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = ('name', )
    list_per_page = 50
    search_fields = ('name',)
    search_help_text = ('Поиск по названию')
    actions_on_bottom = True


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Панель администратора для тегов."""
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    list_filter = ('name', )
    list_editable = ('color',)
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 50
    search_fields = ('name',)
    search_help_text = ('Поиск по имени тега')
    actions_on_bottom = True
