from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from users.models import User
from .validators import validate_regex


class Tags(models.Model):
    name = models.CharField(
        'Название тега',
        unique=True,
        max_length=settings.MAX_LENGTH,
        validators=(validate_regex,),
    )
    color = models.CharField(
        'Цвет(HEX)',
        unique=True,
        max_length=7,
    )
    slug = models.SlugField(
        'Слэг тега',
        unique=True,
        max_length=settings.MAX_LENGTH,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    name = models.CharField(
        'Название ингредиента',
        unique=True,
        max_length=settings.MAX_LENGTH,
        validators=(validate_regex,),
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=20,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_name_ingredient'
            )
        ]

    def __str__(self):
        return self.name


class Recipes(models.Model):
    tags = models.ManyToManyField(
        Tags,
        verbose_name='Теги',
        related_name='recipe'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='recipe',
        verbose_name='Автор',
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        verbose_name='Ингредиенты',
        related_name='recipe',
        through='IngredientInRecipe',
    )
    name = models.CharField(
        'Название рецепта',
        max_length=200
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/images/'
    )
    text = models.TextField(
        'Описание'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=(
            MinValueValidator(
                1, message='Время приготовления больше 1 минуты'),
        ),
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='ingredients_recipes',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Кол-во ингредиента',
        validators=(
            MinValueValidator(
                1, message='Надо больше 1 ингредиента'),
        ),
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиент в рецептах'

    def __str__(self):
        return str(self.recipe)


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shop_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        constraints = [
            models.UniqueConstraint(fields=('user', 'recipe'),
                                    name='unique_cart'),
        ]

    def __str__(self):
        return str(self.recipe)


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites_user',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=('user', 'recipe'),
                                    name='unique_user_recipe'),
        ]

    def __str__(self):
        return str(self.user)
