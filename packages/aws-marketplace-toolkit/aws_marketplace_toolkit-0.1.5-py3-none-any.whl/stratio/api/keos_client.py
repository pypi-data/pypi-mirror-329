# src/stratio/api/keos_client.py
import concurrent.futures
import logging
import os
import re
from typing import Optional

import boto3
import yaml
from boto3.s3.transfer import S3Transfer, TransferConfig
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from stratio.api import BaseClusterClient, BaseKeosClient
from stratio.api.session import ApiSession, CredentialsApiSession, ProfileApiSession
from stratio.config import Config
from stratio.utils import execute_command


class KeosClient(BaseKeosClient):
    """
    Client for cluster-related operations.
    """

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        automations_session: Optional[ApiSession] = None,
        aws_automations_session: Optional[boto3.Session] = None,
        config: Optional[Config] = None,
    ):
        super().__init__(logger=logger, automations_session=automations_session, config=config)
        self._aws_automations_session = aws_automations_session

    def download_keos_workspace(self, cluster_id: str, target_dir: str = "/tmp") -> None:
        if target_dir.startswith("/"):
            target_dir = target_dir[1:]
        workspaces_regex = self.config.clusters.workspaces_bucket_regex
        s3_client = self._aws_automations_session.client("s3")
        buckets = s3_client.list_buckets()["Buckets"]
        filtered_buckets = [bucket["Name"] for bucket in buckets if re.match(workspaces_regex, bucket["Name"])]
        for bucket in filtered_buckets:
            response = s3_client.list_objects_v2(Bucket=bucket, Prefix=f"workspaces/{cluster_id}/")
            download = "Contents" in response
            if download:
                os.makedirs(f"/{target_dir}/{cluster_id}", exist_ok=True)
                self._download_folder_with_transfer(
                    s3_client, bucket, f"workspaces/{cluster_id}/", f"/{target_dir}/{cluster_id}"
                )

    def exec_keos(self, cluster_id: str, workspace_dir: str):
        if not self._aws_automations_session:
            self.logger.error("AWS automations session not initialized.")
            return None

        if workspace_dir.startswith("/"):
            workspace_dir = workspace_dir[1:]

        # download workspace if it doesn't exist
        if not os.path.exists(f"/{workspace_dir}/{cluster_id}/"):
            print("Downloading KEOS workspace...")
            self.download_keos_workspace(cluster_id, f"/{workspace_dir}")
        else:
            print("Workspace already exists. Skipping download")

        # extract keos-installer version from workspace
        with open(f"/{workspace_dir}/{cluster_id}/cluster.yaml") as f:
            cluster_config = yaml.safe_load(f)
            keos_version = cluster_config.get("spec", {}).get("keos", {}).get("version")

        if not keos_version:
            raise RuntimeError("KEOS version not found in workspace (environment_vars)")

        try:
            # Construct the AWS CLI command to start a Session Manager session
            docker_command = [
                "docker",
                "run",
                "-ti",
                "--rm",
                "--net",
                "host",
                "-v",
                "/var/run/docker.sock:/var/run/docker.sock",
                "-v",
                f"/{workspace_dir}/{cluster_id}/:/workspace",
                "-e",
                f"VAULT_MASTER_KEY={self.config.clusters.keos.vault_key}",
                f"{self.config.clusters.keos.base_image}:{keos_version}",
            ]

            self.logger.warn(f"Executing AWS CLI command: {' '.join(docker_command)}")

            # Start the subprocess in a new process group to isolate signal handling
            execute_command(docker_command, self.logger)

            self.logger.info(f"KEOS instance {cluster_id} has been closed.")

        except ClientError as e:
            self.logger.error(f"AWS ClientError while entering KEOS instance {cluster_id}: {e}")
            raise RuntimeError(f"AWS ClientError while entering KEOS session: {e}") from e
        except FileNotFoundError as e:
            self.logger.error(
                "AWS CLI not found. Please ensure that the AWS CLI is installed and available in your PATH."
            )
            raise RuntimeError("AWS CLI not found. Please install the AWS CLI and ensure it's in your PATH.") from e
        except Exception as e:
            self.logger.error(f"Unexpected error entering KEOS: {e}")
            raise RuntimeError(f"Unexpected error entering KEOS: {e}") from e

    @staticmethod
    def _download_folder_with_transfer(s3_client: BaseClient, bucket_name: str, prefix: str, local_dir: str):
        # Tune transfer configuration for better concurrency
        transfer_config = TransferConfig(
            max_concurrency=10,  # Increase the number of concurrent threads
            multipart_threshold=1024 * 25,  # 25KB threshold for multipart downloads (adjust as needed)
            multipart_chunksize=1024 * 25,  # 25KB chunk size (adjust as needed)
            use_threads=True,
        )
        transfer = S3Transfer(s3_client, config=transfer_config)

        download_tasks = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            paginator = s3_client.get_paginator("list_objects_v2")
            for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
                if "Contents" not in page:
                    continue

                for obj in page["Contents"]:
                    key = obj["Key"]
                    relative_path = os.path.relpath(key, prefix)
                    local_file_path = os.path.join(local_dir, relative_path)
                    local_file_dir = os.path.dirname(local_file_path)
                    if not os.path.exists(local_file_dir):
                        os.makedirs(local_file_dir, exist_ok=True)

                    print(f"Downloading {key} to {local_file_path}")
                    # Submit the download task to the executor
                    future = executor.submit(transfer.download_file, bucket_name, key, local_file_path)
                    download_tasks.append(future)

            # Wait for all downloads to finish
            for future in concurrent.futures.as_completed(download_tasks):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error downloading a file: {e}")

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
            automations_session = self.automations_session
            if not automations_session and self.config and self.config.clusters.automations:
                automations_session = self.config.clusters.automations.to_api_session()

            aws_automations_session = KeosClient._initialize_aws_session(automations_session)
            return KeosClient(
                logger=self.logger,
                automations_session=automations_session,
                aws_automations_session=aws_automations_session,
                config=self.config,
            )
