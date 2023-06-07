from django.contrib import admin

from .models import Subscribe, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'username', 'first_name', 'last_name', 'is_superuser',
        'is_active', 'date_joined'
    )
    list_filter = ('email', 'username')
    list_display_links = ('email',)
    search_fields = ('username',)
    fieldsets = (
        (
            'Пользователь',
            {
                'fields': ('email', 'username', 'first_name', 'last_name',
                           'password')
            },
        ),
        (
            'Права',
            {
                'fields':  ('is_active', 'is_staff', 'is_superuser')
            },
        )
     )


@admin.register(Subscribe)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    list_display_links = ('user',)
    search_fields = ('user',)
