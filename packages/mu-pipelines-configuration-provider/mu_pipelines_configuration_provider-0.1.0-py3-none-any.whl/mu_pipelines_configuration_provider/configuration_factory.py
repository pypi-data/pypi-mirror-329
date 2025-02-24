import argparse

from mu_pipelines_interfaces.configuration_provider import ConfigurationProvider

from mu_pipelines_configuration_provider.absolute_configuration_provider import (
    AbsoluteConfigurationProvider,
)


def configuration_factory() -> ConfigurationProvider:
    parser = argparse.ArgumentParser()
    parser.add_argument("job-config", type=str, help="path to job config")
    parser.add_argument(
        "--global-properties", type=str, help="path to global-properties"
    )
    parser.add_argument(
        "--connection-properties", type=str, help="path to connection-properties"
    )

    args = parser.parse_args()

    return AbsoluteConfigurationProvider(
        getattr(args, "job-config"),
        getattr(args, "global_properties"),
        getattr(args, "connection_properties"),
    )
