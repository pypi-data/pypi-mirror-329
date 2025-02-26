from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

import click
from rich import print, table

import coiled
from coiled.cli.curl import sync_request

from ..cluster.utils import find_cluster
from ..utils import CONTEXT_SETTINGS

TODAY = datetime.today().date()


STATE_COLORS = {
    "pending": "yellow",
    "assigned": "green",
    "error": "red",
}


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("cluster", default="", required=False)
@click.option(
    "--workspace",
    default=None,
    help="Coiled workspace (uses default workspace if not specified).",
)
@click.option("--format", default="table", type=click.Choice(["json", "table"]))
@click.option("--limit", default=10, type=int)
@click.option("--sort", default=None)
def batch_status_cli(
    cluster: str,
    workspace: Optional[str],
    format: Literal["table", "json"],
    limit: int,
    sort: str,
):
    if cluster:
        jobs = get_job_status(cluster=cluster, workspace=workspace)
        print_job_status(jobs=jobs, format=format, cluster=cluster, sort=sort.split(",") if sort else None)
    else:
        jobs = get_job_list(workspace=workspace, limit=limit)
        print_job_list(jobs=jobs, format=format)


def format_dt(dt):
    if not dt:
        return ""
    dt = datetime.fromisoformat(dt)

    if dt.date() == TODAY:
        return dt.time().strftime("%H:%M:%S")
    else:
        return dt.strftime("%Y-%m-%d %H:%M:%S")


def format_duration_seconds(n):
    if n > 24 * 60 * 60 * 2:
        d = int(n / 3600 / 24)
        h = int((n - d * 3600 * 24) / 3600)
        return f"{d}d {h}hr"
    if n > 60 * 60 * 2:
        h = int(n / 3600)
        m = int((n - h * 3600) / 60)
        return f"{h}hr {m}m"
    if n > 60 * 10:
        m = int(n / 60)
        s = int(n - m * 60)
        return f"{m}m {s}s"

    return f"{n}s"


def print_job_list(jobs: list[dict], format: Literal["table", "json"]) -> None:
    if format == "json":
        print(jobs)
    else:
        if not jobs:
            print("No batch jobs found")
            return

        show_workspace = len({job["workspace_name"] for job in jobs}) > 1

        t = table.Table()
        t.add_column(
            "ID",
        )
        if show_workspace:
            t.add_column("Workspace")
        t.add_column("State", justify="center")
        t.add_column("Tasks Done", justify="right")
        t.add_column("Submitted", justify="right")
        # t.add_column("Started", justify="right")
        t.add_column("Finished", justify="right")
        t.add_column("Approx Cloud Cost", justify="right")
        t.add_column("Command")

        for job in jobs:
            if job["n_tasks_failed"]:
                if job["n_tasks_succeeded"]:
                    tasks_done = f"{job['n_tasks_succeeded']} + [red]{job['n_tasks_failed']}[/red]"
                    tasks_done = f"{tasks_done:4}"
                else:
                    tasks_done = f"[red]{job['n_tasks_failed']:4}[/red]"
            else:
                tasks_done = f"{job['n_tasks_succeeded']:4}"

            tasks_done = f"{tasks_done} /{job['n_tasks']:4}"
            if job["n_tasks_succeeded"] == job["n_tasks"]:
                tasks_done = f"[green]{tasks_done}[/green]"

            row_data = [str(job["cluster_id"] or "")]

            if show_workspace:
                row_data.append(str(job["workspace_name"] or ""))

            row_data.extend([
                str(job["state"] or ""),
                tasks_done,
                format_dt(job["created"]),
                format_dt(job["completed"]),
                f"${job['approximate_cloud_total_cost']:.2f}" if job["approximate_cloud_total_cost"] else "",
                job["user_command"],
            ])

            t.add_row(*row_data)
        print(t)


def print_job_status(jobs: list[dict], format: Literal["table", "json"], cluster: str | int, sort=None) -> None:
    if sort:
        for job in jobs:
            job["tasks"].sort(key=lambda task: [task.get(sort_key) for sort_key in sort])

    if format == "json":
        print(jobs)
    else:
        if not jobs:
            print(f"No batch jobs for cluster {cluster}")
            return

        cluster_state = jobs[0]["cluster_state"]
        user_command = jobs[0]["user_command"]

        t = table.Table(
            title=(
                f"Batch Jobs for Cluster {cluster} ([bold]{cluster_state}[/bold])\n"
                f"[bold]Command:[/bold] [green]{user_command}[/green]"
            )
        )
        t.add_column("Array ID")
        t.add_column("Assigned To")
        t.add_column("State")
        t.add_column("Start Time")
        t.add_column("Stop Time")
        t.add_column("Duration")
        t.add_column("Exit Code")

        for job in jobs:
            for task in job["tasks"]:
                if task["start"] and task["stop"]:
                    start = datetime.fromisoformat(task["start"])
                    stop = datetime.fromisoformat(task["stop"])
                    duration = format_duration_seconds(int((stop - start).total_seconds()))
                else:
                    duration = ""

                state_color = STATE_COLORS.get(task["state"])
                if task["exit_code"]:
                    state_color = "red"

                state = f"[{state_color}]{task['state']}[/{state_color}]" if state_color else task["state"]
                exit_code = (
                    ""
                    if task["exit_code"] is None
                    else (f"[red]{task['exit_code']}[/red]" if task["exit_code"] else str(task["exit_code"]))
                )

                t.add_row(
                    str(task["array_task_id"]),
                    task["assigned_to"]["private_ip_address"] if task["assigned_to"] else "",
                    state,
                    format_dt(task["start"]),
                    format_dt(task["stop"]),
                    duration,
                    exit_code,
                )
        print(t)


def get_job_status(cluster: str | int, workspace: Optional[str]) -> list[dict]:
    with coiled.Cloud(workspace=workspace) as cloud:
        cluster_info = find_cluster(cloud, cluster)
        cluster_id = cluster_info["id"]

        url = f"{cloud.server}/api/v2/jobs/cluster/{cluster_id}"
        response = sync_request(
            cloud=cloud,
            url=url,
            method="get",
            data=None,
            json_output=True,
        )
        return response or []


def get_job_list(workspace: Optional[str], limit: int) -> list[dict]:
    with coiled.Cloud(workspace=workspace) as cloud:
        url = f"{cloud.server}/api/v2/jobs/?workspace={workspace or ''}&limit={limit or ''}"
        response = sync_request(
            cloud=cloud,
            url=url,
            method="get",
            data=None,
            json_output=True,
        )
        if not response:
            return []
        else:
            return response.get("items", [])
