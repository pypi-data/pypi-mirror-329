# jsonhandler/custom_base.py
from pydantic import BaseModel
from typing import Any, Type, TypeVar

T = TypeVar("T", bound="CustomBase")

class CustomBase(BaseModel):
    class Config:
        extra = 'allow'  # allow extra keys

    @classmethod
    def _convert_value(cls, field_type: Any, value: Any) -> Any:
        """
        Convert a raw value into the proper type if needed.
        If field_type is a subclass of CustomBase and value is a dict,
        recursively call from_dict.
        If field_type is a list[...] and value is a list, convert each element.
        If field_type is a dict[...] and value is a dict, convert each value.
        """
        if value is None:
            return None

        # Handle dict conversion: if the field type is a dict type
        if isinstance(value, dict) and getattr(field_type, '__origin__', None) is dict:
            # field_type.__args__ is a tuple (key_type, value_type)
            key_type, value_type = field_type.__args__
            return {k: cls._convert_value(value_type, v) for k, v in value.items()}

        # For nested models (CustomBase subclasses)
        if isinstance(value, dict) and isinstance(field_type, type) and issubclass(field_type, CustomBase):
            return field_type.from_dict(value)

        # For lists
        if isinstance(value, list) and getattr(field_type, '__origin__', None) is list:
            inner_type = field_type.__args__[0]
            return [cls._convert_value(inner_type, item) for item in value]

        return value

    @classmethod
    def from_dict(cls: Type[T], data: dict) -> T:
        """
        Create an instance of the model from a dict,
        converting nested dicts to their respective CustomBase subclasses.
        Missing fields are auto‑populated:
          - For nested CustomBase types: a new instance is created.
          - For list/dict: an empty list/dict is used.
          - Otherwise, None is used.
        Validation is bypassed using construct().
        """
        complete_data = {}
        for field_name, field in cls.model_fields.items():
            field_type = field.annotation
            if field_name in data:
                complete_data[field_name] = cls._convert_value(field_type, data[field_name])
            else:
                # Auto-populate missing fields
                if isinstance(field_type, type) and issubclass(field_type, CustomBase):
                    complete_data[field_name] = field_type()
                elif getattr(field_type, '__origin__', None) is list:
                    complete_data[field_name] = []
                elif getattr(field_type, '__origin__', None) is dict:
                    complete_data[field_name] = {}
                else:
                    complete_data[field_name] = None
        return cls.construct(**complete_data)

    def __getattr__(self, name):
        # Return None for any attribute not found.
        return None
