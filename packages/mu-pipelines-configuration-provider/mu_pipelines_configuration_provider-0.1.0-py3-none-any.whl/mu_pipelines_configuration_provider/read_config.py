import json
import os
from typing import Type, TypeVar

TConfig = TypeVar("TConfig")


def read_config(file_location: str, ConfigType: Type[TConfig]) -> TConfig:
    with open(file_location) as file:
        if ConfigType == Type[str]:
            return ConfigType(file.read())  # type: ignore [call-arg]
        else:
            config: dict | list[dict] = json.load(file)
            return ConfigType(config)  # type: ignore [call-arg]


def read_adjacent_config_file(
    reference_file_location: str, relative_file_location: str, ConfigType: Type[TConfig]
) -> TConfig:
    pwd = os.path.dirname(reference_file_location)
    adjacent_file_path = os.path.join(pwd, relative_file_location)
    return read_config(adjacent_file_path, ConfigType)
