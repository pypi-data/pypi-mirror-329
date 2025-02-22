from typing import Sequence, Union

from django.db.models import QuerySet
from rest_framework.pagination import BasePagination, LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.views import APIView


class FlatMultiModelBasePagination(BasePagination):
    """Implementation of BasePagination for Flat MultiModel."""

    def prepare_queryset_to_interleave(
        self,
        queryset: QuerySet,
        request: Request,
        view: Union[APIView, None] = None,
    ) -> QuerySet:
        """Prepares the queryset for pagination."""
        raise NotImplementedError(
            "prepare_queryset_to_interleave() must be implemented.",
        )


class FlatMultiModelLimitOffsetPagination(
    FlatMultiModelBasePagination,
    LimitOffsetPagination,
):
    """Implementation of LimitOffsetPagination for Flat MultiModel, with FlatMultiModelBasePagination."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.sliced_out_count = 0

    def get_count(self, queryset: Union[QuerySet, Sequence]) -> int:
        """Gets the count of the queryset, adding the sliced out count."""
        return super().get_count(queryset) + self.sliced_out_count

    def prepare_queryset_to_interleave(
        self,
        queryset: QuerySet,
        request: Request,
        view: Union[APIView, None] = None,
    ) -> QuerySet:
        """Prepares the queryset for pagination, slicing out the extra records for performance's sake."""
        limit = self.get_limit(request)
        if limit is None:
            return queryset
        offset = self.get_offset(request)
        count = super().get_count(queryset)
        if limit + offset >= count:
            return queryset
        self.sliced_out_count += count - (limit + offset)
        # Doing the `.all()` to force the queryset to reevaluate if it's already evaluated and not return a list
        queryset = queryset.all()
        # By slicing up from 0 to limit + offset, we're making sure that all the record wanted are in the queryset.
        # This is because the queryset is ordered by the criteria we want to interleave, so the records we want are
        # at the beginning of the queryset already. We're just slicing out the extra records for every model to
        # then later have fewer records to interleave.
        return queryset[: limit + offset]
