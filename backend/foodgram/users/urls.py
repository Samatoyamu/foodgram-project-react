from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import SubscriptionsView, SubscriptionsViewSet, UserViewSet

app_name = 'users'
router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('users', SubscriptionsViewSet, basename='subscribe')

urlpatterns = [
    path('users/subscriptions/', SubscriptionsView.as_view(),
         name='subscriptions'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
