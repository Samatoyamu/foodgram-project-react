import django_filters
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.pagination import CustomPagination

from .filters import IngredientsFilter, RecipesFilters
from .models import Favorites, Ingredients, Recipes, ShoppingCart, Tags
from .permissions import IsAuthenticatedOrReadOnly
from .serializers import (FavoriteShoppingSerializer, IngredientsSerializer,
                          RecipesSerializer, TagsSerializer)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = TagsSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = RecipesFilters

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        recipe = ShoppingCart.objects.filter(user=self.request.user,
                                             recipe__id=pk).exists()
        if request.method == 'POST':
            if recipe:
                return Response(
                    {'errors': 'Рецепт уже добавлен'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            recipe = get_object_or_404(Recipes, id=pk)
            ShoppingCart.objects.create(user=self.request.user,
                                        recipe=recipe)
            serializer = FavoriteShoppingSerializer(
                recipe,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not recipe:
                return Response(
                    {'errors': 'Рецепта нету в корзине'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            ShoppingCart.objects.filter(user=self.request.user,
                                        recipe__id=pk).delete()
            return Response(
                    {'success': 'Удалено из корзины'},
                    status=status.HTTP_204_NO_CONTENT
                )

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def favorite(self, request, pk):
        favorite = Favorites.objects.filter(user=self.request.user,
                                            recipe__id=pk).exists()
        if request.method == 'POST':
            if favorite:
                return Response(
                    {'errors': 'Рецепт уже в избранном'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            favorite = get_object_or_404(Recipes, id=pk)
            Favorites.objects.create(user=self.request.user,
                                     recipe=favorite)
            serializer = FavoriteShoppingSerializer(
                favorite,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not favorite:
                return Response(
                    {'errors': 'Рецепта нету в избранном'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Favorites.objects.filter(user=self.request.user,
                                     recipe__id=pk).delete()
            return Response(
                    {'success': 'Больше не в избранном'},
                    status=status.HTTP_204_NO_CONTENT
                )


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (IngredientsFilter,)
    search_fields = ('^name',)
