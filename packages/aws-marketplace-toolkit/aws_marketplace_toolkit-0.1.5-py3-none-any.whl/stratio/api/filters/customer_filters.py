# src/stratio/api/filters/customer_filters.py
from enum import Enum
from typing import Any, Optional

from boto3.dynamodb.conditions import Attr
from pydantic import BaseModel, field_validator


class Operator(str, Enum):
    EQUALS = "eq"
    NOT_EQUALS = "neq"
    GREATER_THAN = "gt"
    LESS_THAN = "lt"
    GREATER_THAN_OR_EQUAL = "gte"
    LESS_THAN_OR_EQUAL = "lte"
    CONTAINS = "contains"
    BEGINS_WITH = "begins_with"
    IN = "in"


class Filter(BaseModel):
    field: str
    operator: Operator
    value: Any

    @field_validator("operator")
    def validate_operator(cls, v):
        valid_operators = set(item.value for item in Operator)
        if v not in valid_operators:
            raise ValueError(f"Unsupported operator: {v}")
        return v


class BaseCustomerFilters(BaseModel):
    conditions: list[Filter]


def build_filter_expression(filters: BaseCustomerFilters) -> Optional[Any]:
    """
    Translates CustomerFilters into a DynamoDB FilterExpression.

    :param filters: CustomerFilters instance containing filter conditions.
    :return: FilterExpression or None if no conditions are provided.
    """
    expressions = []
    for condition in filters.conditions:
        attr = Attr(condition.field)
        if condition.operator == Operator.EQUALS:
            expressions.append(attr.eq(condition.value))
        elif condition.operator == Operator.NOT_EQUALS:
            expressions.append(attr.ne(condition.value))
        elif condition.operator == Operator.GREATER_THAN:
            expressions.append(attr.gt(condition.value))
        elif condition.operator == Operator.LESS_THAN:
            expressions.append(attr.lt(condition.value))
        elif condition.operator == Operator.GREATER_THAN_OR_EQUAL:
            expressions.append(attr.gte(condition.value))
        elif condition.operator == Operator.LESS_THAN_OR_EQUAL:
            expressions.append(attr.lte(condition.value))
        elif condition.operator == Operator.CONTAINS:
            expressions.append(attr.contains(condition.value))
        elif condition.operator == Operator.BEGINS_WITH:
            expressions.append(attr.begins_with(condition.value))
        elif condition.operator == Operator.IN:
            if not isinstance(condition.value, list):
                raise ValueError("Value for 'in' operator must be a list.")
            expressions.append(attr.is_in(condition.value))
        else:
            raise ValueError(f"Unsupported operator: {condition.operator}")

    if not expressions:
        return None

    # Combine all expressions with AND logic
    filter_expression = expressions[0]
    for expr in expressions[1:]:
        filter_expression = filter_expression & expr

    return filter_expression
