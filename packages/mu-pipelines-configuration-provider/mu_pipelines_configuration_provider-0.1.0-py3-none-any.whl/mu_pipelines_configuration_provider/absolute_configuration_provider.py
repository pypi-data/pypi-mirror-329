from typing import Type, TypeVar

from mu_pipelines_interfaces.config_types.connection_properties import (
    ConnectionProperties,
)
from mu_pipelines_interfaces.config_types.global_properties.global_properties import (
    GlobalProperties,
)
from mu_pipelines_interfaces.config_types.job_config import JobConfigItem
from mu_pipelines_interfaces.configuration_provider import ConfigurationProvider

from mu_pipelines_configuration_provider.read_config import (
    read_adjacent_config_file,
    read_config,
)

TSuppFileType = TypeVar("TSuppFileType")


class AbsoluteConfigurationProvider(ConfigurationProvider):
    _job_config_path: str
    _global_properties_path: str
    _connection_config_path: str

    def __init__(
        self,
        job_config_path: str,
        global_properties_path: str,
        connection_config_path: str,
    ):
        self._job_config_path = job_config_path
        self._global_properties_path = global_properties_path
        self._connection_config_path = connection_config_path

    def load_job_supporting_artifact(
        self, relative_artifact: str, content_type: Type[TSuppFileType]
    ) -> TSuppFileType | None:
        return read_adjacent_config_file(
            self._job_config_path, relative_artifact, content_type
        )

    @property
    def job_config(self) -> list[JobConfigItem]:
        return read_config(self._job_config_path, list[JobConfigItem])

    @property
    def global_properties(self) -> GlobalProperties:
        return read_config(self._global_properties_path, GlobalProperties)

    @property
    def connection_config(self) -> ConnectionProperties:
        return read_config(self._connection_config_path, ConnectionProperties)
