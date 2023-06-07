from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import IngredientsViewSet, RecipeViewSet, TagsViewSet

app_name = 'recipes'
router = DefaultRouter()
router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
]
