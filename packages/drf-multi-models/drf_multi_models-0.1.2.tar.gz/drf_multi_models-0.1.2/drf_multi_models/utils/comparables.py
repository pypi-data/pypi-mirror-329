from typing import Any


class InterleaveComparable:
    """Class to allow comparison of all the criteria the ordering could have while interleaving.

    Allows the reversing of individual criteria and None to be last.

    Only overwrites __eq__ and __lt__ to allow the use of the sorted function.
    """

    def __init__(self, value: Any, *, is_reversed: bool = False) -> None:
        self.value = value
        self.is_reversed = is_reversed

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, InterleaveComparable):
            raise TypeError(
                f"Comparisons should be between InterleaveComparable objects, not {type(self)} and {type(other)}",
            )
        return other.value == self.value

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, InterleaveComparable):
            raise TypeError(
                f"Comparisons should be between InterleaveComparable objects, not {type(self)} and {type(other)}",
            )

        if self.value is None and other.value is None:
            # If self.value and other.value are None, we don't care about the order,
            # but send False to have the equality evaluated
            is_lt = False
        elif self.value is None:
            # If self.value is None, and since we want None to be last, then it's not less than
            is_lt = False
        elif other.value is None:
            # If other.value is None, and since we want None to be last, then it's less than
            is_lt = True
        else:
            is_lt = self.value < other.value

        return is_lt if not self.is_reversed else not is_lt
