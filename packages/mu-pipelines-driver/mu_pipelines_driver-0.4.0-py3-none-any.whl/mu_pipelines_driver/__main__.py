from mu_pipelines_configuration_provider.configuration_factory import (
    configuration_factory,
)

from mu_pipelines_driver.run_config import run_config_from_provider


def main() -> None:
    config_provider = configuration_factory()

    run_config_from_provider(config_provider)


if __name__ == "__main__":
    main()
