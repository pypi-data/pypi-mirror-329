"""
This module contains the CLI entrypoint to invoke
`opendapi github github run` from the toplevel, making sure
that the group entrypoint is also called.

NOTE: This is just here for backwards compatibility, and should be removed
"""

# pylint: disable=duplicate-code

import os

import click

from opendapi.cli.options import (
    BASE_COMMIT_SHA_PARAM_NAME_WITH_OPTION,
    CATEGORIES_PARAM_NAME_WITH_OPTION,
    DAPI_PARAM_NAME_WITH_OPTION,
    DATASTORES_PARAM_NAME_WITH_OPTION,
    PURPOSES_PARAM_NAME_WITH_OPTION,
    SUBJECTS_PARAM_NAME_WITH_OPTION,
    TEAMS_PARAM_NAME_WITH_OPTION,
    dapi_server_options,
    dev_options,
    features_options,
    git_options,
    minimal_schema_options,
    opendapi_run_options,
    third_party_options,
)
from opendapi.cli.repos.github.options import repo_options
from opendapi.cli.repos.github.runners.github.main import cli as main_cli
from opendapi.cli.repos.github.runners.github.options import runner_options
from opendapi.cli.repos.github.runners.github.run import cli as run_cli

# NOTE: !! IMPORTANT !!
#        Usually, the main cli for a cli group runs, then when the subommand
#        is invoked the kwargs are checked once more. This allows the root of the group
#        to pass state through set envvars and have that reflected in the children.
#        However, since this invokes the main cli and the child with the original set
#        of kwargs, therefore any envvar setting by main_cli is not reflected.
#        We therefore do it manually - but this needs to be kept in sync with any envvar
#        setting done in opendapi/cli/context_agnostic in the interim.
#        This is heavy handed, but allows for the least changes in other files.
_OPTIONS_SET_BY_MAIN_CLI = (
    BASE_COMMIT_SHA_PARAM_NAME_WITH_OPTION,
    CATEGORIES_PARAM_NAME_WITH_OPTION,
    DAPI_PARAM_NAME_WITH_OPTION,
    DATASTORES_PARAM_NAME_WITH_OPTION,
    PURPOSES_PARAM_NAME_WITH_OPTION,
    SUBJECTS_PARAM_NAME_WITH_OPTION,
    TEAMS_PARAM_NAME_WITH_OPTION,
)


def _update_kwargs_for_main_set_envvars(kwargs: dict) -> dict:
    """
    Adds options that are set as envvars in main_cli
    to the kwargs
    """
    # we manually add all set envvar values to kwargs for use in subcommands
    for option in _OPTIONS_SET_BY_MAIN_CLI:
        # explicit check of in os.environ due to defaults
        if kwargs.get(option.name) is None and option.envvar in os.environ:
            envvar_val = os.environ[option.envvar]
            # none of our callbacks make use of ctx or param for now
            val = (
                option.callback(None, None, envvar_val)
                if option.callback
                else envvar_val
            )
            kwargs[option.name] = val

    return kwargs


@click.command()
# common options
@dapi_server_options
@dev_options
@features_options
@git_options
@minimal_schema_options
@opendapi_run_options
@third_party_options
# github repo options
@repo_options
# github repo github runner options
@runner_options
def cli(**kwargs):
    """
    This command combines the `generate`, `enrich`, and `register` commands
    conditionally for a Github remote repo running on a Github hosted runner.

    This interacts with the DAPI server, and thus needs
    the server host and API key as environment variables or CLI options.
    """
    # NOTE: order matters here - parent commands first!
    for command in (main_cli, run_cli):
        command_params = command.params
        # run's params should always be a superset of all the children's params,
        # and therefore we do unsafe dict access as to not swallow any discrepancies
        command_kwargs = {key.name: kwargs[key.name] for key in command_params}
        with click.Context(command) as ctx:
            ctx.invoke(command, **command_kwargs)
            kwargs = _update_kwargs_for_main_set_envvars(kwargs)
