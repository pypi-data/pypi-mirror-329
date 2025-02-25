"""
CLI for syncing Dapi file state with server for server driven CICD:
`opendapi github github server-sync`.
"""

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
from opendapi.cli.repos.github.runners.github.options import (
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
# github repo github runner options
@runner_options
def cli(**kwargs):
    """
    This command will find all the analyzes all models and Dapi files in the Github remote
    repository given a Github hosted runner to collect them along with additional metadata
    to send to the DAPI server for server driven CICD.

    This interacts with the DAPI server, and thus needs
    the server host and API key as environment variables or CLI options.
    """
    change_trigger_event = construct_change_trigger_event(kwargs)
    run_id = kwargs["github_run_id"]
    run_attempt = kwargs["github_run_attempt"]
    run_number = kwargs["github_run_number"]
    return repo_runner_server_sync_cli(
        change_trigger_event,
        lambda dr: dr.cicd_start_github_github(
            run_id=run_id,
            run_attempt=run_attempt,
            run_number=run_number,
        ),
        CICDIntegration.GITHUB_GITHUB,
        {
            "run_id": run_id,
            "run_attempt": run_attempt,
            "run_number": run_number,
        },
        kwargs,
    )
