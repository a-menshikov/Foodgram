from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Пользователь."""

    email = models.EmailField(
        'Электронная почта',
        db_index=True,
        max_length=254,
        unique=True,
        )
    username = models.CharField(
        'Имя пользователя',
        db_index=True,
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Недопустимый символ в имени пользователя',
                )
            ]
        )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=False,
        )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=False,
        )
    password = models.CharField(
        'Пароль',
        max_length=150,
        blank=False,
        )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username
