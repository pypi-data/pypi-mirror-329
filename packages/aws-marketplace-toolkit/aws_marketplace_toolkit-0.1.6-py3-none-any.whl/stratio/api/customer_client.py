# src/stratio/api/customer_client.py
import logging
import re
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from stratio.api import BaseCustomerClient
from stratio.api.filters import BaseCustomerFilters
from stratio.api.filters.customer_filters import build_filter_expression
from stratio.api.formatters import BaseCustomerFormatter
from stratio.api.models import CustomerItem, CustomerTableData
from stratio.api.session import ApiSession, CredentialsApiSession, ProfileApiSession
from stratio.api.transformers import BaseCustomerTransformer
from stratio.config import Config


class CustomerClient(BaseCustomerClient):
    """
    Client for interacting with the Customer API.
    """

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        session: Optional[ApiSession] = None,
        aws_session: Optional[boto3.Session] = None,
        config: Optional[Config] = None,
    ):
        super().__init__(logger=logger, session=session, config=config)
        self._aws_session = aws_session

    def get_customer(
        self, region: str, table_name: str, customer_id: str, formatter: Optional[BaseCustomerFormatter] = None
    ) -> Optional[CustomerItem]:
        try:
            if not self._aws_session:
                self.logger.error("AWS session not initialized.")
                return None

            # Establish connection with DynamoDB
            dynamodb = self._aws_session.resource("dynamodb", region_name=region)
            table = dynamodb.Table(table_name)
            self.logger.debug(f"Connected to DynamoDB in region: {region}")

            # Fetch customer data from the table by the primary key customer_id
            response = table.get_item(Key={"customerIdentifier": customer_id})
            logging.debug(f"Retrieved customer data: {response.get('Item', {})}")
            customer = CustomerItem(**response.get("Item", {}))

            if formatter:
                try:
                    customer = formatter.format_single(customer)
                except Exception as e:
                    self.logger.error(f"Error formatting customer data: {e}")
                    return None

            return customer
        except ClientError as c:
            self.logger.error(f"AWS ClientError listing customers: {c}")
        except re.error as re_err:
            self.logger.error(f"Regex compilation error: {re_err}")
        except Exception as e:
            self.logger.error(f"Unexpected error listing customers: {e}")

    def list_customers(
        self,
        *regions: str,
        filters: Optional[BaseCustomerFilters] = None,
        transformer: BaseCustomerTransformer = None,
        formatter: Optional[BaseCustomerFormatter] = None,
    ):
        customers = []
        try:
            if not self._aws_session:
                self.logger.error("AWS session not initialized.")
                return []

            for region in regions:
                # Establish connection with DynamoDB
                dynamodb = self._aws_session.resource("dynamodb", region_name=region)
                self.logger.debug(f"Connected to DynamoDB in region: {region}")

                # Enumerate all DynamoDB tables for the account
                customer_tables = self._filter_tables_from_config(dynamodb)

                # Fetch customer data from every filtered table
                for table_name in customer_tables:
                    try:
                        customer_data = self._get_customers_from_dynamodb(dynamodb, table_name, filters)
                        customers.append(customer_data)
                    except Exception as e:
                        self.logger.error(f"Error fetching data from table {table_name}: {e}")
                        customers.append(CustomerTableData(source=table_name, items=[], error=str(e)))
        except ClientError as c:
            self.logger.error(f"AWS ClientError listing customers: {c}")
        except re.error as re_err:
            self.logger.error(f"Regex compilation error: {re_err}")
        except Exception as e:
            self.logger.error(f"Unexpected error listing customers: {e}")

        if transformer:
            try:
                customers = transformer.parse(customers)
            except Exception as e:
                self.logger.error(f"Error parsing customer data: {e}")
                return None

        if formatter:
            try:
                customers = formatter.format_list(customers)
            except Exception as e:
                self.logger.error(f"Error formatting customer data: {e}")
                return None

        return customers

    def _filter_tables_from_config(self, dynamodb):
        """
        Filter DynamoDB tables based on the configured regex pattern.
        :param dynamodb: DynamoDB resource object.
        :return:         List of customer table names.
        """

        # Enumerate all DynamoDB tables for the account
        pattern = re.compile(self.config.customers.table_filter_regex)
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
    ) -> CustomerTableData:
        """
        Fetch customer rows from a DynamoDB table with optional server-side filtering.
        :param dynamodb:    DynamoDB resource object.
        :param table_name: Name of the table to fetch data from.
        :param filters:    Optional CustomerFilters instance.
        :return:            CustomerTableData instance.
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

        items = []
        try:
            response = table.scan(**scan_kwargs)
            self.logger.debug(f"Scanned {table_name}: Retrieved {len(response.get('Items', []))} items.")
            items.extend([CustomerItem(**item) for item in response.get("Items", [])])

            # Handle pagination
            while "LastEvaluatedKey" in response:
                scan_kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]
                response = table.scan(**scan_kwargs)
                self.logger.debug(f"Scanned {table_name}: Retrieved {len(response.get('Items', []))} more items.")
                items.extend([CustomerItem(**item) for item in response.get("Items", [])])
        except ClientError as e:
            self.logger.error(f"DynamoDB ClientError while scanning table {table_name}: {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error scanning table {table_name}: {e}")
            raise e

        return CustomerTableData(source=table_name, items=items)

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

    class Builder(BaseCustomerClient.Builder):
        def build(self):
            # Determine which session to use:
            # 1. Use the session provided via with_session
            # 2. Otherwise, use the session from config.customers.session
            session = self.session
            if not session and self.config and self.config.customers.session:
                session = self.config.customers.session.to_api_session()

            aws_session = CustomerClient._initialize_aws_session(session)
            return CustomerClient(logger=self.logger, session=session, config=self.config, aws_session=aws_session)
