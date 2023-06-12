from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientsViewSet, RecipeViewSet, SubscriptionsListView,
                    SubscriptionsViewSet, TagsViewSet)

app_name = 'api'
router = DefaultRouter()
router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('users', SubscriptionsViewSet, basename='subscribe')

urlpatterns = [
    path('users/subscriptions/', SubscriptionsListView.as_view(),
         name='subscriptions'),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
