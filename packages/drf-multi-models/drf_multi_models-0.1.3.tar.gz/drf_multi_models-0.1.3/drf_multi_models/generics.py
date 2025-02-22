from contextlib import contextmanager
from operator import attrgetter
from typing import Any, Dict, Generator, Generic, List, Sequence, Tuple, Union

from django.core.exceptions import ValidationError
from django.db.models import Model, QuerySet
from rest_framework.filters import OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from drf_multi_models.mixins import FlatMultiModelListMixin
from drf_multi_models.pagination import FlatMultiModelBasePagination
from drf_multi_models.utils.comparables import InterleaveComparable
from drf_multi_models.utils.types import ModelLabel, ProcessedQuerysetsShape
from drf_multi_models.views import MultiModelAPIView

REQUIRED_MODEL_SETTINGS_KEY_TUPLES = [
    ("queryset", "get_queryset"),
    ("serializer_class", "get_serializer_class"),
]
NOT_ALLOWED_MODEL_SETTINGS_KEYS = [
    "get_serializer",
    "filter_queryset",
    "pagination_class",
    "paginator",
    "paginate_queryset",
    "get_paginated_response",
]


class BaseMultiModelGenericAPIView(
    MultiModelAPIView,
    GenericAPIView,
    Generic[ProcessedQuerysetsShape],
):
    """Implementation of GenericAPIView for MultiModel, with the MultiModelAPIView."""

    model_settings_mapping: Union[Dict[ModelLabel, Dict[str, Any]], None] = None
    overwritten_model_settings_mapping: Dict[ModelLabel, Dict[str, Any]] = {}
    are_model_settings_applied: bool = False

    def get_model_settings_mapping(self) -> Dict[ModelLabel, Dict[str, Any]]:
        """Return the model_settings_mapping attribute."""
        assert self.model_settings_mapping is not None, (
            f"{self.__class__.__name__} should either include a `model_settings_mapping` attribute, "
            "or override the `get_model_settings_mapping()` method."
        )

        return self.model_settings_mapping

    def _validate_model_settings(self, model_settings: Dict[str, Any]) -> None:
        # Validate required keys
        for required_model_settings_key_tuple in REQUIRED_MODEL_SETTINGS_KEY_TUPLES:
            if all(
                required_model_settings_key not in model_settings
                for required_model_settings_key in required_model_settings_key_tuple
            ):
                formatted_required_model_settings_key_tuple = ", ".join(
                    [
                        f"'{required_model_settings_key}'"
                        for required_model_settings_key in required_model_settings_key_tuple
                    ],
                )
                raise ValidationError(
                    f"All items in the {self.__class__.__name__} model_settings_mapping attribute should contain "
                    f"any of the following keys: {formatted_required_model_settings_key_tuple}",
                )

        # Validate not allowed keys
        for not_allowed_model_settings_key in NOT_ALLOWED_MODEL_SETTINGS_KEYS:
            if not_allowed_model_settings_key in model_settings:
                raise ValidationError(
                    f"No item in the {self.__class__.__name__} model_settings_mapping attribute "
                    f"attribute can contain a {not_allowed_model_settings_key} key.",
                )

    @contextmanager
    def apply_model_settings(
        self,
        model_label: ModelLabel,
        model_settings: Dict[str, Any],
    ) -> Generator[None, None, None]:
        """Apply the model settings for the given model.

        This is done by setting the attributes in the model_settings dict
        as attributes of the view when the context is entered.

        When the context is exited, the original values are restored,
        including deletion of non-existing attributes.
        """
        # Apply the overwritten settings if there are any for the model settings for the given label
        model_settings_to_apply = model_settings.copy()
        if overwritten_model_settings := self.overwritten_model_settings_mapping.get(
            model_label,
        ):
            model_settings_to_apply.update(overwritten_model_settings)

        self._validate_model_settings(model_settings_to_apply)
        existing_model_settings = {}
        non_existing_model_settings_keys = []
        try:
            for key, value in model_settings_to_apply.items():
                if hasattr(self, key):
                    existing_model_settings[key] = getattr(self, key)
                else:
                    non_existing_model_settings_keys.append(key)
                setattr(self, key, value)
            self.are_model_settings_applied = True
            yield
        finally:
            for key, value in existing_model_settings.items():
                setattr(self, key, value)
            for key in non_existing_model_settings_keys:
                delattr(self, key)
            self.are_model_settings_applied = False

    def get_querysets(self) -> Dict[ModelLabel, QuerySet]:
        """Return the querysets for each model in the model_settings_mapping attribute."""
        model_settings_mapping = self.get_model_settings_mapping()
        querysets = {}
        for model_label, model_settings in model_settings_mapping.items():
            with self.apply_model_settings(model_label, model_settings):
                queryset = self.get_queryset()
            querysets[model_label] = queryset
        return querysets

    def filter_querysets(
        self,
        querysets: Dict[ModelLabel, QuerySet],
    ) -> Dict[ModelLabel, QuerySet]:
        """Filter the querysets for each model received, returning the results for all of them."""
        model_settings_mapping = self.get_model_settings_mapping()
        filtered_querysets = {}
        for model_label, queryset in querysets.items():
            model_settings = model_settings_mapping[model_label]
            with self.apply_model_settings(model_label, model_settings):
                filtered_queryset = self.filter_queryset(queryset)
            filtered_querysets[model_label] = filtered_queryset
        return filtered_querysets

    def process_querysets(
        self,
        querysets: Dict[ModelLabel, QuerySet],
    ) -> ProcessedQuerysetsShape:
        """Process the querysets for each model received, returning the results for all of them."""
        raise NotImplementedError("process_querysets() must be implemented.")

    def extract_processed_querysets_items(
        self,
        processed_querysets: ProcessedQuerysetsShape,
    ) -> Sequence[Model]:
        """Extract the processed querysets items from the processed querysets."""
        raise NotImplementedError(
            "extract_processed_querysets_items() must be implemented.",
        )


class FlatMultiModelGenericAPIView(
    BaseMultiModelGenericAPIView[List[Tuple[Model, ModelLabel]]],
):
    """Implementation of BaseMultiModelGenericAPIView for Flat MultiModel.

    A Flat MultiModel is a MultiModel that will return the instances of the models in a single list:
        [ModelA, ModelB, ModelA, ModelA, ModelB]
    """

    def process_querysets(
        self,
        querysets: Dict[ModelLabel, QuerySet],
    ) -> List[Tuple[Model, ModelLabel]]:
        """Process the querysets for each model received, returning the results for all of them.

        For Flat MultiModel, it will return a single list of tuples, where each tuple contains the model instance
        and the model label.

        This is also the method that will interleave the querysets, making sure the order requested by the user
        is now shared among the processed querysets.
        """
        querysets_to_interleave = {}
        for model_label, queryset in querysets.items():
            queryset = querysets[model_label]

            prepared_queryset = self.prepare_queryset_to_interleave(queryset)
            if prepared_queryset is not None:
                querysets_to_interleave[model_label] = prepared_queryset
            else:
                querysets_to_interleave[model_label] = queryset

        return self.get_interleaved_queryset(querysets_to_interleave)

    def prepare_queryset_to_interleave(
        self,
        queryset: QuerySet,
    ) -> Union[QuerySet, None]:
        """Optional pagination option that can prepare the queryset to be interleaved.

        Done with the purpose of reducing the amount of data to be processed by the interleave algorithm.

        Optional since it will check if it's a MultiModel paginator to do so.
        """
        paginator = self.paginator
        if paginator is None:
            return None
        if isinstance(paginator, FlatMultiModelBasePagination):
            return paginator.prepare_queryset_to_interleave(
                queryset,
                self.request,
                self,
            )
        return None

    def get_interleaved_queryset(
        self,
        querysets: Dict[ModelLabel, QuerySet],
    ) -> List[Tuple[Model, ModelLabel]]:
        """Interleave the querysets into a processed list of tuples containing the model instance and model label.

        This logic relies on Ordering through `OrderingFilter` to also gather the ordering parameters to interleave.

        The algorithm is as follows:
        1. For each Queryset:
            1. Get the ordering parameters, using the `OrderingFilter` filter backend.
            2. Try to select related the ordering parameters, so we can use them in the interleaving algorithm without db lookups.
            3. Gather data to be able to perform the interleaving through sorting criteria.
        2. Perform the interleaving through sorting the criteria of all the querysets data combined.
        """
        model_settings_mapping = self.get_model_settings_mapping()

        queryset_data_to_interleave = []
        for model_label, queryset in querysets.items():
            model_settings = model_settings_mapping[model_label]

            # Get all the ordering relying in filter Backends
            ordering_parameters = []
            with self.apply_model_settings(model_label, model_settings):
                for backend in self.filter_backends:
                    if issubclass(backend, OrderingFilter):
                        new_ordering_parameters = backend().get_ordering(
                            self.request,
                            queryset,
                            self,
                        )
                        if new_ordering_parameters is not None:
                            for new_ordering_parameter in new_ordering_parameters:
                                is_reversed = new_ordering_parameter.startswith("-")
                                if is_reversed:
                                    new_ordering_parameter = new_ordering_parameter[1:]
                                ordering_parameters.append(
                                    (new_ordering_parameter, is_reversed),
                                )

            # Try to select related the ordering parameters, so we can use them in the interleave algorithm without db lookups
            for ordering_parameter, _ in ordering_parameters:
                # With this, we can use ordering parameters that span relationships, ignoring always the field itself
                # and selecting the related model containing it. Also ignores fields in the model itself
                select_related_ordering_paramater = "__".join(
                    ordering_parameter.split("__")[:-1],
                )
                if select_related_ordering_paramater:
                    queryset = queryset.select_related(
                        select_related_ordering_paramater,
                    )

            # Create the data containing the model instance, model label and criteria interleave
            for queryset_item in queryset:
                comparable_criteria = []
                for ordering_parameter, is_reversed in ordering_parameters:
                    clean_ordering_parameter = ordering_parameter.replace("__", ".")
                    try:
                        value = attrgetter(clean_ordering_parameter)(queryset_item)
                    except AttributeError:
                        value = None
                    comparable_criteria.append(
                        InterleaveComparable(
                            value,
                            is_reversed=is_reversed,
                        ),
                    )
                queryset_data_to_interleave.append(
                    {
                        "queryset_item": queryset_item,
                        "model_label": model_label,
                        "criteria": tuple(comparable_criteria),
                    },
                )

        # Perform the interleave through sorting the criteria
        sorted_queryset_data_to_interleave = sorted(
            queryset_data_to_interleave,
            key=lambda item: item["criteria"],
        )

        # Create the processed querysets
        interleaved_querysets = []
        for item in sorted_queryset_data_to_interleave:
            interleaved_querysets.append((item["queryset_item"], item["model_label"]))

        return interleaved_querysets

    def extract_processed_querysets_items(
        self,
        processed_querysets: List[Tuple[Model, ModelLabel]],
    ) -> Sequence[Model]:
        """Extract the processed querysets items from the processed querysets.

        For Flat MultiModel, it will return the first item of each tuple, since it contains the model instance.
        """
        return [querysets_item[0] for querysets_item in processed_querysets]


class FlatMultiModelListAPIView(FlatMultiModelListMixin, FlatMultiModelGenericAPIView):
    """Implementation of FlatMultiModelGenericAPIView for Flat MultiModel, with the FlatMultiModelListMixin."""

    def get(self, request: Request, *args, **kwargs) -> Response:
        """Maps the GET API method to the `list()` method."""
        return self.list(request, *args, **kwargs)
