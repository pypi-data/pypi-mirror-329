"""
CLI for syncing Dapi file state with server for server driven CICD:
`opendapi github buildkite server-sync`.
"""

import datetime

import click

from opendapi.adapters.dapi_server import CICDIntegration
from opendapi.cli.context_agnostic import repo_runner_server_sync_cli
from opendapi.cli.options import (
    dapi_server_options,
    dev_options,
    minimal_schema_options,
    opendapi_run_options,
)
from opendapi.cli.repos.github.options import repo_options
from opendapi.cli.repos.github.runners.buildkite.options import (
    construct_change_trigger_event,
    runner_options,
)


@click.command()
# common options
@dapi_server_options
@dev_options
@minimal_schema_options
@opendapi_run_options
# github repo options
@repo_options
# github repo buildkite runner options
@runner_options
def cli(**kwargs):
    """
    This command will find all the analyzes all models and Dapi files in the Github remote
    repository given a Buildkite hosted runner to collect them along with additional metadata
    to send to the DAPI server for server driven CICD.

    This interacts with the DAPI server, and thus needs
    the server host and API key as environment variables or CLI options.
    """
    change_trigger_event = construct_change_trigger_event(kwargs)
    job_id = kwargs["buildkite_job_id"]
    # NOTE: we may want to make this an envvar set by the script,
    #       but this works for now. The ideal case is we pull this from BK API,
    #       which we will need anyway for DBT, but this is fine for now.
    job_started_at = datetime.datetime.now(datetime.timezone.utc)
    build_id = kwargs["buildkite_build_id"]
    retry_count = kwargs["buildkite_retry_count"]
    return repo_runner_server_sync_cli(
        change_trigger_event,
        lambda dr: dr.cicd_start_github_buildkite(
            job_id=job_id,
            job_started_at=job_started_at,
            build_id=build_id,
            retry_count=retry_count,
        ),
        CICDIntegration.GITHUB_BUILDKITE,
        {
            "job_id": job_id,
            "job_started_at": job_started_at.isoformat(),
            "build_id": build_id,
            "retry_count": retry_count,
        },
        kwargs,
    )
