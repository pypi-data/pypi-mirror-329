from collections import defaultdict
from typing import Any, Generic, List, OrderedDict, Sequence, Tuple, Union

from django.db.models import Model
from rest_framework.mixins import ListModelMixin
from rest_framework.request import Request
from rest_framework.response import Response

from drf_multi_models.utils.types import (
    BaseMultiModelGenericAPIViewProtocol,
    ModelLabel,
    ProcessedQuerysetsShape,
)


class BaseMultiModelListMixin(
    ListModelMixin,
    Generic[ProcessedQuerysetsShape],
    BaseMultiModelGenericAPIViewProtocol[ProcessedQuerysetsShape],
):
    """Implementation of ListModelMixin for MultiModel.

    Meant to be mixed in with a BaseMultiModelGenericAPIView.
    """

    def list(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        """Override the DRF ListModelMixin's list method. to be used with MultiModel."""
        querysets = self.filter_querysets(self.get_querysets())

        processed_querysets = self.process_querysets(querysets)
        processed_querysets_items = self.extract_processed_querysets_items(
            processed_querysets,
        )

        page = self.paginate_queryset(processed_querysets_items)
        if page is not None:
            serialized_data = self.serialize_processed_querysets_items(
                page,
                processed_querysets,
            )
            return self.get_paginated_response(serialized_data)

        serialized_data = self.serialize_processed_querysets_items(
            processed_querysets_items,
            processed_querysets,
        )
        return Response(serialized_data)

    def serialize_processed_querysets_items(
        self,
        processed_querysets_items: Sequence[Model],
        processed_querysets: ProcessedQuerysetsShape,
    ) -> List[OrderedDict[str, Any]]:
        """Serialize the processed querysets items."""
        raise NotImplementedError(
            "serialize_processed_querysets_items() must be implemented.",
        )


class FlatMultiModelListMixin(BaseMultiModelListMixin[List[Tuple[Model, ModelLabel]]]):
    """Implementation of BaseMultiModelListMixin for Flat MultiModel.

    Meant to be mixed in with a FlatMultiModelGenericAPIView.
    """

    model_label_key: Union[str, None]

    def get_model_label_key(self) -> Union[str, None]:
        """Return the label key location."""
        assert hasattr(self, "model_label_key"), (
            "'%s' should either include a `model_label_key` attribute, "
            "or override the `get_model_label_key()` method." % self.__class__.__name__
        )
        return self.model_label_key

    def serialize_processed_querysets_items(
        self,
        processed_querysets_items: Sequence[Model],
        processed_querysets: List[Tuple[Model, ModelLabel]],
    ) -> List[OrderedDict[str, Any]]:
        """Serialize the processed querysets items.

        It will do it by grouping them by model label and then serializing them together, instead of one by one.
        """
        querysets_mapping = dict(processed_querysets)
        model_label_to_querysets_items = defaultdict(list)
        for querysets_item in processed_querysets_items:
            model_label = querysets_mapping[querysets_item]
            model_label_to_querysets_items[model_label].append(querysets_item)

        model_label_key = self.get_model_label_key()
        model_settings_mapping = self.get_model_settings_mapping()

        # Grouping them again to serialize in group instead of individually
        querysets_item_to_serialized_item = {}
        for model_label, querysets_items in model_label_to_querysets_items.items():
            model_settings = model_settings_mapping[model_label]
            with self.apply_model_settings(model_label, model_settings):
                serializer = self.get_serializer(querysets_items, many=True)
            serialized_items = serializer.data
            if len(serialized_items) != len(querysets_items):
                raise RuntimeError(
                    "The number of serialized items is not the same as the number of querysets items in a Flat MultiModel view.",
                )

            for querysets_item, serialized_item in zip(
                querysets_items,
                serialized_items,
            ):
                # Adding the model label key to the serialized item
                if model_label_key is not None:
                    serialized_item[model_label_key] = model_label
                querysets_item_to_serialized_item[querysets_item] = serialized_item

        processed_serialized_items = []
        for querysets_item in processed_querysets_items:
            processed_serialized_items.append(
                querysets_item_to_serialized_item[querysets_item],
            )

        return processed_serialized_items
