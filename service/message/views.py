# Create your views here.
from django.contrib.auth import get_user_model
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from .models import Groups
from .serializers import GroupsSerializer


class UserViewSet(NestedViewSetMixin, ModelViewSet):
    model = get_user_model()


class GroupViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = GroupsSerializer
    permission_classes = (IsAuthenticated,)
    model = Groups

    @detail_route(methods=['get'])
    def join(self, request, pk=None):
        return Response({'status': 'join set %s' % request.user.username})

    @detail_route(methods=['get'])
    def dismiss(self, request, pk=None):
        return Response({'status': 'dismiss set %s' % request.user.username})

    @detail_route(methods=['get'])
    def quit(self, request, pk=None):
        return Response({'status': 'quit set %s' % request.user.username})

    def get_queryset(self):
        return self.request.user.im_groups.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
