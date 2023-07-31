from contextlib import contextmanager
from typing import TypeVar, Type, Union

from pydantic import BaseModel

from src.utils.dto_data_comparable import DTODataComparable

TPydanticModelSubtype = TypeVar('TPydanticModelSubtype', bound=Union[BaseModel, DTODataComparable])


@contextmanager
def patched_dto_for_comparison(model_type: Type[TPydanticModelSubtype]):
    hash_backup = model_type.__hash__
    eq_backup = model_type.__eq__

    model_type.__hash__ = model_type._data_hash
    model_type.__eq__ = model_type._data_eq
    try:
        yield
    finally:
        model_type.__hash__ = hash_backup
        model_type.__eq__ = eq_backup
