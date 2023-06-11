from django_filters import rest_framework
from rest_framework.filters import SearchFilter

from users.models import User


class RecipesFilters(rest_framework.FilterSet):
    author = rest_framework.ModelChoiceFilter(
        queryset=User.objects.all()
    )
    tags = rest_framework.AllValuesMultipleFilter(
        field_name='tags__slug'
    )
    is_favorited = rest_framework.BooleanFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    def filter_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorites_recipes__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(recipes_cart__user=self.request.user)
        return queryset


class IngredientsFilter(SearchFilter):
    search_param = 'name'
