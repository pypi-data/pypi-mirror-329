# src/stratio/api/formatters/cluster_formatters.py
import json
import re
from typing import Optional

from tabulate import tabulate

from stratio.api.models import ClusterItem, ClusterMetadataItem

from .base_formatter import BaseClusterFormatter


class CLIFormatter(BaseClusterFormatter):
    def __init__(self, exclude: Optional[list[str]] = None):
        """
        Initialize the CLIFormatter.

        :param exclude: Optional list of CustomerItem attribute names to exclude from the output.
        """
        self.exclude = set(exclude) if exclude else set()

    def format_list(self, data: list[ClusterItem]) -> str:
        if not data:
            return "No customer data available."

        # handle user-requested exclusions and logic-mandatory exclusions
        excluded = set() if self.exclude is None else self.exclude
        # "installation" will combine installationAction and successfullyInstalled
        excluded.add("installationAction")
        excluded.add("installationPhase")
        excluded.add("installationStatus")
        excluded.add("successfullyInstalled")
        excluded.add("clusterStatus")
        excluded.add("clusterAction")
        excluded.add("customerIdentifier")
        excluded.add("k8sVersion")
        excluded.add("keosVersion")
        excluded.add("universeVersion")
        excluded.add("created")

        # Dynamically retrieve all fields from CustomerItem, excluding specified fields
        metadata_fields = [field for field in ClusterMetadataItem.model_fields if field not in excluded]

        # Combine 'Source' with CustomerItem fields for headers
        headers = (
            list(_camel_case_to_title(field) for field in metadata_fields)
            + ["Installation status"]
            + ["Cluster status"]
            + ["EKS/EC2 Status"]
            + ["K8s"]
            + ["KEOS / Universe"]
            + ["Errors"]
        )

        table = []
        for cluster in data:
            if isinstance(cluster, ClusterItem):
                item_dict = cluster.metadata.model_dump()
                row = []

                # handle metadata fields
                for field in metadata_fields:
                    value = item_dict.get(field, "")
                    # If the value is a boolean, convert it to 'Yes'/'No' for better readability
                    if isinstance(value, bool):
                        value = "Yes" if value else "No"
                    row.append(value)

                self.add_installation_status(cluster, row)
                self.add_cluster_status(cluster, row)
                self.add_eks_ec2_status(cluster, row)
                self.add_k8s_version(cluster, row)
                self.add_product_version(cluster, row)
                self.add_errors(cluster, row)
                table.append(row)

        return tabulate(table, headers=headers, tablefmt="github")

    @staticmethod
    def add_k8s_version(cluster, row):
        if cluster.metadata.k8sVersion:
            row.append(cluster.metadata.k8sVersion)
        else:
            row.append("")

    @staticmethod
    def add_product_version(cluster, row):
        if cluster.metadata.keosVersion and cluster.metadata.universeVersion:
            versions = f"{cluster.metadata.keosVersion} / {cluster.metadata.universeVersion}"
            row.append(versions)
        else:
            row.append("")

    @staticmethod
    def add_eks_ec2_status(cluster, row):
        if cluster.eks:
            status = cluster.eks.status
            if cluster.ec2:
                running_instances = sum(
                    1 for instance in cluster.ec2 if (instance.State and instance.State.get("Name") == "running")
                )
                status += f" ({running_instances}/{len(cluster.ec2)} nodes)"
            row.append(status)
        else:
            row.append("")

    @staticmethod
    def add_cluster_status(cluster, row):
        if cluster.metadata.clusterAction is not None:
            row.append(_hyphen_to_title(cluster.metadata.clusterAction))
        elif cluster.metadata.clusterAction is None and cluster.metadata.clusterStatus is not None:
            row.append(_hyphen_to_title(cluster.metadata.clusterStatus))
        else:
            row.append("")

    @staticmethod
    def add_installation_status(cluster, row):
        if cluster.metadata.successfullyInstalled is True and cluster.metadata.installationAction is None:
            row.append("Installed")
        elif cluster.metadata.installationAction is not None and cluster.metadata.installationPhase is not None:
            row.append(_hyphen_to_title(cluster.metadata.installationPhase))
        elif cluster.metadata.installationAction is not None:
            row.append(_hyphen_to_title(cluster.metadata.installationAction))
        else:
            row.append("")

    @staticmethod
    def add_errors(cluster, row):
        if cluster.metadata.installationAction and "check" in cluster.metadata.installationAction:
            row.append("Installation Error")
        elif (
            cluster.metadata.clusterAction
            and "check" in cluster.metadata.clusterAction
            and cluster.metadata.clusterStatus == "started"
        ):
            row.append("Stop failed")
        elif (
            cluster.metadata.clusterAction
            and "check" in cluster.metadata.clusterAction
            and cluster.metadata.clusterStatus == "stopped"
        ):
            row.append("Start failed")
        else:
            row.append("")

    def format_single(self, data: ClusterItem) -> str:
        return self.format_list([data])


class JSONFormatter(BaseClusterFormatter):
    def format_single(self, data: ClusterItem) -> str:
        return json.dumps(data.model_dump(), default=str, indent=2)

    def format_list(self, data: list[ClusterItem]) -> str:
        return json.dumps([item.dict() for item in data], default=str, indent=2)


def _camel_case_to_title(text: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", " ", text).title().replace("Provisioned", "")


def _hyphen_to_title(text: str) -> str:
    return text.replace("-", " ").title().replace("Check", "")
