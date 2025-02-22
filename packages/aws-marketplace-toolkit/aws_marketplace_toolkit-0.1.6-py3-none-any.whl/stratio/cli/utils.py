# utils.py
from typing import Optional

import typer

from stratio.api.filters import BaseCustomerFilters, Filter, Operator
from stratio.cli.config import logger


def parse_filter_option(filter_option: list[str]) -> Optional[BaseCustomerFilters]:
    """
    Parse a list of filter strings into a BaseCustomerFilters object.
    Each filter must be in the format: "field,operator,value"

    Example:
       --filter "clusterStatus eq started" --filter "customerIdentifier neq 1234"
    """
    filters = []
    for f in filter_option:
        try:
            parts = f.split(" ", 2)
            if len(parts) != 3:
                raise ValueError(f"Filter '{f}' must be in the format 'field operator value'")

            # common handling
            field, op_str, value = parts
            if op_str not in [op.value for op in Operator]:
                raise ValueError(
                    f"Operator '{op_str}' is not valid. Allowed operators: {[op.value for op in Operator]}"
                )
            # boolean handling
            if value.lower() == "true" or value.lower() == "false":
                value = value.lower() == "true"

            # list handling
            if op_str == "in":
                if "[" not in value or "]" not in value:
                    raise ValueError("Value for 'in' operator must be a list: [a,b,c]")
                value = value.strip("[]").split(",")
                value = [
                    v.strip().lower() == "true" if v.strip().lower() in ["true", "false"] else v.strip() for v in value
                ]

            filters.append(Filter(field=field, operator=op_str, value=value))
        except Exception as e:
            logger.error(f"Error parsing filter '{f}': {e}")
            raise typer.Exit(1) from e
    if filters:
        return BaseCustomerFilters(conditions=filters)
    return None


def region_callback(value: Optional[list[str]]) -> list[str]:
    """
    Callback for the region option.
    If the user did not provide a list, prompt for input.
    Also, if the value is a single comma-separated string, split it.
    """
    if not value:
        input_str = typer.prompt("Please enter region(s) (comma separated)")
        return [r.strip() for r in input_str.split(",") if r.strip()]
    # If a single string containing commas was passed, split it.
    if len(value) == 1 and "," in value[0]:
        return [r.strip() for r in value[0].split(",") if r.strip()]
    return value
