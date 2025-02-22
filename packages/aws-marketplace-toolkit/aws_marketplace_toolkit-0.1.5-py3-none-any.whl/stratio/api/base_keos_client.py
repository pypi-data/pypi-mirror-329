# src/stratio/api/base_keos_client.py
import logging
from abc import ABC, abstractmethod
from typing import Optional

from stratio.api.session import ApiSession
from stratio.config import Config

logging.basicConfig(level=logging.INFO)


class BaseKeosClient(ABC):
    """
    Abstract client definition for interacting with a Stratio Cluster.
    """

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        automations_session: Optional[ApiSession] = None,
        config: Optional[Config] = None,
    ):
        self.logger = logger or self._default_logger()
        self.automations_session = automations_session
        self.config = config

    @abstractmethod
    def download_keos_workspace(self, cluster_id: str, target_dir: str = "/tmp") -> None:
        """
        Downloads the keos workspace for a given cluster.
        :param cluster_id:  The cluster identifier.
        :param target_dir:  The target directory.
        """
        pass

    @abstractmethod
    def exec_keos(self, cluster_id: str, workspace_dir: str) -> None:
        """
        Returns an interactive shell to the KEOS instance provided.
        :param cluster_id:  The cluster identifier.
        :param workspace_dir:  The workspace directory (fetch from configuration).
        """
        pass

    @staticmethod
    def _default_logger():
        logger = logging.getLogger("BaseClient")
        if not logger.handlers:
            # Prevent adding multiple handlers in interactive environments
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    class Builder:
        """
        Abstract Builder class for BaseClient.
        """

        def __init__(self):
            # public attributes
            self.logger: Optional[logging.Logger] = None

            self.seller_session: Optional[ApiSession] = None
            self.automations_session: Optional[ApiSession] = None
            self.config: Optional[Config] = None

            # private attributes
            self._aws_seller_session = None
            self._aws_automations_session = None

        def with_config(self, config: Config):
            self.config = config
            return self

        def with_logger(self, logger: logging.Logger):
            self.logger = logger
            return self

        def with_seller_session(self, session: ApiSession):
            self.seller_session = session
            return self

        def with_automations_session(self, session: ApiSession):
            self.automations_session = session
            return self

        @abstractmethod
        def build(self):
            pass
