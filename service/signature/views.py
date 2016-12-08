# Create your views here.

from filters.mixins import FiltersMixin
from rest_framework import filters, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet, ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from url_filter.integrations.drf import DjangoFilterBackend

from .models import Signature, Identity, Validate
from .serializers import SignatureSerializer, IdentitySerializer, ValidateSerializer


class VerifyViewSet(NestedViewSetMixin, mixins.CreateModelMixin, GenericViewSet):
    serializer_class = SignatureSerializer
    permission_classes = (IsAuthenticated,)
    model = Signature

    def get_queryset(self):
        return self.request.user.signatures.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class HistoryViewSet(FiltersMixin, ReadOnlyModelViewSet):
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_fields = ['created']

    ordering_fields = ('created',)
    ordering = ('id',)

    serializer_class = SignatureSerializer
    permission_classes = (IsAuthenticated,)
    model = Signature

    def get_queryset(self):
        return self.request.user.signatures.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class IdentityViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = IdentitySerializer
    queryset = Identity.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class ValidateViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ValidateSerializer
    queryset = Validate.objects.all()
    lookup_field = 'key'
