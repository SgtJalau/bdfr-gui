import dataclasses
from dataclasses import fields
from enum import Enum
from typing import Union, List


def get_field_types_of_dataclass(dataclass: dataclasses.dataclass) -> dict:
    return {field.name: field.type for field in fields(dataclass)}


def get_type_of_field_in_dataclass(dataclass: dataclasses.dataclass, field_name: str) -> type:
    return get_field_types_of_dataclass(dataclass)[field_name]


def convert_str_to_type(string: str, type_val: type):
    if type_val == str:
        return string
    elif type_val == bool:
        return string == 'True'
    elif type_val == int:
        if string == '':
            return None
        return int(string)
    elif type_val == float:
        if string == '':
            return None
        return float(string)
    elif type_val == List[str]:
        value = string.splitlines()

        # Remove empty lines
        value = [x for x in value if x]

        return value
    # Check if type_val is an enum
    elif issubclass(type_val, Enum):
        return getattr(type_val, string)
    else:
        raise Exception(f'Could not convert string to type {type_val}')
