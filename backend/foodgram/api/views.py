import django_filters
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import (Favorites, IngredientInRecipe, Ingredients,
                            Recipes, ShoppingCart, Tags)
from users.models import Subscribe, User
from .filters import IngredientsFilter, RecipesFilters
from .pagination import CustomPagination
from .permissions import IsAuthenticatedOrReadOnly
from .serializers import (FavoriteShoppingSerializer, IngredientsSerializer,
                          RecipesSerializer, SubscriptionsSerializer,
                          TagsSerializer)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = TagsSerializer


class RecipeViewSet(viewsets.ModelViewSet):
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

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        ingredients = (
            IngredientInRecipe.objects.filter(
                recipe__recipes_cart__user=request.user
            )
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(sum_amount=Sum('amount')).order_by('amount')
        )
        data_dict = {}
        ingredients_list = []
        for item in ingredients:
            name = item['ingredient__name']
            measure = item['ingredient__measurement_unit']
            sum_amount = item['sum_amount']
            data_dict[name] = [sum_amount, measure]
        for id, (key, value) in enumerate(data_dict.items()):
            ingredients_list.append(
                f'{id}. {key} - ' f'{value[0]} ' f'{value[1]}'
            )
        return HttpResponse('\n'.join(ingredients_list),
                            content_type='text/plain',
                            status=status.HTTP_200_OK)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (IngredientsFilter,)
    search_fields = ('^name',)


class SubscriptionsViewSet(viewsets.ViewSetMixin,
                           generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination
    serializer_class = SubscriptionsSerializer

    @action(
        detail=False,
        methods=['GET'],
    )
    def subscriptions(self, request):
        users = User.objects.filter(following__user=self.request.user)
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
    )
    def subscribe(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        subs = self.request.user.follower.filter(author=author).exists()
        if request.method == 'POST':
            if subs:
                return Response(
                    {'errors': 'уже есть подписка'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if author == self.request.user:
                return Response(
                    {'errors': 'На себя нельзя подписаться'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = SubscriptionsSerializer(
                author,
                context={'request': request}
                )
            Subscribe.objects.create(user=self.request.user,
                                     author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not subs:
                return Response(
                    {'errors': 'Не было в подписках'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Subscribe.objects.filter(user=self.request.user,
                                     author=author).delete()
            return Response(
                    {'success': 'Отписались'},
                    status=status.HTTP_204_NO_CONTENT
                )
