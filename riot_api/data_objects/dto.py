import inspect
from abc import ABC
from dataclasses import dataclass, fields
from typing import get_args, get_origin


@dataclass
class Dto(ABC):
    def __init__(self, *args, **kwargs):
        pass

    def __post_init__(self):
        for field in fields(self):
            if inspect.isclass(field.type):
                if issubclass(field.type, Dto):
                    self.__setattr__(
                        field.name,
                        field.type(**self.__getattribute__(field.name)),
                    )
            if get_origin(field.type) is list:
                field_type = get_args(field.type)[0]
                if inspect.isclass(field_type):
                    if issubclass(field_type, Dto):
                        self.__setattr__(
                            field.name,
                            [
                                field_type(**obj)
                                for obj in self.__getattribute__(field.name)
                            ]
                        )
