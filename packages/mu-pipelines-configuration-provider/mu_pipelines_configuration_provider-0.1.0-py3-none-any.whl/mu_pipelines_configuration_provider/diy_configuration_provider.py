from typing import Type, TypeVar

from mu_pipelines_interfaces.config_types.connection_properties import (
    ConnectionProperties,
)
from mu_pipelines_interfaces.config_types.global_properties.global_properties import (
    GlobalProperties,
)
from mu_pipelines_interfaces.config_types.job_config import JobConfigItem
from mu_pipelines_interfaces.configuration_provider import ConfigurationProvider

TSuppFileType = TypeVar("TSuppFileType")

ConfigurationProvider = ConfigurationProvider


class DIYConfigurationProvider(ConfigurationProvider):
    _job_config: list[JobConfigItem]
    _global_properties: GlobalProperties
    _connection_config: ConnectionProperties

    def __init__(
        self,
        job_config: list[JobConfigItem],
        global_properties: GlobalProperties,
        connection_config: ConnectionProperties,
    ):
        self._job_config = job_config
        self._global_properties = global_properties
        self._connection_config = connection_config

    def load_job_supporting_artifact(
        self, relative_artifact: str, content_type: Type[TSuppFileType]
    ) -> TSuppFileType | None:
        raise NotImplementedError()

    @property
    def job_config(self) -> list[JobConfigItem]:
        return self._job_config

    @property
    def global_properties(self) -> GlobalProperties:
        return self._global_properties

    @property
    def connection_config(self) -> ConnectionProperties:
        return self._connection_config
