import json
from inspect import Signature
from typing import Any, Dict, get_origin

from pydantic import BaseModel


def files_to_parameters(input_files: Dict[str, str], signature: Signature) -> Dict[str, Any]:
    parameters = {}

    for parameter in signature.parameters.values():
        parameter_name = parameter.name
        parameter_type = parameter.annotation

        # skip parameters without input files
        if parameter_name not in input_files:
            continue

        origin = get_origin(parameter_type)
        if origin:
            parameter_type = origin

        with open(input_files[parameter_name], "r") as file:
            file_content = file.read()

        parameter_value = str_to_parameter_type(file_content, parameter_type)

        parameters[parameter_name] = parameter_value

    return parameters


def str_to_parameter_type(data: str, parameter_type: Any) -> Any:
    if issubclass(parameter_type, str):
        return data

    if issubclass(parameter_type, bool):
        return bool(data)

    if issubclass(parameter_type, int):
        return int(data)

    if issubclass(parameter_type, float):
        return float(data)

    if issubclass(parameter_type, (list, dict)):
        return json.loads(data)

    if issubclass(parameter_type, BaseModel):
        return parameter_type.model_validate_json(data)

    raise ValueError(f"Type {parameter_type} is not supported")


def is_simple_type(value: Any) -> bool:
    return isinstance(value, (str, int, float, bool))
