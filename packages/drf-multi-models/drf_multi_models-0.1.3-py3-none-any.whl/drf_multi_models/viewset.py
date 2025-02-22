from rest_framework.viewsets import GenericViewSet

from drf_multi_models.generics import FlatMultiModelGenericAPIView
from drf_multi_models.mixins import FlatMultiModelListMixin


class GenericFlatMultiModelViewSet(FlatMultiModelGenericAPIView, GenericViewSet):
    """Implementation of GenericViewSet for Flat MultiModel, with the FlatMultiModelGenericAPIView."""


class FlatMultiModelAPIViewSet(GenericFlatMultiModelViewSet, FlatMultiModelListMixin):
    """Implementation of GenericFlatMultiModelViewSet for Flat MultiModel, with the FlatMultiModelListMixin."""
