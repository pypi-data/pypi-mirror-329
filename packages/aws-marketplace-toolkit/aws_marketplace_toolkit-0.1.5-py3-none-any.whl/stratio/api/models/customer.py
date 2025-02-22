# src/stratio/api/models/customer.py
from typing import Optional

from pydantic import BaseModel


class CustomerItem(BaseModel):
    # mandatory attributes
    customerIdentifier: str
    productCode: str
    # optional attributes
    customerAWSAccountID: Optional[str] = None
    clusterIdentifier: Optional[str] = None
    provisionedAccountId: Optional[str] = None
    adminUsername: Optional[str] = None
    bucketSecretArn: Optional[str] = None
    companyName: Optional[str] = None
    contactEmail: Optional[str] = None
    contactPhone: Optional[str] = None
    created: Optional[str] = None
    installationAction: Optional[str] = None
    installationRegion: Optional[str] = None
    installationPhase: Optional[str] = None
    subscriptionAction: Optional[str] = None
    subscriptionExpired: Optional[bool] = None
    successfullyInstalled: Optional[bool] = None
    successfullyRegistered: Optional[bool] = None
    successfullySubscribed: Optional[bool] = None
    isFreeTrialTermPresent: Optional[bool] = None


class CustomerTableData(BaseModel):
    source: str
    items: list[CustomerItem]
    error: Optional[str] = None
