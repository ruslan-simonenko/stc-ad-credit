from abc import ABC, abstractmethod


class DTODataComparable(ABC):
    """
    Defines second set of equality methods to use in conjunction with
    tests.utils.dto_comparison_utils.patched_dto_for_comparison.
    Allows one to ignore certain unpredictable values when comparing data in tests: ids, dates, etc
    """

    @abstractmethod
    def _data_hash(self) -> int:
        pass

    @abstractmethod
    def _data_eq(self, other) -> bool:
        pass
