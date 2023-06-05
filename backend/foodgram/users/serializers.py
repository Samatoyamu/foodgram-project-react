from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from recipes.serializers import FavoriteShoppingSerializer
from rest_framework import serializers

from .models import Subscribe
from .validators import validate_regex

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(validators=[validate_regex])
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')

    def validate(self, data):
        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError('Такой пользователь уже есть')
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError('Такая почта уже есть')
        return data


class UserListSerializer(UserCreateSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        if self.context.get('request').user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=self.context.get('request').user,
                                        author=obj.pk).exists()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')


class SubscriptionsSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        source='recipe.count', read_only=True
    )

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(user=self.context.get('request').user,
                                        author=obj).exists()

    def get_recipes(self, obj):
        limit = self.context.get('request').GET.get('recipes_limit')
        recipes = User.objects.get(id=obj.pk).recipe.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = FavoriteShoppingSerializer(
            recipes,
            many=True,
        )
        return serializer.data

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
