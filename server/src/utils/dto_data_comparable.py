from abc import ABC, abstractmethod


class DTODataComparable(ABC):
    """
    Defines second set of equality methods to use in conjunction with
    tests.utils.dto_comparison_utils.patched_dto_for_comparison.
    Allows one to ignore certain unpredictable values when comparing data in tests: ids, dates, etc. This is especially
    important when comparing values inside collections.
    """

    @abstractmethod
    def _data_hash(self) -> int:
        """
        Same as __hash__, but doesn't take into account dynamically generated data: IDs, Dates, etc
        :return: Object's hash
        """
        pass

    @abstractmethod
    def _data_eq(self, other) -> bool:
        """
        Same as __eq__, but doesn't take into account dynamically generated data: IDs, Dates, etc

        :param other:
        :return: Whether objects are equal or not
        """
        pass
