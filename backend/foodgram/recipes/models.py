from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from users.models import User
from .validators import validate_name, validate_hex


class Tags(models.Model):
    name = models.CharField(
        'Название тега',
        help_text=f'Название тега, '
                  f'не более {settings.TAGS_SLUG_NAME_MAX_LENGTH} символов',
        unique=True,
        max_length=settings.TAGS_SLUG_NAME_MAX_LENGTH,
        validators=(validate_name,),
    )
    color = models.CharField(
        'Цвет(HEX)',
        help_text=f'Поле HEX, не более {settings.HEX_COLOR_LENGTH} символов',
        unique=True,
        max_length=settings.HEX_COLOR_LENGTH,
        validators=(validate_hex,),
    )
    slug = models.SlugField(
        'Слэг тега',
        help_text=f'Уникальный слэг, '
                  f'не более {settings.TAGS_SLUG_NAME_MAX_LENGTH} символов',
        unique=True,
        max_length=settings.TAGS_SLUG_NAME_MAX_LENGTH,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    name = models.CharField(
        'Название ингредиента',
        help_text=f'Уникальное название, '
                  f'не более {settings.INGREDIENTS_NAME_MAX_LENGTH} символов',
        unique=True,
        max_length=settings.INGREDIENTS_NAME_MAX_LENGTH,
        validators=(validate_name,),
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        help_text=f'Единица измерения, '
                  f'не более {settings.INGREDIENTS_MEASUREMENT_LENGHT} '
                  f'символов',
        max_length=settings.INGREDIENTS_MEASUREMENT_LENGHT,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
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
        help_text='Выберите тег(или несколько) для рецепта',
        related_name='recipe'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        help_text='Автор данного рецепта',
        on_delete=models.CASCADE,
        null=True,
        related_name='recipe',
    )
    name = models.CharField(
        'Название рецепта',
        help_text=f'Название рецепта, '
                  f'не более {settings.RECIPES_NAME_MAX_LENGTH} символов',
        max_length=settings.RECIPES_NAME_MAX_LENGTH
    )
    image = models.ImageField(
        'Изображение',
        help_text='Фото рецепта',
        upload_to='recipes/images/'
    )
    text = models.TextField(
        'Описание',
        help_text='Описание рецепта',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        help_text='Время приготовления, мин.',
        validators=(
            MinValueValidator(
                1, message='Время приготовления больше 1 минуты'),
        ),
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipes,
        verbose_name='Рецепт',
        help_text='Название рецепта',
        on_delete=models.CASCADE,
        related_name='ingredients',
    )
    ingredient = models.ForeignKey(
        Ingredients,
        verbose_name='Ингредиент',
        help_text='Ингредиент рецепта',
        on_delete=models.CASCADE,
        related_name='+',
    )
    amount = models.PositiveSmallIntegerField(
        'Кол-во ингредиента',
        help_text='Количество ингредиента',
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
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shop_cart',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='+',
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
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorites_user',
    )
    recipe = models.ForeignKey(
        Recipes,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='+',
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
