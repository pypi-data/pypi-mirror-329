"""Logs command group for the adalib CLI.

This submodule encompasses commands related to AdaLab logs
in the adalib CLI. It uses Typer for command line interface implementation,
allowing the user to retrieve different types of logs.

Functions:

"""

import sys

import typer
from adalib.apps import get_app, get_app_logs
from adalib.harbor import get_publish_logs
from adalib.lab import get_build_logs, get_lab_logs
from adalib.schedules import get_run_logs
from loguru import logger
from prompt_toolkit.completion import NestedCompleter
from rich import print as rich_print
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from typing_extensions import Annotated

from .completion_tree import completion_tree
from .factory import check_authentication
from .interactive import interactive_mode

logs_app = typer.Typer()


@logs_app.command("app", no_args_is_help=True)
def logs_get_app_logs(
    app_id: Annotated[
        str,
        typer.Argument(
            help="The ID of the app to fetch logs for.",
        ),
    ],
    container: Annotated[
        str,
        typer.Option(
            "-c",
            "--container",
            help="The name of the container whose logs to fetch.",
        ),
    ] = "",
    container_idx: Annotated[
        int,
        typer.Option(
            "-i",
            "--container-index",
            help="The index of the container whose logs to fetch.",
        ),
    ] = 0,
    from_date: Annotated[
        str,
        typer.Option(
            "-f",
            "--from",
            help="The start date for the logs, in ISO format (YYYY-MM-DDTHH:mm:ss+HH:mm).",
        ),
    ] = "",
    source: Annotated[
        str,
        typer.Option(
            "-s",
            "--source",
            help="The source of the logs. One of 'container' or 'system'.",
        ),
    ] = "container",
    to_date: Annotated[
        str,
        typer.Option(
            "-t",
            "--to",
            help="The end date for the logs, in ISO format (YYYY-MM-DDTHH:mm:ss+HH:mm).",
        ),
    ] = "",
):
    """
    Fetches logs for the app with the given ID.
    """
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Fetching data...", total=None)
            tmp = get_app(app_id)
            app_name = tmp["name"]
            logs = get_app_logs(
                app_id,
                container=container,
                container_idx=container_idx,
                from_date=from_date,
                source=source,
                to_date=to_date,
            )
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit()

    rich_print(f"{source.capitalize()} logs for app: {app_name} ({len(logs)})")

    table = Table("Timestamp", "Log message", title="Logs")
    for log in logs:
        table.add_row(log["time"], log["message"])

    console = Console()
    console.print(table)


@logs_app.command("build", no_args_is_help=True)
def logs_get_build_logs(
    build_id: Annotated[
        int,
        typer.Argument(
            help="The ID of the build process to fetch logs for.",
        ),
    ],
    source: Annotated[
        str,
        typer.Option(
            "-s",
            "--source",
            help="The source of the logs. One of 'build' or 'system'.",
        ),
    ] = "build",
):
    """
    Fetches logs for the build with the given ID.
    """
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Fetching data...", total=None)
            logs = get_build_logs(
                build_id=build_id,
                source=source,
            )
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit()

    rich_print(f"{source.capitalize()} logs for build process: {build_id} ({len(logs)})")

    if len(logs[0].keys()) == 2:
        table = Table("Timestamp", "Log message", title="Logs")
        for log in logs:
            table.add_row(log["time"], log["message"])
    else:
        table = Table("Timestamp", "Input", "Output", title="Logs")
        for log in logs:
            table.add_row(log["time"], log["input"], log["output"])

    console = Console()
    console.print(table)


@logs_app.command("lab", no_args_is_help=True)
def logs_get_lab_logs(
    from_date: Annotated[
        str,
        typer.Option(
            "-f",
            "--from",
            help="The start date for the logs, in ISO format (YYYY-MM-DDTHH:mm:ss+HH:mm).",
        ),
    ] = "",
    source: Annotated[
        str,
        typer.Option(
            "-s",
            "--source",
            help="The source of the logs. One of 'user' or 'system'.",
        ),
    ] = "user",
    to_date: Annotated[
        str,
        typer.Option(
            "-t",
            "--to",
            help="The end date for the logs, in ISO format (YYYY-MM-DDTHH:mm:ss+HH:mm).",
        ),
    ] = "",
):
    """
    Fetches logs for the user's Lab instance.
    """
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Fetching data...", total=None)
            logs = get_lab_logs(
                from_date=from_date,
                source=source,
                to_date=to_date,
            )
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit()

    rich_print(f"{source.capitalize()} Lab logs ({len(logs)})")

    table = Table("Timestamp", "Log message", title="Logs")
    for log in logs:
        table.add_row(log["time"], log["message"])

    console = Console()
    console.print(table)


@logs_app.command("publish", no_args_is_help=True)
def logs_get_publish_logs(
    metadata_id: Annotated[
        int,
        typer.Argument(
            help="The ID of the publish process to fetch logs for.",
        ),
    ],
    source: Annotated[
        str,
        typer.Option(
            "-s",
            "--source",
            help="The source of the logs. One of 'publish' or 'system'.",
        ),
    ] = "publish",
):
    """
    Fetches logs for the publish process with the given ID.
    """
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Fetching data...", total=None)
            logs = get_publish_logs(
                metadata_id=metadata_id,
                source=source,
            )
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit()

    rich_print(
        f"{source.capitalize()} logs for publish process of metadata {metadata_id} ({len(logs)})"
    )

    if len(logs[0].keys()) == 2:
        table = Table("Timestamp", "Log message", title="Logs")
        for log in logs:
            table.add_row(log["time"], log["message"])
    else:
        table = Table("Timestamp", "Input", "Output", title="Logs")
        for log in logs:
            table.add_row(log["time"], log["input"], log["output"])

    console = Console()
    console.print(table)


@logs_app.command("run", no_args_is_help=True)
def logs_get_run_logs(
    schedule_id: Annotated[
        int,
        typer.Argument(
            help="The ID of the schedule to fetch logs for.",
        ),
    ],
    run_id: Annotated[
        int,
        typer.Argument(
            help="The ID of the run instance to fetch logs for.",
        ),
    ],
):
    """
    Fetches logs for the schedule run instance with the given ID.
    """
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Fetching data...", total=None)
            logs = get_run_logs(
                schedule_id=schedule_id,
                run_id=run_id,
            )
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit()

    rich_print(f"Logs for run process {run_id} of schedule {schedule_id} ({len(logs)})")

    table = Table("Timestamp", "Source", "Input", "Output", "Cell number", title="Logs")
    for log in logs:
        table.add_row(
            log["timestamp"],
            log["log_type"],
            log["input"] or "",
            log["output"] or "",
            str(log["cell_number"]) or "",
        )

    console = Console()
    console.print(table)


@logs_app.callback(invoke_without_command=True)
def main(
    interactive: bool = typer.Option(
        False, "-i", "--interactive", help="Activate interactive mode"
    )
):
    if interactive:
        interactive_mode(
            this_app=logs_app,
            title="logs",
            color="maroon",
            completion=NestedCompleter.from_nested_dict(completion_tree["logs"]),
        )
    else:
        check_authentication()
