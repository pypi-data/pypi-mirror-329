# src/stratio/api/logs_client.py
import logging
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from stratio.api import BaseClusterClient, BaseLogsClient
from stratio.api.filters import Filter, Operator
from stratio.api.filters.customer_filters import BaseCustomerFilters, build_filter_expression
from stratio.api.models import StreamItem
from stratio.api.models.logs import MarketplaceFunction
from stratio.api.session import ApiSession, CredentialsApiSession, ProfileApiSession
from stratio.config import Config


class LogsClient(BaseLogsClient):
    """
    Client for cluster-related operations.
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

    def list_streams(self, group: str, limit: Optional[int] = None) -> Optional[list[StreamItem]]:
        if not self._aws_automations_session:
            self.logger.error("AWS automations session not initialized.")
            return None

        # Create a CloudWatch Logs client
        logs_client = self._aws_automations_session.client("logs")
        self.logger.info(f"Listing log streams for group '{group}'.")

        streams = []
        try:
            paginator = logs_client.get_paginator("describe_log_streams")
            for page in paginator.paginate(logGroupName=group):
                for log_stream in page.get("logStreams", []):
                    streams.append(
                        StreamItem(
                            streamName=log_stream.get("logStreamName"),
                            lastEventTime=log_stream.get("lastEventTimestamp"),
                        )
                    )
        except Exception as e:
            self.logger.error(f"Error listing log streams: {e}")
            return None

        streams.sort(key=lambda x: (x.lastEventTime is not None, x.lastEventTime), reverse=True)
        return streams[:limit] if limit else streams

    def filter_streams(self, group: str, including: str, limit: int) -> Optional[list[StreamItem]]:
        if not self._aws_automations_session:
            self.logger.error("AWS automations session not initialized.")
            return None

        streams = self.list_streams(group, limit)
        if not streams:
            return None

        def read_and_filter(stream):
            log_lines = self._read_log_stream(group, stream.streamName, limit=100)
            return stream if any(including in line for line in log_lines) else None

        filtered_streams = []
        with ThreadPoolExecutor() as executor:
            future_to_stream = {executor.submit(read_and_filter, stream): stream for stream in streams}
            for future in as_completed(future_to_stream):
                result = future.result()
                if result:
                    filtered_streams.append(result)

        return filtered_streams

    def list_groups(self) -> Optional[list[str]]:
        if not self._aws_automations_session:
            self.logger.error("AWS automations session not initialized.")
            return None

        # Create a CloudWatch Logs client
        logs_client = self._aws_automations_session.client("logs")
        self.logger.info("Listing log groups.")

        groups = []
        try:
            paginator = logs_client.get_paginator("describe_log_groups")
            for page in paginator.paginate():
                for log_group in page.get("logGroups", []):
                    groups.append(log_group.get("logGroupName"))
        except Exception as e:
            self.logger.error(f"Error listing log groups: {e}")
            return None

        return groups

    def get_group(self, region: str, cluster_id: str, function: MarketplaceFunction) -> Optional[str]:
        if not self._aws_seller_session:
            self.logger.error("AWS seller session not initialized.")
            return

        # locate the customer source table from the cluster id
        source = self._get_customer_source_table(region, cluster_id)
        if source:
            customer_prefix = self.config.clusters.lambdas.marketplace_subscribers_prefix
            stack = source.replace(customer_prefix, "")
            function_prefix = getattr(self.config.clusters.lambdas, function.value, "")
            return f"/aws/lambda/{function_prefix}{stack}"

        return None

    def get_groups(self, region: str, cluster_id: str, *functions: MarketplaceFunction) -> Optional[list[str]]:
        groups = []
        for function in functions:
            group = self.get_group(region, cluster_id, function)
            if group:
                groups.append(group)

        return groups if len(groups) > 0 else None

    def stream(self, group: str, stream: str) -> None:
        if not self._aws_automations_session:
            self.logger.error("AWS automations session not initialized.")
            return

        # Create a CloudWatch Logs client
        logs_client = self._aws_automations_session.client("logs")
        next_token = None
        self.logger.info(f"Starting log streaming for group '{group}' and stream '{stream}'.")

        try:
            while True:
                # Prepare the parameters for get_log_events
                kwargs = {
                    "logGroupName": group,
                    "logStreamName": stream,
                    "startFromHead": True,  # fetch events from the beginning of the stream
                }
                if next_token:
                    kwargs["nextToken"] = next_token

                # Fetch log events
                response = logs_client.get_log_events(**kwargs)
                events = response.get("events", [])
                for event in events:
                    # Here we simply print the log message; you could also forward it to another sink
                    print(event.get("message", "").rstrip())

                # Update next_token so that the next call only returns new events
                next_token = response.get("nextForwardToken")
                # Wait a short while before polling for new events
                time.sleep(1)

        except KeyboardInterrupt:
            self.logger.info("Log streaming interrupted by user.")
        except Exception as e:
            self.logger.error(f"Error streaming logs: {e}")
            raise

    def _get_customer_source_table(self, region: str, cluster_id: str) -> Optional[str]:
        try:
            # Establish connection with DynamoDB
            dynamodb = self._aws_seller_session.resource("dynamodb", region_name=region)
            self.logger.debug(f"Connected to DynamoDB in region: {region}")

            # Enumerate all DynamoDB tables for the account
            customer_tables = self._filter_tables_from_config(dynamodb)

            filters = BaseCustomerFilters(
                conditions=[Filter(field="clusterIdentifier", operator=Operator.EQUALS, value=cluster_id)]
            )
            # Fetch customer data from every filtered table
            for table_name in customer_tables:
                exists = self._is_customer_in_table(dynamodb, table_name, filters)
                if exists:
                    return table_name

        except ClientError as c:
            self.logger.error(f"AWS ClientError listing customers: {c}")
        except re.error as re_err:
            self.logger.error(f"Regex compilation error: {re_err}")
        except Exception as e:
            self.logger.error(f"Unexpected error listing customers: {e}")

        return None

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

    def _is_customer_in_table(self, dynamodb, table_name: str, filters: Optional[BaseCustomerFilters] = None) -> bool:
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
        items = [item["customerIdentifier"] for item in response.get("Items", [])]

        return bool(items)

    def _read_log_stream(self, group: str, stream_name: str, limit: int) -> list[str]:
        """
        Read the first n lines from a given log stream.

        :param group: The CloudWatch log group name.
        :param stream_name: The specific log stream name within the log group.
        :param limit: The number of log events to read.
        :return: A list of log event messages.
        """
        logs_client = self._aws_automations_session.client("logs")
        response = logs_client.get_log_events(
            logGroupName=group, logStreamName=stream_name, limit=limit, startFromHead=True
        )
        return [event["message"] for event in response.get("events", [])]

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
            if not seller_session and self.config and self.config.clusters.seller:
                seller_session = self.config.clusters.seller.to_api_session()
            automations_session = self.automations_session
            if not automations_session and self.config and self.config.clusters.automations:
                automations_session = self.config.clusters.automations.to_api_session()

            aws_seller_session = LogsClient._initialize_aws_session(seller_session)
            aws_automations_session = LogsClient._initialize_aws_session(automations_session)
            return LogsClient(
                logger=self.logger,
                seller_session=seller_session,
                automations_session=automations_session,
                aws_seller_session=aws_seller_session,
                aws_automations_session=aws_automations_session,
                config=self.config,
            )
