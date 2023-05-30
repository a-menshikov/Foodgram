from django.contrib import admin

from users.models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    """Панель администратора для пользователей."""

    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
    )
    list_editable = (
        'is_active',
    )
    list_filter = (
        'email',
        'username',
    )
