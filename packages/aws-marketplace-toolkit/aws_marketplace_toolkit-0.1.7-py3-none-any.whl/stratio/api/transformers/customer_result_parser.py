# src/stratio/utils/customer_result_parser.py
from abc import ABC, abstractmethod
from collections import defaultdict

from stratio.api.models import CustomerTableData


class BaseCustomerTransformer(ABC):
    """
    Abstract base class for customer-related result transformers.
    """

    @abstractmethod
    def parse(self, data: list[CustomerTableData]) -> list[CustomerTableData]:
        """
        Parse the list of CustomerTableData and return the desired format.

        :param data: List of CustomerTableData instances.
        :return: Parsed result in desired format.
        """
        pass


class GroupByProductCode(BaseCustomerTransformer):
    """
    Parser that groups customers by their productCode and returns a list of CustomerTableData.
    Each CustomerTableData's source is the productCode, and items are the customers with that productCode.
    """

    def parse(self, data: list[CustomerTableData]) -> list[CustomerTableData]:
        grouped_data = defaultdict(list)
        for table_data in data:
            for item in table_data.items:
                if item.productCode:
                    grouped_data[item.productCode].append(item)
                else:
                    grouped_data["Unknown"].append(item)

        # Transform the grouped data into a list of CustomerTableData
        parsed_result = [
            CustomerTableData(source=product_code, items=items) for product_code, items in grouped_data.items()
        ]

        return parsed_result
