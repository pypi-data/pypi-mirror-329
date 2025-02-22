# src/stratio/api/operations_client.py
import json
import logging
import os
import re
import urllib
from typing import Optional

import boto3
import requests
from botocore.exceptions import ClientError

from stratio.api import BaseClusterClient, BaseOperationsClient
from stratio.api.filters import BaseCustomerFilters, Filter, Operator
from stratio.api.filters.customer_filters import build_filter_expression
from stratio.api.formatters import BaseBootstrapFormatter
from stratio.api.models.bootstrap import BootstrapItem
from stratio.api.session import ApiSession, CredentialsApiSession, ProfileApiSession
from stratio.config import Config
from stratio.utils import execute_command


class OperationsClient(BaseOperationsClient):
    """
    Client for cluster-related operations.
    """

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        root_session: Optional[ApiSession] = None,
        seller_session: Optional[ApiSession] = None,
        automations_session: Optional[ApiSession] = None,
        aws_root_session: Optional[boto3.Session] = None,
        aws_seller_session: Optional[boto3.Session] = None,
        aws_automations_session: Optional[boto3.Session] = None,
        config: Optional[Config] = None,
    ):
        super().__init__(
            logger=logger, seller_session=seller_session, automations_session=automations_session, config=config
        )
        self._aws_root_session = aws_root_session
        self._aws_seller_session = aws_seller_session
        self._aws_automations_session = aws_automations_session

    def list_bootstraps(
        self,
        *regions: str,
        formatter: Optional[BaseBootstrapFormatter] = None,
    ) -> Optional[list[BootstrapItem]]:
        if not self._aws_automations_session:
            self.logger.error("AWS session not initialized.")
            return []

        bootstraps = []
        for region in regions:
            self.logger.info(f"Searching for bootstraps in region: {region}")
            try:
                ec2_client = self._aws_automations_session.client("ec2", region_name=region)
                response = ec2_client.describe_instances()
                self.logger.debug(f"EC2 DescribeInstances response: {response}")
                for reservation in response.get("Reservations", []):
                    for instance in reservation.get("Instances", []):
                        bootstrap = BootstrapItem(
                            InstanceId=instance["InstanceId"],
                            InstanceType=instance["InstanceType"],
                            ImageId=instance["ImageId"],
                            State=instance["State"]["Name"],
                            AvailabilityZone=instance["Placement"]["AvailabilityZone"],
                            LaunchTime=instance["LaunchTime"],
                            VpcId=instance.get("VpcId"),
                            SubnetId=instance.get("SubnetId"),
                            PublicIpAddress=instance.get("PublicIpAddress"),
                            PrivateIpAddress=instance.get("PrivateIpAddress"),
                            Tags=instance.get("Tags"),
                        )
                        bootstraps.append(bootstrap)

            except ClientError as e:
                self.logger.error(f"Error fetching bootstraps in region {region}: {e}")
                continue
            except Exception as e:
                self.logger.error(f"Unexpected error in region {region}: {e}")
                continue

        if formatter:
            try:
                bootstraps = formatter.format_list(bootstraps)
            except Exception as e:
                self.logger.error(f"Error formatting bootstraps: {e}")
                return None

        return bootstraps if bootstraps else None

    def exec_bootstrap(self, region: str, bootstrap_id: str) -> None:
        if not self._aws_automations_session:
            self.logger.error("AWS automations session not initialized.")
            return None

        try:
            ssm_client = self._aws_automations_session.client("ssm", region_name=region)
            self.logger.info(
                f"Verifying if instance {bootstrap_id} is managed by AWS Systems Manager in region {region}."
            )

            # Verify if the instance is managed by SSM
            response = ssm_client.describe_instance_information(
                Filters=[
                    {"Key": "InstanceIds", "Values": [bootstrap_id]},
                ]
            )
            instance_info = response.get("InstanceInformationList", [])
            if not instance_info:
                self.logger.error(
                    f"Instance {bootstrap_id} is not managed by AWS Systems Manager. "
                    "Ensure that the SSM Agent is installed and the IAM role is attached correctly."
                )
                raise RuntimeError(f"Instance {bootstrap_id} is not managed by AWS Systems Manager.")

            self.logger.info(f"Instance {bootstrap_id} is managed by AWS Systems Manager. Initiating SSH session.")

            # Construct the AWS CLI command to start a Session Manager session
            aws_cli_command = [
                "aws",
                "ssm",
                "start-session",
                "--target",
                bootstrap_id,
                "--region",
                region,
            ]

            self.logger.debug(f"Executing AWS CLI command: {' '.join(aws_cli_command)}")

            # Extract credentials from the boto3 session
            credentials = self._aws_automations_session.get_credentials()
            if not credentials:
                self.logger.error("No credentials found in the AWS automations session.")
                raise RuntimeError("AWS credentials are not available.")

            # Refresh credentials if needed
            credentials = credentials.get_frozen_credentials()

            # Prepare environment variables for the subprocess
            env = os.environ.copy()
            env["AWS_ACCESS_KEY_ID"] = credentials.access_key
            env["AWS_SECRET_ACCESS_KEY"] = credentials.secret_key
            env["AWS_SESSION_TOKEN"] = credentials.token
            execute_command(aws_cli_command, self.logger, environment=env)

            self.logger.info(f"SSM session for instance {bootstrap_id} has been closed.")

        except ClientError as e:
            self.logger.error(f"AWS ClientError while initiating SSM session for instance {bootstrap_id}: {e}")
            raise RuntimeError(f"AWS ClientError while initiating SSM session: {e}") from e
        except FileNotFoundError as e:
            self.logger.error(
                "AWS CLI not found. Please ensure that the AWS CLI is installed and available in your PATH."
            )
            raise RuntimeError("AWS CLI not found. Please install the AWS CLI and ensure it's in your PATH.") from e
        except Exception as e:
            self.logger.error(f"Unexpected error during SSM session initiation for instance {bootstrap_id}: {e}")
            raise RuntimeError(f"Unexpected error during SSM session initiation: {e}") from e

    def terminate_bootstrap(self, region: str, bootstrap_id: str) -> bool:
        """
        Terminates and removes the EC2 instance identified by bootstrap_id in the specified region.

        :param region:          AWS region where the EC2 instance is located.
        :param bootstrap_id:    Unique identifier (Instance ID) of the EC2 instance to terminate.
        :return:                True if termination was successful, False otherwise.
        """
        if not self._aws_automations_session:
            self.logger.error("AWS automations session not initialized.")
            return False

        try:
            ec2_client = self._aws_automations_session.client("ec2", region_name=region)
            self.logger.info(f"Initiating termination of EC2 instance {bootstrap_id} in region {region}.")

            # Terminate the instance
            response = ec2_client.terminate_instances(InstanceIds=[bootstrap_id])
            self.logger.debug(f"TerminateInstances response: {response}")

            # Check the response to confirm termination
            terminating_instances = response.get("TerminatingInstances", [])
            for instance in terminating_instances:
                if instance.get("InstanceId") == bootstrap_id:
                    current_state = instance.get("CurrentState", {}).get("Name")
                    previous_state = instance.get("PreviousState", {}).get("Name")
                    self.logger.info(f"Instance {bootstrap_id} transitioned from {previous_state} to {current_state}.")
                    if current_state in ["shutting-down", "terminated"]:
                        self.logger.info(f"Instance {bootstrap_id} termination initiated successfully.")
                        return True
                    else:
                        self.logger.warning(f"Instance {bootstrap_id} is in state: {current_state}.")
                        return False

            self.logger.error(f"No termination information found for instance {bootstrap_id}.")
            return False

        except ClientError as e:
            self.logger.error(f"AWS ClientError while terminating instance {bootstrap_id}: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error while terminating instance {bootstrap_id}: {e}")
            return False

    def force_uninstall(self, region: str, cluster_id: str) -> bool:
        """
        Forces uninstallation only on unsubscribed clusters.
        This method will scan through all DynamoDB tables (filtered by the configured regex)
        to find a record whose 'clusterIdentifier' matches the provided cluster_id.
        Once found, it will update the record with 'uninstall-pending' action.

        :param region: AWS region to scan for the cluster record.
        :param cluster_id: The cluster identifier to search for.
        :return: True if the record was found and updated; False otherwise.
        """
        if not self._aws_seller_session:
            self.logger.error("AWS seller session not initialized.")
            return False

        # Fetch all tables that match the configured regex pattern
        dynamodb = self._aws_seller_session.resource("dynamodb", region_name=region)
        customer_tables = self._filter_tables_from_config(dynamodb)

        for table_name in customer_tables:
            self.logger.debug(f"Scanning table '{table_name}' for clusterIdentifier = '{cluster_id}'")
            by_cluster_id = BaseCustomerFilters(
                conditions=[
                    Filter(field="clusterIdentifier", operator=Operator.EQUALS, value=cluster_id),
                    Filter(field="successfullySubscribed", operator=Operator.EQUALS, value=False),
                ]
            )

            try:
                scan_kwargs = {}
                filter_expression = build_filter_expression(by_cluster_id)
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
                self.logger.debug(f"No matching record found in table '{table.name}'.")
                continue

            record = items[0]
            customer_identifier = record.get("customerIdentifier")

            self.logger.info(
                f"Found record in table '{table_name}' with customerIdentifier = '{customer_identifier}'. Updating..."
            )

            try:
                update_response = table.update_item(
                    Key={"customerIdentifier": customer_identifier},
                    UpdateExpression="SET installationAction = :ia, successfullyInstalled = :si REMOVE clusterAction, installationPhase",
                    ExpressionAttributeValues={
                        ":ia": "uninstall-pending",
                        ":si": True,
                    },
                    ReturnValues="UPDATED_NEW",
                )
                self.logger.info(f"Update successful: {update_response.get('Attributes')}")
                return True
            except Exception as e:
                self.logger.error(f"Error updating record in table '{table.name}': {e}")
                return False

        self.logger.error(f"No record found with clusterIdentifier = '{cluster_id}' in any table.")
        return False

    def get_aws_console_link(self, account_id: str, region: str = "us-east-1") -> Optional[str]:
        if not self._aws_root_session:
            self.logger.error("Failed to initialize root boto3 session")
            return None

        try:
            # Assume the OrganizationAccountAccessRole in the target account.
            sts_client = self._aws_root_session.client("sts", region_name=region)
            role_arn = f"arn:aws:iam::{account_id}:role/OrganizationAccountAccessRole"
            self.logger.info(f"Assuming role {role_arn} using root session.")
            assumed_role = sts_client.assume_role(RoleArn=role_arn, RoleSessionName="OperationsConsoleLinkSession")
            credentials = assumed_role["Credentials"]

            # Create a new boto3 session using the assumed role credentials.
            assumed_session = boto3.Session(
                aws_access_key_id=credentials["AccessKeyId"],
                aws_secret_access_key=credentials["SecretAccessKey"],
                aws_session_token=credentials["SessionToken"],
                region_name=region,
            )

            return self._generate_aws_console_link(assumed_session)

        except ClientError as e:
            self.logger.error(f"AWS ClientError while generating console link: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error generating AWS console link: {e}")
            return None

    def get_aws_profile_link(self, aws_profile: str, region: str = "us-east-1") -> Optional[str]:
        if not self._aws_root_session:
            self.logger.error("Failed to initialize root boto3 session")
            return None

        try:
            session = boto3.Session(profile_name=aws_profile)
            if not session:
                self.logger.error(f"Failed to initialize boto3 session for profile '{aws_profile}'")
                return None

            return self._generate_aws_console_link(session)

        except ClientError as e:
            self.logger.error(f"AWS ClientError while generating console link: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error generating AWS console link: {e}")
            return None

    def _generate_aws_console_link(self, assumed_session):
        creds_obj = assumed_session.get_credentials()
        if not creds_obj:
            self.logger.error("Unable to obtain credentials from the assumed session.")
            return None
        frozen_creds = creds_obj.get_frozen_credentials()
        session_credentials = {
            "sessionId": frozen_creds.access_key,
            "sessionKey": frozen_creds.secret_key,
            "sessionToken": frozen_creds.token,
        }
        json_credentials = json.dumps(session_credentials)
        self.logger.debug(f"Temporary credentials JSON: {json_credentials}")
        # Define session duration in seconds (e.g., 12 hours).
        session_duration = 43200
        encoded_session = urllib.parse.quote_plus(json_credentials)
        federation_endpoint = (
            f"https://signin.aws.amazon.com/federation?Action=getSigninToken"
            f"&SessionDuration={session_duration}&Session={encoded_session}"
        )
        self.logger.debug(f"Federation endpoint URL: {federation_endpoint}")
        # Request a sign-in token from the AWS federation endpoint.
        response = requests.get(federation_endpoint)
        response.raise_for_status()
        token_response = response.json()
        signin_token = token_response.get("SigninToken")
        if not signin_token:
            self.logger.error("No SigninToken found in the federation response.")
            return None
        self.logger.debug(f"Received SigninToken: {signin_token}")
        # Build the final login URL.
        destination = urllib.parse.quote_plus("https://console.aws.amazon.com/")
        issuer = urllib.parse.quote_plus("Stratio Marketplace API")
        login_url = (
            f"https://signin.aws.amazon.com/federation?Action=login"
            f"&Issuer={issuer}&Destination={destination}&SigninToken={signin_token}"
        )
        self.logger.info("Successfully generated AWS console login URL.")
        return login_url

    def _filter_tables_from_config(self, dynamodb):
        """
        Filter DynamoDB tables based on the configured regex pattern.
        :param dynamodb: DynamoDB resource object.
        :return:         List of customer table names.
        """

        # Enumerate all DynamoDB tables for the account
        pattern = re.compile(self.config.clusters.table_filter_regex)
        self.logger.debug(f"Compiled regex pattern: {self.config.clusters.table_filter_regex}")
        customer_tables = []
        for table in dynamodb.tables.all():
            if pattern.match(table.name):
                customer_tables.append(table.name)
            else:
                self.logger.debug(f"Excluded Table: {table.name}")

        self.logger.debug(f"Total customer tables found: {len(customer_tables)}")
        return customer_tables

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
            root_session = self.root_session
            seller_session = self.seller_session
            automations_session = self.automations_session
            if not root_session and self.config and self.config.clusters.root:
                root_session = self.config.clusters.root.to_api_session()
            if not seller_session and self.config and self.config.clusters.seller:
                seller_session = self.config.clusters.seller.to_api_session()
            if not automations_session and self.config and self.config.clusters.automations:
                automations_session = self.config.clusters.automations.to_api_session()

            aws_root_session = OperationsClient._initialize_aws_session(root_session)
            aws_seller_session = OperationsClient._initialize_aws_session(seller_session)
            aws_automations_session = OperationsClient._initialize_aws_session(automations_session)
            return OperationsClient(
                logger=self.logger,
                root_session=root_session,
                seller_session=seller_session,
                automations_session=automations_session,
                aws_root_session=aws_root_session,
                aws_seller_session=aws_seller_session,
                aws_automations_session=aws_automations_session,
                config=self.config,
            )
