from django.contrib import admin
from recipes.models import Ingredient, Tag, Recipe, Favorite
from django.db.models import Count, OuterRef


class TagsInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 3


class IngredientsInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 3


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


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Панель администратора для рецептов."""
    list_display = (
        'id',
        'name',
        'author',
        'favorite_count',
    )
    inlines = (
        TagsInline,
        IngredientsInline
    )
    fields = ('name', 'author', 'image', 'text', 'cooking_time',
              'favorite_count')
    readonly_fields = ('favorite_count',)
    list_filter = ('author', 'name', 'tags')

    def get_queryset(self, request):
        return Recipe.objects.annotate(
            favorite_count=Count(
                Favorite.objects.filter(recipe=OuterRef('pk')).values('id')
            )
        )

    @admin.display(
        ordering='favorite_count',
        description='Количество добавлений в избранное',
    )
    def favorite_count(self, obj):
        return obj.favorite_count
