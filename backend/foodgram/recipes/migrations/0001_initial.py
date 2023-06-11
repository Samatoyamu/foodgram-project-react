# Generated by Django 3.2 on 2023-06-10 13:34

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import recipes.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранные',
            },
        ),
        migrations.CreateModel(
            name='IngredientInRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(help_text='Количество ингредиента', validators=[django.core.validators.MinValueValidator(1, message='Надо больше 1 ингредиента')], verbose_name='Кол-во ингредиента')),
            ],
            options={
                'verbose_name': 'Ингредиент в рецепте',
                'verbose_name_plural': 'Ингредиент в рецептах',
            },
        ),
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Уникальное название, не более 200 символов', max_length=200, unique=True, validators=[recipes.validators.validate_name()], verbose_name='Название ингредиента')),
                ('measurement_unit', models.CharField(help_text='Единица измерения, не более 20 символов', max_length=20, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название рецепта, не более 200 символов', max_length=200, verbose_name='Название рецепта')),
                ('image', models.ImageField(help_text='Фото рецепта', upload_to='recipes/images/', verbose_name='Изображение')),
                ('text', models.TextField(help_text='Описание рецепта', verbose_name='Описание')),
                ('cooking_time', models.PositiveSmallIntegerField(help_text='Время приготовления, мин.', validators=[django.core.validators.MinValueValidator(1, message='Время приготовления больше 1 минуты')], verbose_name='Время приготовления')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название тега, не более 200 символов', max_length=200, unique=True, validators=[recipes.validators.validate_name()], verbose_name='Название тега')),
                ('color', models.CharField(help_text='Поле HEX, не более 7 символов', max_length=7, unique=True, validators=[recipes.validators.validate_hex()], verbose_name='Цвет(HEX)')),
                ('slug', models.SlugField(help_text='Уникальный слэг, не более 200 символов', max_length=200, unique=True, verbose_name='Слэг тега')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='recipes.recipes', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзина',
            },
        ),
    ]
