from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SubscriptionsListView, SubscriptionsViewSet, UserViewSet

app_name = 'users'
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'users', SubscriptionsViewSet, basename='subscribe')

urlpatterns = [
    path('users/subscriptions/', SubscriptionsListView.as_view(),
         name='subscriptions'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
