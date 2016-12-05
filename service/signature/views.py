# Create your views here.
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from .models import Signature, Identity
from .serializers import SignatureSerializer, IdentitySerializer


class VerifyViewSet(NestedViewSetMixin, mixins.CreateModelMixin, GenericViewSet):
    serializer_class = SignatureSerializer
    permission_classes = (IsAuthenticated,)
    model = Signature

    def get_queryset(self):
        return self.request.user.signatures.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class CertificateViewSet(NestedViewSetMixin, ReadOnlyModelViewSet):
    serializer_class = SignatureSerializer
    permission_classes = (IsAuthenticated,)
    model = Signature

    def get_queryset(self):
        return self.request.user.signatures.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class HistoryViewSet(NestedViewSetMixin, ReadOnlyModelViewSet):
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

    @list_route(methods=['GET', 'POST'])
    def callback(self, request, *args, **kwargs):
        return Response(['serializer.data'], status=status.HTTP_201_CREATED)

    @list_route(methods=['GET', 'POST'])
    def validate(self, request, *args, **kwargs):
        return Response(['serializer.data'], status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
