# src/stratio/api/formatters/base_formatter.py
from abc import ABC, abstractmethod

from stratio.api.models import ClusterItem, CustomerItem, CustomerTableData
from stratio.api.models.bootstrap import BootstrapItem


class BaseCustomerFormatter(ABC):
    @abstractmethod
    def format_list(self, data: list[CustomerTableData]) -> str:
        pass

    @abstractmethod
    def format_single(self, data: CustomerItem) -> str:
        pass


class BaseClusterFormatter(ABC):
    @abstractmethod
    def format_list(self, data: list[ClusterItem]) -> str:
        pass

    @abstractmethod
    def format_single(self, data: ClusterItem) -> str:
        pass


class BaseBootstrapFormatter(ABC):
    @abstractmethod
    def format_list(self, data: list[BootstrapItem]) -> str:
        pass

    @abstractmethod
    def format_single(self, data: BootstrapItem) -> str:
        pass
