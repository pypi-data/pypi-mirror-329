"""TcEx Framework Module"""

# standard library
from typing import Optional

# third-party
import typer

# first-party
from tcex_cli.cli.deploy.deploy_cli import DeployCli
from tcex_cli.render.render import Render

# typer does not yet support PEP 604, but pyupgrade will enforce
# PEP 604. this is a temporary workaround until support is added.
IntOrNone = Optional[int]  # noqa: UP007
StrOrNone = Optional[str]  # noqa: UP007


def command(
    server: str = typer.Argument(
        ...,
        envvar='TC_DEPLOY_SERVER',
        help='Can be defined as an environment variable to avoid passing in each time.',
    ),
    allow_all_orgs: bool = typer.Option(
        default=True, help='If true all orgs are able to use the App.'
    ),
    allow_distribution: bool = typer.Option(
        default=True, help='If true the App is allowed to be distributed.'
    ),
    app_file: StrOrNone = typer.Option(
        None,
        help='The fully qualified path to App file. Will be auto-detected if not provided.',
    ),
    proxy_host: StrOrNone = typer.Option(None, help='(Advanced) Hostname for the proxy server.'),
    proxy_port: IntOrNone = typer.Option(None, help='(Advanced) Port number for the proxy server.'),
    proxy_user: StrOrNone = typer.Option(None, help='(Advanced) Username for the proxy server.'),
    proxy_pass: StrOrNone = typer.Option(None, help='(Advanced) Password for the proxy server.'),
):
    r"""CLI command for deploying Apps to ThreatConnect Exchange.

    This command REQUIRES the following environment variables to be set.\n\n\n
    * TC_API_ACCESS_ID\n
    * TC_API_SECRET_KEY\n\n\n
    Optional environment variables include:\n\n\n
    * PROXY_HOST\n
    * PROXY_PORT\n
    * PROXY_USER\n
    * PROXY_PASS\n
    """
    cli = DeployCli(
        server,
        allow_all_orgs,
        allow_distribution,
        app_file,
        proxy_host,
        proxy_port,
        proxy_user,
        proxy_pass,
    )
    try:
        cli.deploy_app()
    except Exception as ex:
        cli.log.exception('Failed to run "tcex deploy" command.')
        Render.panel.failure(f'Exception: {ex}')
