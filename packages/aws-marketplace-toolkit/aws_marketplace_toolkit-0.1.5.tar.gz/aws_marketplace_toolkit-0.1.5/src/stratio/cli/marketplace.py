#!/usr/bin/env python3

import os
import sys
import time
from multiprocessing import Process
from typing import Optional

import pyperclip
import typer
from rich.console import Console

# remove if stratio api is packaged
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


from stratio.api import ClusterClient, CustomerClient, KeosClient, LogsClient, OperationsClient
from stratio.api.formatters import BootstrapCLI, BootstrapJson, ClusterCLI, ClusterJson, CustomerCLI, CustomerJson
from stratio.api.models.logs import MarketplaceFunction
from stratio.cli.config import (
    check_for_updates,
    copy_default_config_if_missing,
    get_current_version,
    load_config,
    logger,
)
from stratio.cli.utils import parse_filter_option
from stratio.config import Config

app = typer.Typer(
    help="Stratio CLI Tool: Manage customers, clusters, and bootstrap instances.", invoke_without_command=True
)
customers_app = typer.Typer(help="Commands for customer management.")
clusters_app = typer.Typer(help="Commands for cluster management.")
keos_app = typer.Typer(help="Commands for KEOS management.")
bootstrap_app = typer.Typer(help="Commands for bootstrap instance management.")
aws_app = typer.Typer(help="Commands for AWS-related operations.")
logs_app = typer.Typer(help="Commands for log operations (groups, streams, read a specific log).")

# Register the subcommands.
app.add_typer(customers_app, name="customers")
app.add_typer(clusters_app, name="clusters")
app.add_typer(bootstrap_app, name="bootstraps")
app.add_typer(keos_app, name="keos")
app.add_typer(logs_app, name="logs")
app.add_typer(aws_app, name="aws")

console = Console()


def get_customer_client() -> CustomerClient:
    return CustomerClient.Builder().with_config(state.config).with_logger(logger).build()


def get_cluster_client() -> ClusterClient:
    return ClusterClient.Builder().with_config(state.config).with_logger(logger).build()


def get_operations_client() -> OperationsClient:
    return OperationsClient.Builder().with_config(state.config).with_logger(logger).build()


def get_keos_client() -> KeosClient:
    return KeosClient.Builder().with_config(state.config).with_logger(logger).build()


def get_logs_client() -> LogsClient:
    return LogsClient.Builder().with_config(state.config).with_logger(logger).build()


# Global state to hold our loaded configuration.
class AppState:
    config: Optional[Config] = None


state = AppState()

# Infrastructure region (all infrastructure is currently deployed in us-east-1, independently of installationRegion)
INFRASTRUCTURE_REGION = "us-east-1"


@app.callback()
def main(
    context: Optional[str] = typer.Option(
        None,
        "--context",
        "-x",
        help="Configuration environment (e.g. dev, prod). Loads ~/.marketplace/config_<context>.yaml",
    ),
    config: Optional[str] = typer.Option(None, "--config", "-c", help="Absolute path to the configuration YAML file"),
    version: Optional[bool] = typer.Option(None, "--version", "-v", help="Show the CLI version and exit"),
):
    """
    Stratio CLI Tool

    This tool manages customers, clusters, and bootstrap instances.
    The configuration file is loaded based on --context or --config. If neither is provided,
    the default configuration (~/.marketplace/config_default.yaml) is used.
    """
    if version:
        console.print(f"{get_current_version()}")
        raise typer.Exit()

    # Pre-flight checks
    check_for_updates()
    copy_default_config_if_missing()

    # Ensure the user does not supply both options simultaneously.
    if config and context:
        typer.echo("Please provide either --context or --config, not both.")
        raise typer.Exit(1)

    if config:
        config_path = config
    elif context:
        config_path = os.path.expanduser(f"~/.marketplace/config_{context}.yaml")
    else:
        config_path = os.path.expanduser("~/.marketplace/config_default.yaml")

    state.config = load_config(config_path)


# ─── ARGUMENT DEFINITION ─────────────────────────────────────────────────────────

FILTER_OPTION = typer.Option(None, "--filter", "-f", help="Filter in the format field,operator,value. Can be repeated.")
OUTPUT_OPTION = typer.Option("table", "--output", "-o", help="Output format: table or json", case_sensitive=False)
EXCLUDE_OPTION = typer.Option(
    None,
    "--exclude",
    "-e",
    help="List of attributes to exclude from the output. Only applicable when output is table.",
)
CLUSTER_ID_OPTION = typer.Option(..., "--cluster", "-c", help="Cluster identifier")
ACCOUNT_ID_OPTION = typer.Option("", "--account", "-a", help="AWS account identifier")
PROFILE_ID_OPTION = typer.Option("", "--profile", "-p", help="AWS profile from ~/.aws")
YES_OPTION = typer.Option(False, "--yes", "-y", help="Automatic yes to confirmation prompt")


# ─── CUSTOMERS COMMANDS ─────────────────────────────────────────────────────────


@customers_app.command("list")
def list_customers(
    filters: list[str] = FILTER_OPTION,
    output: str = OUTPUT_OPTION,
    exclude: list[str] = EXCLUDE_OPTION,
):
    """
    List customers with optional filtering and attribute exclusion (table mode only).
    """

    client = get_customer_client()
    filter_obj = parse_filter_option(filters) if filters else None

    formatter = CustomerJson() if output.lower() == "json" else CustomerCLI(exclude=exclude)

    try:
        spinner_message = "[bold green]Fetching customers...[/bold green]"
        # Create a separate console that writes to stderr for the spinner.
        spinner_console = Console(stderr=True)
        with spinner_console.status(spinner_message, spinner="dots", spinner_style="green"):
            result = client.list_customers(INFRASTRUCTURE_REGION, filters=filter_obj, formatter=formatter)

        if not result:
            console.print("No customers found.", style="yellow")
        else:
            console.print(result)
    except Exception as e:
        logger.error(f"Error listing customers: {e}")
        raise typer.Exit(1) from e


# ─── CLUSTERS COMMANDS ────────────────────────────────────────────────────────────


@clusters_app.command("list")
def list_clusters(
    filters: list[str] = FILTER_OPTION,
    output: str = OUTPUT_OPTION,
    exclude: list[str] = EXCLUDE_OPTION,
):
    """
    List clusters with optional filtering and attribute exclusion (table mode only).
    """

    client = get_cluster_client()
    filter_obj = parse_filter_option(filters) if filters else None

    formatter = ClusterJson() if output.lower() == "json" else ClusterCLI(exclude=exclude)

    spinner_message = "[bold green]Fetching clusters...[/bold green]"
    # Create a separate console that writes to stderr for the spinner.
    spinner_console = Console(stderr=True)
    with spinner_console.status(spinner_message, spinner="dots", spinner_style="green"):
        result = client.list_clusters(INFRASTRUCTURE_REGION, filters=filter_obj, formatter=formatter)

    if not result:
        console.print("No clusters found.", style="yellow")
    else:
        # Print to stdout (so that piping to jq is clean when using JSON output)
        console.print(result)


@clusters_app.command("start")
def start_cluster(
    cluster_id: str = CLUSTER_ID_OPTION,
    yes: bool = YES_OPTION,
):
    """
    Start a cluster (confirmation required).
    """
    if not yes and not typer.confirm(f"Are you sure you want to start cluster '{cluster_id}'?"):
        console.print("Operation cancelled.", style="red")
        raise typer.Exit()
    client = get_cluster_client()
    try:
        success = client.start(INFRASTRUCTURE_REGION, cluster_id)
        if success:
            console.print(f"Cluster '{cluster_id}' start initiated successfully.", style="green")
        else:
            console.print(f"Failed to start cluster '{cluster_id}'.", style="red")
    except Exception as e:
        logger.error(f"Error starting cluster: {e}")
        raise typer.Exit(1) from e


@clusters_app.command("stop")
def stop_cluster(
    cluster_id: str = CLUSTER_ID_OPTION,
    yes: bool = YES_OPTION,
):
    """
    Stop a cluster (confirmation required).
    """
    if not yes and not typer.confirm(f"Are you sure you want to stop cluster '{cluster_id}'?"):
        console.print("Operation cancelled.", style="red")
        raise typer.Exit()
    client = get_cluster_client()
    try:
        success = client.stop(INFRASTRUCTURE_REGION, cluster_id)
        if success:
            console.print(f"Cluster '{cluster_id}' stop initiated successfully.", style="green")
        else:
            console.print(f"Failed to stop cluster '{cluster_id}'.", style="red")
    except Exception as e:
        logger.error(f"Error stopping cluster: {e}")
        raise typer.Exit(1) from e


@clusters_app.command("uninstall")
def force_uninstall_cluster(
    cluster_id: str = CLUSTER_ID_OPTION,
    yes: bool = YES_OPTION,
):
    """
    Force uninstall a cluster (only on unsubscribed clusters; confirmation required).
    """
    if not yes and not typer.confirm(f"Are you sure you want to force uninstall cluster '{cluster_id}'?"):
        console.print("Operation cancelled.", style="red")
        raise typer.Exit()
    client = get_operations_client()
    try:
        success = client.force_uninstall(INFRASTRUCTURE_REGION, cluster_id)
        if success:
            console.print(f"Cluster '{cluster_id}' force uninstall initiated successfully.", style="green")
        else:
            console.print(f"Failed to force uninstall cluster '{cluster_id}'.", style="red")
    except Exception as e:
        logger.error(f"Error force uninstalling cluster: {e}")
        raise typer.Exit(1) from e


# ─── BOOTSTRAP COMMANDS ──────────────────────────────────────────────────────────


@bootstrap_app.command("list")
def list_bootstraps(
    output: str = typer.Option("table", "--output", "-o", help="Output format: table or json", case_sensitive=False),
    exclude: list[str] = EXCLUDE_OPTION,
):
    """
    List bootstrap instances with optional attribute exclusion (table mode only).
    """
    client = get_operations_client()
    formatter = BootstrapJson() if output.lower() == "json" else BootstrapCLI(exclude=exclude)
    try:
        spinner_message = "[bold green]Fetching bootstraps...[/bold green]"
        # Create a separate console that writes to stderr for the spinner.
        spinner_console = Console(stderr=True)
        with spinner_console.status(spinner_message, spinner="dots", spinner_style="green"):
            result = client.list_bootstraps(INFRASTRUCTURE_REGION, formatter=formatter)
        if not result:
            console.print("No bootstrap instances found.", style="yellow")
        else:
            console.print(result)
    except Exception as e:
        logger.error(f"Error listing bootstrap instances: {e}")
        raise typer.Exit(1) from e


@bootstrap_app.command("exec")
def exec_bootstrap(
    bootstrap_id: str = typer.Option(..., "--instance", "-i", help="Bootstrap instance ID"),
):
    """
    Enter a bootstrap instance via an SSM session.
    """
    client = get_operations_client()
    try:
        client.exec_bootstrap(INFRASTRUCTURE_REGION, bootstrap_id)
    except Exception as e:
        logger.error(f"Error entering bootstrap instance: {e}")
        raise typer.Exit(1) from e


@bootstrap_app.command("terminate")
def stop_bootstrap(
    bootstrap_id: str = typer.Option(..., "--instance", "-i", help="Bootstrap instance ID"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Automatic yes to confirmation prompt"),
):
    """
    Stop a bootstrap instance (confirmation required).
    """
    if not yes and not typer.confirm(f"Are you sure you want to stop bootstrap instance '{bootstrap_id}'?"):
        console.print("Operation cancelled.", style="red")
        raise typer.Exit()
    client = get_operations_client()
    try:
        success = client.terminate_bootstrap(INFRASTRUCTURE_REGION, bootstrap_id)
        if success:
            console.print(f"Bootstrap instance '{bootstrap_id}' termination initiated successfully.", style="green")
        else:
            console.print(f"Failed to terminate bootstrap instance '{bootstrap_id}'.", style="red")
    except Exception as e:
        logger.error(f"Error stopping bootstrap instance: {e}")
        raise typer.Exit(1) from e


# ─── KEOS COMMANDS ─────────────────────────────────────────────────────────


@keos_app.command("exec")
def exec_keos(
    cluster_identifier: str = CLUSTER_ID_OPTION,
):
    """
    Enter a cluster via the Keos client.
    """
    client = get_keos_client()
    try:
        workspaces = client.config.clusters.keos.workspaces_local_folder
        client.exec_keos(cluster_identifier, workspaces)
    except Exception as e:
        logger.error(f"Error entering keos for cluster '{cluster_identifier}': {e}")
        raise typer.Exit(1) from e


@keos_app.command("download")
def download_keos(
    cluster_identifier: str = CLUSTER_ID_OPTION,
):
    """
    Downloads a workspace for the cluster identifier provided.
    """
    client = get_keos_client()
    try:
        workspaces = client.config.clusters.keos.workspaces_local_folder
        client.download_keos_workspace(cluster_identifier, workspaces)
    except Exception as e:
        logger.error(f"Error download keos workspace '{cluster_identifier}': {e}")
        raise typer.Exit(1) from e


# ─── AWS COMMANDS ─────────────────────────────────────────────────────────


@aws_app.command("link")
def aws_link(account_identifier: str = ACCOUNT_ID_OPTION, profile: str = PROFILE_ID_OPTION):
    """
    Downloads a workspace for the cluster identifier provided.
    """
    client = get_operations_client()
    try:
        # both account_identifier and profile cannot be used at the same time, throw a descriptive error
        if account_identifier and profile:
            console.print("Please specify a log type: either --account or --profile, not both.", style="red")
            raise typer.Exit(1)

        if account_identifier:
            link = client.get_aws_console_link(account_identifier)
        else:
            link = client.get_aws_profile_link(profile)

        # copy link to clipboard
        pyperclip.copy(link)
        console.print(f"AWS Console link copied to clipboard: {link}")
    except Exception as e:
        logger.error(f"Error creating AWS link for '{account_identifier}': {e}")
        raise typer.Exit(1) from e


# ─── LOGS COMMANDS ─────────────────────────────────────────────────────────


@logs_app.command("cluster")
def cluster_logs(
    start_stop: bool = typer.Option(False, "--start-stop", help="Show start/stop logs for the cluster."),
    uninstall: bool = typer.Option(False, "--uninstall", help="Show uninstall logs for the cluster."),
    cluster_id: str = CLUSTER_ID_OPTION,
):
    """
    Stream logs for a cluster and automatically switch to a newer log stream if one appears.

    This command uses the API’s list_streams() method to periodically poll for a newer stream.
    When a new stream is detected (i.e. the first stream returned has changed), it terminates
    the currently running streaming process (which calls client.stream()) and starts a new one.

    Only one log type may be specified at a time.
    """
    # Validate that exactly one log type is selected.
    if not start_stop and not uninstall:
        console.print("Please specify a log type: either --start-stop or --uninstall.", style="red")
        raise typer.Exit(1)
    if start_stop and uninstall:
        console.print(
            "Please specify only one log type at a time (either --start-stop or --uninstall).",
            style="red",
        )
        raise typer.Exit(1)

    groups: list[str] = []
    client = get_logs_client()
    if start_stop:
        groups = client.get_groups(
            INFRASTRUCTURE_REGION, cluster_id, MarketplaceFunction.START_STOP, MarketplaceFunction.START_APPLICATIONS
        )
    elif uninstall:
        groups = [client.get_group(INFRASTRUCTURE_REGION, cluster_id, MarketplaceFunction.UNINSTALL)]

    if not groups:
        console.print(
            "Could not determine log group for the specified cluster and function.",
            style="red",
        )
        raise typer.Exit(1)

    console.print(f"Monitoring log groups: [bold]{groups}[/bold]")

    # Helper function to stream logs from a given stream.
    def stream_logs(group: str, stream_name: str):
        try:
            client.stream(group, stream_name)
        except Exception as error:
            logger.error(f"Error streaming logs for stream '{stream_name}': {error}")

    current_stream = None
    stream_process = None
    poll_interval = 5
    latest_streams = []
    try:
        while True:
            for group in groups:
                filtered = client.filter_streams(group, including=f"Handling [{cluster_id}]", limit=5)
                if filtered:
                    new_stream = filtered[0]
                    already_processed = any(item.streamName == new_stream.streamName for item in latest_streams)
                    if (
                        not already_processed
                        and new_stream.streamName != current_stream
                        and (
                            not latest_streams
                            or new_stream.lastEventTime > max(item.lastEventTime for item in latest_streams)
                        )
                    ):
                        console.print(f"[green]New stream detected: {new_stream.streamName}[/green]")
                        current_stream = new_stream.streamName
                        latest_streams.append(new_stream)
                        # Terminate the current streaming process if it exists.
                        if stream_process and stream_process.is_alive():
                            console.print("Terminating previous log stream...", style="yellow")
                            stream_process.terminate()
                            stream_process.join()
                        # Start a new process to stream logs from the new stream.
                        stream_process = Process(target=stream_logs, args=(group, current_stream))
                        stream_process.start()
                time.sleep(poll_interval)
    except KeyboardInterrupt:
        console.print("\nLog streaming interrupted by user.", style="red")
        if stream_process and stream_process.is_alive():
            stream_process.terminate()
            stream_process.join()
    except Exception as e:
        logger.error(f"Error monitoring log streams: {e}")
        if stream_process and stream_process.is_alive():
            stream_process.terminate()
            stream_process.join()
        raise typer.Exit(1) from e


@logs_app.command("groups")
def list_log_groups():
    """
    List all CloudWatch log groups available.
    """
    client = get_logs_client()
    groups = client.list_groups()
    if groups:
        console.print("[bold green]Available Log Groups:[/bold green]")
        for group in groups:
            console.print(f"- {group}")
    else:
        console.print("No log groups found.", style="yellow")


@logs_app.command("streams")
def list_log_streams(
    group: str = typer.Option(..., "--group", "-g", help="Name of the log group"),
    limit: int = typer.Option(10, "--limit", "-l", help="Maximum number of log streams to list"),
):
    """
    List log streams for a given log group.
    """
    client = get_logs_client()
    streams = client.list_streams(group, limit=limit)
    if streams:
        console.print(f"[bold green]Log Streams for group '{group}':[/bold green]")
        for stream in streams:
            # stream.lastEventTime may be None if no events have occurred
            last_time = stream.lastEventTime if stream.lastEventTime is not None else "N/A"
            console.print(f"- {stream.streamName} (last event time: {last_time})")
    else:
        console.print(f"No log streams found for group '{group}'.", style="yellow")


@logs_app.command("read")
def stream_specific_log(
    group: str = typer.Option(..., "--group", "-g", help="Name of the log group"),
    stream: str = typer.Option(..., "--stream", "-s", help="Name of the log stream"),
):
    """
    Stream logs for a specific log group and stream.

    This will continuously output log events from the specified log stream.
    """
    client = get_logs_client()
    try:
        console.print(f"Streaming logs for group '{group}' and stream '{stream}'. Press Ctrl+C to exit.")
        client.stream(group, stream)
    except KeyboardInterrupt:
        console.print("\nLog streaming interrupted by user.", style="red")
    except Exception as e:
        logger.error(f"Error streaming logs for group '{group}' and stream '{stream}': {e}")
        raise typer.Exit(1) from e


if __name__ == "__main__":
    app()
