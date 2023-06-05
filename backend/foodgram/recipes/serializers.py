from django.contrib.auth import get_user_model
from drf_base64.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import Subscribe
from .models import (Favorites, IngredientInRecipe, Ingredients, Recipes,
                     ShoppingCart, Tags)

User = get_user_model()


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tags


class AuthorSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        if self.context.get('request').user.is_anonymous:
            return False
        return Subscribe.objects.filter(
            user=self.context.get('request').user, author=obj.pk).exists()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed'
        )


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient.id', queryset=Ingredients.objects.all()
    )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True
    )
    name = serializers.CharField(
        source='ingredient.name', read_only=True
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = [
            UniqueTogetherValidator(queryset=IngredientInRecipe.objects.all(),
                                    fields=('ingredient', 'recipe')
                                    )
        ]


class RecipeListSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    author = AuthorSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        queryset = IngredientInRecipe.objects.filter(recipe=obj)
        return IngredientInRecipeSerializer(queryset, many=True).data

    def get_is_in_shopping_cart(self, obj):
        if self.context.get('request').user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=self.context.get('request').user.id,
            recipe=obj.id
        ).exists()

    def get_is_favorited(self, obj):
        if self.context.get('request').user.is_anonymous:
            return False
        return Favorites.objects.filter(
            user=self.context.get('request').user.id,
            recipe=obj.id).exists()

    class Meta:
        model = Recipes
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )


class IngredientsCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredients.objects.all())

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class RecipesSerializer(serializers.ModelSerializer):
    ingredients = IngredientsCreateSerializer(many=True)
    image = Base64ImageField()

    def to_representation(self, instance):
        serializer = RecipeListSerializer(
            instance,
            context={'request': self.context.get('request')}
        )
        return serializer.data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        data = Recipes.objects.create(**validated_data)
        data.tags.set(tags)
        IngredientInRecipe.objects.bulk_create([
            IngredientInRecipe(
                recipe=data,
                ingredient=ingredient.get('id'),
                amount=ingredient.get('amount')
            )
            for ingredient in ingredients
        ])
        return data

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance = super().update(instance, validated_data)
        if tags:
            instance.tags.set(tags)
        if ingredients:
            instance.ingredients.clear()
            IngredientInRecipe.objects.bulk_create([
                IngredientInRecipe(
                    recipe=instance,
                    ingredient=ingredient.get('id'),
                    amount=ingredient.get('amount')
                )
                for ingredient in ingredients
            ])
        return instance

    class Meta:
        model = Recipes
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredients


class FavoriteShoppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
