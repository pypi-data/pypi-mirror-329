# src/stratio/api/base_cluster_client.py
import logging
from abc import ABC, abstractmethod
from typing import Optional

from stratio.api.filters import BaseCustomerFilters
from stratio.api.formatters import BaseClusterFormatter
from stratio.api.session import ApiSession
from stratio.config import Config

logging.basicConfig(level=logging.INFO)


class BaseClusterClient(ABC):
    """
    Abstract client definition for interacting with a Stratio Cluster.
    """

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        root_session: Optional[ApiSession] = None,
        seller_session: Optional[ApiSession] = None,
        automations_session: Optional[ApiSession] = None,
        config: Optional[Config] = None,
    ):
        self.logger = logger or self._default_logger()
        self.root_session = root_session
        self.seller_session = seller_session
        self.automations_session = automations_session
        self.config = config

    @abstractmethod
    def list_clusters(
        self,
        *regions: str,
        filters: Optional[BaseCustomerFilters] = None,
        formatter: Optional[BaseClusterFormatter] = None,
        max_workers: int = 10,
    ):
        """
        Lists the clusters in the given regions.
        :param regions:     The AWS regions
        :param filters:     (Optional) The filters to apply
        :param formatter:   (Optional) The formatter to use
        :param max_workers: (Optional) The maximum number of workers to use
        :return:            The clusters output depending on the kind of formatter used
        """
        pass

    @abstractmethod
    def get_cluster(self, region: str, cluster_id: str, formatter: Optional[BaseClusterFormatter] = None):
        """
        Gets the cluster information for a specific cluster.
        :param region:      The AWS region
        :param cluster_id:  The cluster identifier
        :param formatter:   (Optional) The formatter to use
        :return:            The cluster output depending on the kind of formatter used
        """
        pass

    @abstractmethod
    def start(self, region: str, cluster_id: str) -> bool:
        """
        Starts a cluster forcing the marketplace dynamodb entry to be updated.
        :param region:      The AWS region
        :param cluster_id:  The cluster identifier
        :return:            True if started, False if there was some error (check logs)
        """
        pass

    @abstractmethod
    def stop(self, region: str, cluster_id: str) -> bool:
        """
        Stops a cluster forcing the marketplace dynamodb entry to be updated.
        :param region:      The AWS region
        :param cluster_id:  The cluster identifier
        :return:            True if stopped, False if there was some error (check logs)
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
            self.root_session: Optional[ApiSession] = None
            self.seller_session: Optional[ApiSession] = None
            self.automations_session: Optional[ApiSession] = None
            self.config: Optional[Config] = None

            # private attributes
            self._aws_root_session = None
            self._aws_seller_session = None
            self._aws_automations_session = None

        def with_config(self, config: Config):
            self.config = config
            return self

        def with_logger(self, logger: logging.Logger):
            self.logger = logger
            return self

        def with_root_session(self, session: ApiSession):
            self.root_session = session
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
