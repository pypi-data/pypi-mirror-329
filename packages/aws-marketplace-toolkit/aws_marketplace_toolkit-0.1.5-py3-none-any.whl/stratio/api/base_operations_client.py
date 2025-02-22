# src/stratio/api/base_operations_client.py
import logging
from abc import ABC, abstractmethod
from typing import Optional

from stratio.api.formatters import BaseClusterFormatter
from stratio.api.session import ApiSession
from stratio.config import Config

logging.basicConfig(level=logging.INFO)


class BaseOperationsClient(ABC):
    """
    Abstract client definition for common operations on a Stratio AWS infrastructure.
    """

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        seller_session: Optional[ApiSession] = None,
        automations_session: Optional[ApiSession] = None,
        config: Optional[Config] = None,
    ):
        self.logger = logger or self._default_logger()
        self.seller_session = seller_session
        self.automations_session = automations_session
        self.config = config

    @abstractmethod
    def list_bootstraps(self, *regions: str, formatter: Optional[BaseClusterFormatter] = None):
        """
        Lists all bootstraps in the specified regions.
        :param regions:     List of AWS regions to search for bootstraps.
        :param formatter:   (Optional) Formatter to apply to the list of bootstraps.
        :return:            List of bootstraps in the specified regions.
        """
        pass

    @abstractmethod
    def exec_bootstrap(self, region: str, bootstrap_id: str) -> None:
        """
        Initiates an SSH session to the specified EC2 instance using AWS Systems Manager Session Manager.
        :param region:          AWS region where the EC2 instance is located.
        :param bootstrap_id:    Unique identifier (Instance ID) of the EC2 instance to SSH into.
        :raises RuntimeError:   If any step in the process fails.
        """
        pass

    @abstractmethod
    def terminate_bootstrap(self, region: str, bootstrap_id: str) -> bool:
        """
        Terminates the specified EC2 bootstrap instance.
        :param region:          AWS region where the EC2 instance is located.
        :param bootstrap_id:    Unique identifier (Instance ID) of the EC2 instance to terminate.
        :return:                True if the instance was successfully terminated, False otherwise.
        """
        pass

    @abstractmethod
    def force_uninstall(self, region: str, cluster_id: str) -> bool:
        """
        Forces uninstallation only on unsubscribed clusters
        :return:        True if the cluster was requested to uninstall, False otherwise
        """
        pass

    @abstractmethod
    def get_aws_console_link(self, region: str, account_id: str):
        """
        Returns the AWS authenticated console link for the given cluster
        :param region:      The AWS region
        :param account_id:  The AWS account identifier
        :return:            The AWS authenticated console link
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
