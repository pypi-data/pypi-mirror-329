# src/stratio/api/config/config.py

import os
from pathlib import Path

import yaml
from pydantic import BaseModel

from .clusters_config import ClustersConfig
from .customer_config import CustomersConfig


class Config(BaseModel):
    customers: CustomersConfig
    clusters: ClustersConfig

    @classmethod
    def load_from_file(cls, file_path: str) -> "Config":
        """
        Loads configuration from a YAML file.

        :param file_path: Path to the YAML configuration file.
        :return: Config object populated with the YAML data.
        :raises FileNotFoundError: If the configuration file does not exist.
        :raises ValueError: If there's an error parsing the YAML file.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Configuration file '{file_path}' does not exist.")
        with open(file_path) as f:
            try:
                config_data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise ValueError(f"Error parsing YAML file: {e}") from e
        return cls(**config_data)

    @classmethod
    def load_from_env(cls, env: str = "dev") -> "Config":
        """
        Load configuration based on the specified environment.

        :param env: Environment name ('dev', 'pro', 'test').
        :return: Config object.
        """
        env = env.lower()
        # Determine the directory where config.py resides
        config_dir = Path(__file__).resolve().parent
        # Construct the full path to the configuration file
        config_file = config_dir / f"config_{env}.yaml"
        return cls.load_from_file(str(config_file))
