from django.contrib import admin

from .models import (Favorites, IngredientInRecipe, Ingredients, Recipes,
                     ShoppingCart, Tags)


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color')
    search_fields = ('name',)
    list_filter = ('name', 'slug', 'color')
    list_editable = ('color',)
    list_display_links = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name', )
    list_display_links = ('name',)
    empty_value_display = '-пусто-'


class RecipeIngredientInline(admin.TabularInline):
    model = Recipes.ingredients.through
    extra = 1


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = ('id', 'name', 'author')
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags')
    ordering = ('id',)
    list_display_links = ('name',)
    readonly_fields = ('favorite_count',)

    @admin.display(description='Добавили в избранное')
    def favorite_count(self, recipes):
        return recipes.favorites_recipes.count()


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    list_display_links = ('recipe',)
    search_fields = ('recipe',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_display_links = ('user',)
    search_fields = ('user',)


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_display_links = ('user',)
    search_fields = ('user',)
