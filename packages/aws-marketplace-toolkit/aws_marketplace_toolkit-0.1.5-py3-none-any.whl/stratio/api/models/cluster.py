# src/stratio/api/models/cluster.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EC2Item(BaseModel):
    # mandatory attributes
    ImageId: str
    InstanceId: str
    InstanceType: str
    State: dict

    # optional attributes
    VpcId: Optional[str] = None
    SubnetId: Optional[str] = None
    LaunchTime: Optional[datetime] = None
    Placement: Optional[dict] = None
    Tags: Optional[list[dict]] = None


class EKSItem(BaseModel):
    # mandatory attributes
    name: str
    arn: str
    createdAt: datetime
    version: str
    roleArn: str
    status: str
    # optional attributes
    endpoint: Optional[str] = None
    health: Optional[dict] = None
    platformVersion: Optional[str] = None


class ClusterMetadataItem(BaseModel):
    # mandatory attributes
    customerIdentifier: str
    # optional attributes
    clusterIdentifier: Optional[str] = None
    provisionedAccountId: Optional[str] = None
    contactEmail: Optional[str] = None
    installationAction: Optional[str] = None
    installationRegion: Optional[str] = None
    installationPhase: Optional[str] = None
    clusterStatus: Optional[str] = None
    clusterAction: Optional[str] = None
    successfullyInstalled: Optional[bool] = None
    created: Optional[str] = None
    k8sVersion: Optional[str] = None
    keosVersion: Optional[str] = None
    universeVersion: Optional[str] = None


class ClusterItem(BaseModel):
    metadata: ClusterMetadataItem
    eks: Optional[EKSItem] = None
    ec2: list[EC2Item]


class ClusterTableData(BaseModel):
    source: str
    items: list[ClusterMetadataItem]
    error: Optional[str] = None
