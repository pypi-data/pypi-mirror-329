from typing import Any, Dict
from datetime import datetime

from attrs import has
from cattrs import Converter
from cattrs.gen import make_dict_structure_fn, make_dict_unstructure_fn


class BaseModelFactory:
    def __new__(cls, name: str, reg_alias: bool = True, reg_datetime: bool = True):
        class CustomBaseModel:
            converter = Converter()

            @classmethod
            def structure(cls, obj: Dict[str, Any]):
                return cls.converter.structure(obj, cls)

            def unstructure(self):
                return self.converter.unstructure(self)

            @classmethod
            def register_aliases(cls):
                cls.converter.register_structure_hook_factory(
                    has,
                    lambda _cls: make_dict_structure_fn(_cls, cls.converter, _cattrs_use_alias=True)
                )

                cls.converter.register_unstructure_hook_factory(
                    has,
                    lambda _cls: make_dict_unstructure_fn(_cls, cls.converter, _cattrs_use_alias=True)
                )

            @classmethod
            def register_datetime(cls):
                cls.converter.register_structure_hook(datetime, lambda obj, _: datetime.fromisoformat(obj))
                cls.converter.register_unstructure_hook(datetime, lambda obj: obj.isoformat().replace('+00:00', 'Z'))

        CustomBaseModel.__name__ = name
        CustomBaseModel.register_aliases() if reg_alias else None
        CustomBaseModel.register_datetime() if reg_datetime else None
        return CustomBaseModel


__all__ = ("BaseModelFactory", )
