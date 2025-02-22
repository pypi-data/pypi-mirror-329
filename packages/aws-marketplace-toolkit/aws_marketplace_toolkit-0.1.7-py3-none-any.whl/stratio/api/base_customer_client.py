# src/stratio/api/base_customer_client.py
import logging
from abc import ABC, abstractmethod
from typing import Optional

from stratio.api.filters import BaseCustomerFilters
from stratio.api.formatters import BaseCustomerFormatter
from stratio.api.session import ApiSession
from stratio.api.transformers import BaseCustomerTransformer
from stratio.config import Config

logging.basicConfig(level=logging.INFO)


class BaseCustomerClient(ABC):
    """
    Abstract client definition for interacting with the customer information.
    """

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        session: Optional[ApiSession] = None,
        config: Optional[Config] = None,
    ):
        self.logger = logger or self._default_logger()
        self.session = session
        self.config = config

    @abstractmethod
    def get_customer(
        self, region: str, table_name: str, customer_id: str, formatter: Optional[BaseCustomerFormatter] = None
    ):
        """
        Returns a customer given a region, table name and customer id.
        :param region:      The AWS region.
        :param table_name:  The table name.
        :param customer_id: The customer id.
        :param formatter:   (Optional) The formatter to use.
        :return:            The customer output depending on the kind of formatter used.
        """
        pass

    @abstractmethod
    def list_customers(
        self,
        *regions: str,
        filters: Optional[BaseCustomerFilters] = None,
        transformer: BaseCustomerTransformer = None,
        formatter: Optional[BaseCustomerFormatter] = None,
    ):
        """
        Lists the customers in the given regions.
        :param regions:     The AWS regions.
        :param filters:     (Optional) The filters to apply.
        :param transformer: (Optional) The transformer to use.
        :param formatter:   (Optional) The formatter to use.
        :return:            The customers output depending on the kind of formatter used.
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
            self.session: Optional[ApiSession] = None
            self.config: Optional[Config] = None

            # private attributes
            self._aws_session = None

        def with_config(self, config: Config):
            self.config = config
            return self

        def with_logger(self, logger: logging.Logger):
            self.logger = logger
            return self

        def with_session(self, session: ApiSession):
            self.session = session
            return self

        @abstractmethod
        def build(self):
            pass
