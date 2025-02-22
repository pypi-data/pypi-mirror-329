# src/stratio/api/base_logs_client.py
import logging
from abc import ABC, abstractmethod
from typing import Optional

from stratio.api.models import StreamItem
from stratio.api.models.logs import MarketplaceFunction
from stratio.api.session import ApiSession
from stratio.config import Config

logging.basicConfig(level=logging.INFO)


class BaseLogsClient(ABC):
    """
    Abstract client definition for interacting with a Stratio Cluster.
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
    def list_streams(self, group: str) -> Optional[list[StreamItem]]:
        """
        Lists the streams in the given group.
        :param group:   The CloudWatch log group.
        :return:        The streams in the group.
        """
        pass

    @abstractmethod
    def filter_streams(self, group: str, including: str, limit: int) -> Optional[list[StreamItem]]:
        """
        Filters the streams in the given group to those that contain the 'including' string.
        :param group:       The CloudWatch log group.
        :param including:   The string to include in the stream contents.
        :param limit:       The maximum number of streams to return.
        :return:            The streams in the group that contain the 'including' string.
        """
        pass

    @abstractmethod
    def list_groups(self) -> Optional[list[str]]:
        """
        Lists the CloudWatch log groups for automations account.
        :return:    The CloudWatch log groups.
        """
        pass

    @abstractmethod
    def get_group(self, region: str, cluster_id: str, function: MarketplaceFunction):
        """
        Given a cluster identifier and a lambda function prefix, it searches the customer
        that owns the cluster and returns the CloudWatch log group associated with the customer and the lambda.

        :param region:          The AWS region.
        :param cluster_id:      The cluster identifier.
        :param function:        The lambda function prefix (i.e.: StartStopStratioCluster).
        :return:                The CloudWatch log group name.
        """
        pass

    @abstractmethod
    def get_groups(self, region: str, cluster_id: str, *functions: MarketplaceFunction) -> Optional[list[str]]:
        """
        Given a cluster identifier and a list of lambda function prefixes, it returns the associated cloudwatch group
        :param region:      The AWS region.
        :param cluster_id:  The cluster identifier.
        :param functions:   The lambda function prefixes.
        :return:            The CloudWatch log group names.
        """
        pass

    @abstractmethod
    def stream(self, group: str, stream: str) -> None:
        """
        Stream logs from a given CloudWatch log group and log stream (for example, Lambda logs).
        :param group: The CloudWatch log group name (e.g. "/aws/lambda/my-function").
        :param stream: The specific log stream name within the log group.
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
