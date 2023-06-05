from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Subscribe
from .pagination import CustomPagination
from .serializers import SubscriptionsSerializer

User = get_user_model()


class UserViewSet(UserViewSet):
    pagination_class = CustomPagination


class SubscriptionsListView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SubscriptionsSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)


class SubscriptionsViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SubscriptionsSerializer

    @action(
        detail=True,
        methods=['POST', 'DELETE']
    )
    def subscribe(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        subs = Subscribe.objects.filter(user=self.request.user,
                                        author=author).exists()
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
