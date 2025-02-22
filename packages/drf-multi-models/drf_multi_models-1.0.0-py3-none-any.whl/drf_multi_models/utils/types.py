from contextlib import contextmanager
from typing import Any, Dict, Generator, Protocol, Sequence, TypeAlias, TypeVar

from django.db.models import Model, QuerySet
from rest_framework.response import Response
from rest_framework.serializers import Serializer

ModelLabel: TypeAlias = str
ProcessedQuerysetsShape = TypeVar("ProcessedQuerysetsShape")


class BaseMultiModelGenericAPIViewProtocol(
    Protocol[ProcessedQuerysetsShape],
):
    # region Defined by DRF stubs

    def get_serializer(self, *args: Any, **kwargs: Any) -> Serializer: ...

    def paginate_queryset(
        self,
        queryset: QuerySet[Model] | Sequence[Any],
    ) -> Sequence[Any] | None: ...

    def get_paginated_response(self, data: Any) -> Response: ...

    # endregion
    # region Defined internally in the package

    @contextmanager
    def apply_model_settings(
        self,
        model_label: ModelLabel,
        model_settings: Dict[str, Any],
    ) -> Generator[None, None, None]: ...

    def extract_processed_querysets_items(
        self,
        processed_querysets: ProcessedQuerysetsShape,
    ) -> Sequence[Model]: ...

    def filter_querysets(
        self,
        querysets: Dict[ModelLabel, QuerySet],
    ) -> Dict[ModelLabel, QuerySet]: ...

    def get_querysets(self) -> Dict[ModelLabel, QuerySet]: ...

    def process_querysets(
        self,
        querysets: Dict[ModelLabel, QuerySet],
    ) -> ProcessedQuerysetsShape: ...

    def get_model_settings_mapping(self) -> Dict[ModelLabel, Dict[str, Any]]: ...

    # endregion
