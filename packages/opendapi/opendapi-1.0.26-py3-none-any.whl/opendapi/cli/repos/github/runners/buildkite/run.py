"""
CLI for generating, validating and enriching DAPI files: `opendapi github buildkite run`
"""

# pylint: disable=duplicate-code

import os

import click

from opendapi.cli.context_agnostic import RunCommand, repo_runner_run_cli
from opendapi.cli.generate import cli as generate_cli
from opendapi.cli.options import (
    dapi_server_options,
    dev_options,
    git_options,
    minimal_schema_options,
    opendapi_run_options,
    third_party_options,
)
from opendapi.cli.repos.github.options import repo_options
from opendapi.cli.repos.github.runners.buildkite.enrich import cli as enrich_cli
from opendapi.cli.repos.github.runners.buildkite.options import runner_options
from opendapi.cli.repos.github.runners.buildkite.register import cli as register_cli
from opendapi.cli.repos.github.runners.buildkite.server_sync import (
    cli as server_sync_cli,
)
from opendapi.feature_flags import FeatureFlag, get_feature_flag


def _should_skip_dbt_cloud__pr(kwargs):
    """
    Check if the `generate` command should be skipped

    Skip scenarios:
    1. If integrated with dbt Cloud
        a. Skip if pull request event and the run is the first attempt
    """
    should_wait_on_dbt_cloud = kwargs.get("dbt_cloud_url") is not None
    # retry of 0 is first run
    run_attempt = (
        int(kwargs.get("buildkite_retry_count"))
        if kwargs.get("buildkite_retry_count")
        else 0
    ) + 1
    # NOTE see if there is another way to get this
    is_pr_event = bool(kwargs["buildkite_pull_request"])

    return should_wait_on_dbt_cloud and is_pr_event and run_attempt == 1


def _should_skip_dbt_cloud__push(kwargs):
    """
    Check if the `generate` command should be skipped

    Skip scenarios:
    1. If integrated with dbt Cloud
        a. Skip if push event - since DBT cloud doesnt run on pushes to main by default
    """
    should_wait_on_dbt_cloud = kwargs.get("dbt_cloud_url") is not None
    # NOTE see if there is another way to get this
    is_push_event = not bool(kwargs["buildkite_pull_request"])

    return should_wait_on_dbt_cloud and is_push_event


def _should_skip_dbt_cloud__all(kwargs):
    """
    Check if the `generate` command should be skipped

    Skip scenarios:
    1. If integrated with dbt Cloud
        a. Skip if the event is a pull request or push event
    """
    return _should_skip_dbt_cloud__pr(kwargs) or _should_skip_dbt_cloud__push(kwargs)


def _dbt_cloud_envvar_prereqs(kwargs):
    """
    set envvars depending on dbt cloud integration
    """
    # if this is a push event for a DBT integration, the DBT run will not run
    # and so we should skip the DBT sync step during generate
    if _should_skip_dbt_cloud__push(kwargs):
        os.environ["ALWAYS_SKIP_DBT_SYNC"] = "true"


def _should_skip_wrapper_for_cicd_migration(fn):
    """
    Check if command should be skipped due to cicd migration
    """
    return lambda kw: get_feature_flag(
        FeatureFlag.PERFORM_COMPLETE_SERVER_SIDE_CICD
    ) or fn(kw)


@click.command()
# common options
@dapi_server_options
@dev_options
@git_options
@minimal_schema_options
@opendapi_run_options
@third_party_options
# github repo options
@repo_options
# github repo bk runner options
@runner_options
def cli(**kwargs):
    """
    This command combines the `generate`, `enrich`, and `register` commands
    conditionally for a Github remote repo running on a Buildkite hosted runner.

    This interacts with the DAPI server, and thus needs
    the server host and API key as environment variables or CLI options.
    """

    # perform prereqs for dbt cloud integration
    _dbt_cloud_envvar_prereqs(kwargs)

    # Run register last to ensure the DAPI files are registered and unregistered
    # Register will also validate the DAPI files in the backend
    commands = {
        "server-sync": RunCommand(
            command=server_sync_cli,
            description="sync DAPI files with the server",
            # NOTE: This should skip on PRs, since we wait for DBT to finish.
            #       However, this still must run for pushes - even though no DBT run exists
            #       (not configured to run on main, and commit shas change on merge so
            #       cant pull old ones) - so that the register flow can work as expected.
            #       In these scnenarios we will just have to do without true generated files.
            skip_condition=_should_skip_dbt_cloud__pr,
        ),
        "generate": RunCommand(
            command=generate_cli,
            description="generate DAPI files",
            skip_condition=_should_skip_wrapper_for_cicd_migration(
                _should_skip_dbt_cloud__all
            ),
        ),
        "enrich": RunCommand(
            command=enrich_cli,
            description="validate and enrich DAPI files",
            skip_condition=_should_skip_wrapper_for_cicd_migration(
                _should_skip_dbt_cloud__all
            ),
        ),
        "register": RunCommand(
            command=register_cli,
            description="register DAPI files",
            skip_condition=_should_skip_wrapper_for_cicd_migration(lambda *_: False),
        ),
    }

    repo_runner_run_cli(commands, kwargs)
