# Generated by Django 3.2 on 2023-06-05 11:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0004_auto_20230603_0038'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredientinrecipe',
            options={'verbose_name': 'Ингредиент в рецепте', 'verbose_name_plural': 'Ингредиент в рецептах'},
        ),
        migrations.AlterModelOptions(
            name='ingredients',
            options={'ordering': ('id',), 'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.RemoveConstraint(
            model_name='favorites',
            name='uniq_favorite_user_recipe',
        ),
        migrations.RemoveConstraint(
            model_name='ingredientinrecipe',
            name='unique ingredient recipe',
        ),
        migrations.RemoveConstraint(
            model_name='ingredients',
            name='unique_ingredient',
        ),
        migrations.AlterField(
            model_name='favorites',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites_recipes', to='recipes.recipes', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='ingredientinrecipe',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Надо больше 1 ингредиента')], verbose_name='Кол-во ингредиента'),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipe', through='recipes.IngredientInRecipe', to='recipes.Ingredients', verbose_name='Ингредиенты'),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='tags',
            field=models.ManyToManyField(related_name='recipe', to='recipes.Tags', verbose_name='Теги'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_cart', to='recipes.recipes', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_cart', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddConstraint(
            model_name='favorites',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_user_recipe'),
        ),
    ]