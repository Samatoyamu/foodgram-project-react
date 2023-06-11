from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from recipes.validators import validate_name


class User(AbstractUser):
    email = models.EmailField(
        'Адрес электронной почты',
        help_text=f'Электронная почта, '
                  f'не более {settings.EMAIL_LENGTH} символов',
        unique=True,
        max_length=settings.EMAIL_LENGTH,
    )
    first_name = models.CharField(
        'Имя',
        help_text=f'Имя, не более '
                  f'{settings.USER_FIRST_LAST_NAME_LENGTH} символов',
        validators=(validate_name(),),
        max_length=settings.USER_FIRST_LAST_NAME_LENGTH
    )
    last_name = models.CharField(
        'Фамилия',
        help_text=f'Фамилия, не более '
                  f'{settings.USER_FIRST_LAST_NAME_LENGTH} символов',
        validators=(validate_name(),),
        max_length=settings.USER_FIRST_LAST_NAME_LENGTH
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        help_text='Тот, кто подписывается',
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        help_text='Тот, на кого подписываются',
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(fields=['author', 'user'],
                                    name='unique_follow'),
            models.CheckConstraint(check=~models.Q(author=models.F('user')),
                                   name='cant_follow_yourself'),
        ]
