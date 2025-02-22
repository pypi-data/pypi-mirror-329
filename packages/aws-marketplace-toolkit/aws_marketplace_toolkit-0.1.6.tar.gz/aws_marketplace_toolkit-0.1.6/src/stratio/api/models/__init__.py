# src/stratio/api/models/__init__.py
from pydantic import BaseModel

from .cluster import ClusterItem, ClusterMetadataItem, ClusterTableData, EC2Item, EKSItem
from .customer import CustomerItem, CustomerTableData
from .logs import StreamItem

__all__ = [
    "ClusterItem",
    "ClusterMetadataItem",
    "ClusterTableData",
    "EC2Item",
    "EKSItem",
    "CustomerItem",
    "StreamItem",
    "CustomerTableData",
    "Error",
]


class Error(BaseModel):
    source: str
    error: str
