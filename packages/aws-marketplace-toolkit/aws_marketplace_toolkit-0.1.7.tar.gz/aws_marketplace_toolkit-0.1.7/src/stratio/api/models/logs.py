from enum import Enum
from typing import Optional

from pydantic import BaseModel


class StreamItem(BaseModel):
    streamName: str
    lastEventTime: Optional[int] = None


class MarketplaceFunction(str, Enum):
    START_STOP = "start_stop_stratio_cluster_prefix"
    START_APPLICATIONS = "start_stratio_applications_prefix"
    UNINSTALL = "remove_stratio_cluster_prefix"
