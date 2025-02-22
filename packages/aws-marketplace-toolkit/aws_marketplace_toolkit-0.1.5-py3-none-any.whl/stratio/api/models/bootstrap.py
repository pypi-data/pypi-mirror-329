# src/stratio/api/models/bootstrap.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BootstrapItem(BaseModel):
    # Mandatory attributes
    InstanceId: str
    InstanceType: str
    ImageId: str
    State: str
    AvailabilityZone: str
    LaunchTime: datetime

    # Optional attributes
    VpcId: Optional[str] = None
    SubnetId: Optional[str] = None
    PublicIpAddress: Optional[str] = None
    PrivateIpAddress: Optional[str] = None
    Tags: Optional[list[dict]] = None
