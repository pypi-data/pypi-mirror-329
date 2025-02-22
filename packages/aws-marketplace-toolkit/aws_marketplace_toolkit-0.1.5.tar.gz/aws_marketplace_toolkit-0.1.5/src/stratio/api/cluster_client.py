# src/stratio/api/cluster_client.py
import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Optional

import boto3
from botocore.exceptions import ClientError

from stratio.api import BaseClusterClient
from stratio.api.filters import BaseCustomerFilters, Operator
from stratio.api.filters.customer_filters import Filter, build_filter_expression
from stratio.api.formatters import BaseClusterFormatter
from stratio.api.models import ClusterItem, ClusterMetadataItem, ClusterTableData, EC2Item, EKSItem, Error
from stratio.api.session import ApiSession, CredentialsApiSession, ProfileApiSession
from stratio.config import Config


class ClusterClient(BaseClusterClient):
    """
    Client for interacting with the Cluster API.
    """

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        seller_session: Optional[ApiSession] = None,
        automations_session: Optional[ApiSession] = None,
        aws_seller_session: Optional[boto3.Session] = None,
        aws_automations_session: Optional[boto3.Session] = None,
        config: Optional[Config] = None,
    ):
        super().__init__(
            logger=logger, seller_session=seller_session, automations_session=automations_session, config=config
        )
        self._aws_seller_session = aws_seller_session
        self._aws_automations_session = aws_automations_session

    def list_clusters(
        self,
        *regions: str,
        filters: Optional[BaseCustomerFilters] = None,
        formatter: Optional[BaseClusterFormatter] = None,
        max_workers: int = 10,
    ):
        if not self._aws_seller_session:
            self.logger.error("AWS session not initialized.")
            return []

        # fetch customer metadata and cluster information for each customer
        accounts_to_process = self._get_customers_metadata(list(regions), filters)
        clusters = self._get_cluster_info(accounts_to_process, max_workers) if accounts_to_process else []

        # apply formatter if defined
        if formatter:
            try:
                clusters = formatter.format_list(clusters)
            except Exception as e:
                self.logger.error(f"Error formatting customer data: {e}")
                return None

        return clusters

    def get_cluster(self, region: str, cluster_id: str, formatter: Optional[BaseClusterFormatter] = None):
        # fetch customer metadata for the requested cluster_id
        account_to_process = self._get_customers_metadata(
            [region],
            BaseCustomerFilters(
                conditions=[Filter(field="clusterIdentifier", operator=Operator.EQUALS, value=cluster_id)]
            ),
        )

        cluster = None
        if account_to_process:
            # fetch cluster
            fetched = self._get_cluster_info(account_to_process, 1)
            cluster = fetched[0] if fetched else None

            # apply formatter if defined
            if cluster and formatter:
                try:
                    cluster = formatter.format_single(cluster)
                except Exception as e:
                    self.logger.error(f"Error formatting customer data: {e}")
                    return None

        return cluster

    def start(self, region: str, cluster_id: str) -> bool:
        if not self._aws_seller_session:
            self.logger.error("AWS seller session not initialized.")
            return False

        # build filter with clusterIdentifier and clusterStatus restricted to a stopped cluster
        cluster_filter = BaseCustomerFilters(
            conditions=[
                Filter(field="clusterIdentifier", operator=Operator.EQUALS, value=cluster_id),
                Filter(field="clusterStatus", operator=Operator.EQUALS, value="stopped"),
            ]
        )
        customer: Optional[tuple[Any, str]] = self._get_customer_for_cluster(region, cluster_id, cluster_filter)
        if not customer:
            self.logger.error(f"Customer not found for cluster '{cluster_id}' in region '{region}'.")
            return False

        table = customer[0]
        customer_identifier = customer[1]
        try:
            response = table.update_item(
                Key={"customerIdentifier": customer_identifier},
                UpdateExpression="SET clusterAction = :ca",
                ExpressionAttributeValues={":ca": "start-pending"},
                ReturnValues="UPDATED_NEW",
            )
            self.logger.info(f"Update successful: {response.get('Attributes')}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating record in table '{table.name}': {e}")
            return False

    def stop(self, region: str, cluster_id: str) -> bool:
        if not self._aws_seller_session:
            self.logger.error("AWS seller session not initialized.")
            return False

        # build filter with clusterIdentifier and clusterStatus restricted to a started cluster
        cluster_filter = BaseCustomerFilters(
            conditions=[
                Filter(field="clusterIdentifier", operator=Operator.EQUALS, value=cluster_id),
                Filter(field="clusterStatus", operator=Operator.EQUALS, value="started"),
            ]
        )
        customer: Optional[tuple[Any, str]] = self._get_customer_for_cluster(region, cluster_id, cluster_filter)
        if not customer:
            self.logger.error(f"Customer not found for cluster '{cluster_id}' in region '{region}'.")
            return False

        table = customer[0]
        customer_identifier = customer[1]
        try:
            response = table.update_item(
                Key={"customerIdentifier": customer_identifier},
                UpdateExpression="SET clusterAction = :ca",
                ExpressionAttributeValues={":ca": "stop-pending"},
                ReturnValues="UPDATED_NEW",
            )
            self.logger.info(f"Update successful: {response.get('Attributes')}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating record in table '{table.name}': {e}")
            return False

    def _get_customer_for_cluster(
        self, region: str, cluster_id: str, filter: BaseCustomerFilters
    ) -> Optional[tuple[Any, str]]:
        # Fetch all tables that match the configured regex pattern
        dynamodb = self._aws_seller_session.resource("dynamodb", region_name=region)
        customer_tables = self._filter_tables_from_config(dynamodb)
        for table_name in customer_tables:
            self.logger.debug(f"Scanning table '{table_name}' for clusterIdentifier = '{cluster_id}'")

            try:
                scan_kwargs = {}
                filter_expression = build_filter_expression(filter)
                if filter_expression:
                    scan_kwargs["FilterExpression"] = filter_expression

                table = dynamodb.Table(table_name)
                response = table.scan(**scan_kwargs)
            except Exception as e:
                self.logger.error(f"Error scanning table '{table_name}': {e}")
                continue

            # Check record and save customer_identifier
            items = response.get("Items", [])
            if not items and len(items) == 0:
                self.logger.debug(f"No matching record found in table '{table_name}'.")
                continue

            record = items[0]
            customer_identifier = record.get("customerIdentifier")

            self.logger.info(
                f"Found record in table '{table_name}' with customerIdentifier = '{customer_identifier}'. Updating..."
            )

            return table, customer_identifier

        # no records where found
        return None

    def _get_cluster_info(self, customers: list[ClusterMetadataItem], max_workers: int):
        """
        Obtains information from EKS and EC2 for each customer in the list.
        :param customers:       List of ClusterMetadataItem objects.
        :param max_workers:     Maximum number of threads to use.
        :return:                List of ClusterItem objects.
        """
        output = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_account = {
                executor.submit(self._process_account, customer.provisionedAccountId, customer.installationRegion): (
                    customer
                )
                for customer in customers
            }

            for future in as_completed(future_to_account):
                customer = future_to_account[future]
                try:
                    eks, ec2 = future.result()
                    output.append(ClusterItem(metadata=customer, eks=eks, ec2=ec2))
                except Exception as e:
                    self.logger.error(f"Error processing cluster {customer.clusterIdentifier}: {e}")
                    output.append(Error(source=customer.clusterIdentifier, error=str(e)))

        return output

    def _get_customers_metadata(
        self, regions: list[str], filters: Optional[BaseCustomerFilters] = None
    ) -> list[ClusterMetadataItem]:
        """
        Fetches customer metadata from DynamoDB tables along with basic cluster status information.
        :param regions:     List of AWS regions to connect to.
        :return:            List of ClusterMetadataItem objects.
        """
        accounts_to_process = []

        try:
            for region in regions:
                # Establish connection with DynamoDB
                dynamodb = self._aws_seller_session.resource("dynamodb", region_name=region)
                self.logger.debug(f"Connected to DynamoDB in region: {region}")

                # Enumerate all DynamoDB tables for the account
                customer_tables = self._filter_tables_from_config(dynamodb)

                # Fetch customer data from every filtered table
                for table_name in customer_tables:
                    customer_data = self._get_customers_from_dynamodb(dynamodb, table_name, filters)

                    for customer in customer_data.items:
                        account_id = customer.provisionedAccountId
                        cluster_id = customer.clusterIdentifier
                        if account_id and cluster_id:
                            accounts_to_process.append(customer)

        except ClientError as c:
            self.logger.error(f"AWS ClientError listing customers: {c}")
        except re.error as re_err:
            self.logger.error(f"Regex compilation error: {re_err}")
        except Exception as e:
            self.logger.error(f"Unexpected error listing customers: {e}")

        return accounts_to_process

    def _filter_tables_from_config(self, dynamodb) -> list[str]:
        """
        Filter DynamoDB tables based on the configured regex pattern.
        :param dynamodb: DynamoDB resource object.
        :return:         List of customer table names.
        """
        # Enumerate all DynamoDB tables for the account
        pattern = re.compile(self.config.clusters.table_filter_regex)
        self.logger.debug(f"Compiled regex pattern: {self.config.customers.table_filter_regex}")
        customer_tables = []
        for table in dynamodb.tables.all():
            if pattern.match(table.name):
                customer_tables.append(table.name)
            else:
                self.logger.debug(f"Excluded Table: {table.name}")

        self.logger.debug(f"Total customer tables found: {len(customer_tables)}")
        return customer_tables

    def _get_customers_from_dynamodb(
        self, dynamodb, table_name: str, filters: Optional[BaseCustomerFilters] = None
    ) -> ClusterTableData:
        """
        Fetch all customer rows from a DynamoDB table.
        :param dynamodb:    DynamoDB resource object.
        :param table_name:  Name of the table to fetch data from.
        :return:            Dictionary containing the source table name and a list of customer items.
        """

        self.logger.debug(f"Fetching data from table: {table_name}")

        table = dynamodb.Table(table_name)

        # Initialize Scan parameters
        scan_kwargs = {}
        if filters:
            filter_expression = build_filter_expression(filters)
            if filter_expression:
                scan_kwargs["FilterExpression"] = filter_expression
                self.logger.debug(f"Applied filters: {filters}")

        response = table.scan(**scan_kwargs)
        items = [ClusterMetadataItem(**item) for item in response.get("Items", [])]

        # Handle pagination
        while "LastEvaluatedKey" in response:
            scan_kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]
            response = table.scan(**scan_kwargs)
            self.logger.debug(f"Scanned {table_name}: Retrieved {len(response.get('Items', []))} more items.")
            items.extend([ClusterMetadataItem(**item) for item in response.get("Items", [])])

        return ClusterTableData(source=table_name, items=items)

    def _process_account(self, account_id: str, region: str) -> (EKSItem, list[EKSItem]):
        session = self._get_session_for_account(account_id)

        if not session:
            raise ValueError(f"Unable to create session for account {account_id}")

        eks_status = self._get_eks_status(session, region)
        ec2_status = self._get_ec2_status(session, region)
        return eks_status, ec2_status

    def _get_session_for_account(self, account_id: str) -> Optional[boto3.Session]:
        """
        Creates a boto3 session for the provided account ID.
        This requires the root account to be properly configured.
        :param account_id:      AWS account ID.
        :return:                Boto3 session object.
        """
        try:
            root_session = None
            session_type = self.config.clusters.root.to_api_session()
            if isinstance(session_type, ProfileApiSession):
                root_session = boto3.Session(profile_name=session_type.profile_name)
            elif isinstance(session_type, CredentialsApiSession):
                root_session = boto3.Session(
                    aws_access_key_id=session_type.key_id,
                    aws_secret_access_key=session_type.secret_key,
                    region_name=session_type.region_name,
                )
            sts_client = root_session.client("sts")
            assumed_role = sts_client.assume_role(
                RoleArn=f"arn:aws:iam::{account_id}:role/OrganizationAccountAccessRole",
                RoleSessionName="ClusterClientSession",
            )
            credentials = assumed_role["Credentials"]
            return boto3.Session(
                aws_access_key_id=credentials["AccessKeyId"],
                aws_secret_access_key=credentials["SecretAccessKey"],
                aws_session_token=credentials["SessionToken"],
            )
        except ClientError as e:
            self.logger.error(f"Error assuming role for account {account_id}: {e}")
            return None

    def _get_eks_status(self, session: boto3.Session, region: str) -> Optional[EKSItem]:
        """
        Fetches the status of the EKS cluster for the provided session and region.
        :param session:     Boto3 session object (typically the customer's AWS session).
        :param region:      AWS region to query.
        :return:            EKSItem object.
        """
        eks_client = session.client("eks", region_name=region)
        try:
            clusters_response = eks_client.list_clusters()
            logging.debug(f"Clusters found: {clusters_response}")
            clusters = clusters_response.get("clusters", [])
            # we are assuming that there will be only one cluster per account
            cluster_details = None
            if clusters:
                cluster_name = clusters[0]
                cluster_info = eks_client.describe_cluster(name=cluster_name)["cluster"]
                cluster_details = EKSItem(**cluster_info)
            return cluster_details
        except ClientError as e:
            self.logger.error(f"EKS ClientError: {e}")
            return None
        except Exception as e:
            self.logger.error(f"EKS unhandled error: {e}")
            return None

    def _get_ec2_status(self, session: boto3.Session, region: str) -> Optional[list[EC2Item]]:
        """
        Fetches all running EC2 instances for the provided session and region.
        :param session:     Boto3 session object (typically the customer's AWS session).
        :param region:      AWS region to query.
        :return:            List of EC2Item objects.
        """
        ec2_client = session.client("ec2", region_name=region)
        try:
            reservations = ec2_client.describe_instances()
            instances = [
                EC2Item(**instance)
                for reservation in reservations["Reservations"]
                for instance in reservation["Instances"]
            ]
            return instances
        except ClientError as e:
            self.logger.error(f"EC2 ClientError: {e}")
            return None

    @staticmethod
    def _initialize_aws_session(session: Optional[ApiSession]) -> Optional[boto3.Session]:
        if not session:
            return None
        if isinstance(session, ProfileApiSession):
            return boto3.Session(profile_name=session.profile_name)
        elif isinstance(session, CredentialsApiSession):
            return boto3.Session(
                aws_access_key_id=session.key_id,
                aws_secret_access_key=session.secret_key,
                region_name=session.region_name,
            )
        return None

    class Builder(BaseClusterClient.Builder):
        def build(self):
            # Determine which session to use:
            # 1. Use the session provided via with_session
            # 2. Otherwise, use the session from config.clusters.session
            seller_session = self.seller_session
            automations_session = self.automations_session
            if not seller_session and self.config and self.config.clusters.seller:
                seller_session = self.config.clusters.seller.to_api_session()
            if not automations_session and self.config and self.config.clusters.automations:
                automations_session = self.config.clusters.automations.to_api_session()

            aws_seller_session = ClusterClient._initialize_aws_session(seller_session)
            aws_automations_session = ClusterClient._initialize_aws_session(automations_session)
            return ClusterClient(
                logger=self.logger,
                seller_session=seller_session,
                automations_session=automations_session,
                aws_seller_session=aws_seller_session,
                aws_automations_session=aws_automations_session,
                config=self.config,
            )
