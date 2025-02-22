# src/stratio/api/formatters/customer_formatters.py
import json
import re
from typing import Optional

from tabulate import tabulate

from stratio.api.models import CustomerItem, CustomerTableData

from .base_formatter import BaseCustomerFormatter


class CLIFormatter(BaseCustomerFormatter):
    def __init__(self, exclude: Optional[list[str]] = None):
        """
        Initialize the CLIFormatter.

        :param exclude: Optional list of CustomerItem attribute names to exclude from the output.
        """
        self.exclude = set(exclude) if exclude else set()

        # Validate that excluded fields exist in CustomerItem
        all_fields = set(CustomerItem.model_fields.keys())
        invalid_excludes = self.exclude - all_fields
        if invalid_excludes:
            raise ValueError(f"Invalid fields to exclude: {invalid_excludes}")

    def format_list(self, data: list[CustomerTableData]) -> str:
        if not data:
            return "No customer data available."

        # handle user-requested exclusions and logic-mandatory exclusions
        excluded = set() if self.exclude is None else self.exclude
        # "installation" will combine installationAction and successfullyInstalled
        excluded.add("installationAction")
        excluded.add("installationPhase")
        excluded.add("installationStatus")
        excluded.add("successfullyInstalled")
        excluded.add("clusterStatus")
        excluded.add("clusterAction")
        excluded.add("bucketSecretArn")
        excluded.add("contactPhone")
        excluded.add("isFreeTrialTermPresent")
        excluded.add("productCode")
        excluded.add("subscriptionAction")
        excluded.add("created")
        excluded.add("installed")
        excluded.add("adminUsername")
        excluded.add("customerIdentifier")
        excluded.add("companyName")
        excluded.add("customerAWSAccountID")

        # Dynamically retrieve all fields from CustomerItem, excluding specified fields
        customer_fields = [field for field in CustomerItem.model_fields if field not in self.exclude]

        # Combine 'Source' with CustomerItem fields for headers
        headers = ["Source"] + list(_camel_case_to_title(field) for field in customer_fields)

        table = []
        for table_data in data:
            for item in table_data.items:
                # Convert CustomerItem to a dict, ensuring all fields are included
                item_dict = item.model_dump()
                # Create a row starting with the source
                row = [table_data.source.replace("MarketplaceSubscribers", "")]
                # Append each field's value, handling missing fields gracefully
                for field in customer_fields:
                    value = item_dict.get(field, "")
                    # If the value is a boolean, convert it to 'Yes'/'No' for better readability
                    if isinstance(value, bool):
                        value = "Yes" if value else "No"
                    row.append(value)
                table.append(row)

        return tabulate(table, headers=headers, tablefmt="github")

    def format_single(self, data: CustomerItem) -> str:
        if not data:
            return "No customer data available."

        customer_fields = [field for field in CustomerItem.model_fields if field not in self.exclude]
        headers = list(_camel_case_to_title(field) for field in customer_fields)
        table = []
        item_dict = data.model_dump()
        row = []

        # Append each field's value, handling missing fields gracefully
        for field in customer_fields:
            value = item_dict.get(field, "")
            # If the value is a boolean, convert it to 'Yes'/'No' for better readability
            if isinstance(value, bool):
                value = "Yes" if value else "No"
            row.append(value)
        table.append(row)

        return tabulate(table, headers=headers, tablefmt="github")


class JSONFormatter(BaseCustomerFormatter):
    def format_single(self, data: CustomerItem) -> str:
        return json.dumps(data.model_dump(), indent=2)

    def format_list(self, data: list[CustomerTableData]) -> str:
        return json.dumps([item.dict() for item in data], indent=2)


def _camel_case_to_title(text: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", " ", text).title().replace("I D", "Id").title()
