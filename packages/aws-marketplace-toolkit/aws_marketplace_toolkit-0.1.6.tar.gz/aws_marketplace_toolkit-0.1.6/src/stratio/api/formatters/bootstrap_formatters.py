# src/stratio/api/formatters/bootstrap_formatters.py
import json
import re
from datetime import datetime
from typing import Optional

from tabulate import tabulate

from stratio.api.models.bootstrap import BootstrapItem

from .base_formatter import BaseBootstrapFormatter


class CLIFormatter(BaseBootstrapFormatter):
    def __init__(self, exclude: Optional[list[str]] = None):
        """
        Initialize the CLIFormatter.

        :param exclude: Optional list of BootstrapItem attribute names to exclude from the output.
        """
        self.exclude = set(exclude) if exclude else set()

    def format_list(self, data: list[BootstrapItem]) -> str:
        if not data:
            return "No bootstrap data available."

        # handle user-requested exclusions and logic-mandatory exclusions
        excluded = set() if self.exclude is None else self.exclude
        # "installation" will combine installationAction and successfullyInstalled
        excluded.add("InstanceType")
        excluded.add("SubnetId")
        excluded.add("VpcId")
        excluded.add("Tags")
        excluded.add("PublicIpAddress")

        # Dynamically retrieve all fields from BootstrapItem, excluding specified fields
        bootstrap_fields = [field for field in BootstrapItem.model_fields if field not in excluded]

        # Define headers by converting camelCase to Title Case
        headers = [self._camel_case_to_title(field) for field in bootstrap_fields] + ["Owner", "Cluster Id"]

        table = []
        for bootstrap in data:
            item_dict = bootstrap.model_dump()
            row = []

            for field in bootstrap_fields:
                value = item_dict.get(field, "")
                # Convert booleans to 'Yes'/'No' for better readability
                if isinstance(value, bool):
                    value = "Yes" if value else "No"
                # Format datetime objects as strings if necessary
                if isinstance(value, datetime):
                    value = value.isoformat()
                row.append(value)

            owner = next(
                (tag["Value"] for tag in item_dict.get("Tags", []) if tag["Key"] == "keos.stratio.com/customer_email"),
                "",
            )
            cluster_name = next(
                (tag["Value"] for tag in item_dict.get("Tags", []) if tag["Key"] == "keos.stratio.com/cluster_name"),
                "",
            )
            row.append(owner)
            row.append(cluster_name)

            table.append(row)

        return tabulate(table, headers=headers, tablefmt="github")

    def format_single(self, data: BootstrapItem) -> str:
        return self.format_list([data])

    @staticmethod
    def _camel_case_to_title(text: str) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", " ", text).title()


class JSONFormatter(BaseBootstrapFormatter):
    def format_list(self, data: list[BootstrapItem]) -> str:
        return json.dumps([item.model_dump() for item in data], default=str, indent=2)

    def format_single(self, data: BootstrapItem) -> str:
        return json.dumps(data.model_dump(), default=str, indent=2)
