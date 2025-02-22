import click

from tobikodata.tcloud.auth import SSOAuth

SSO = SSOAuth()


@click.group()
def auth() -> None:
    """
    Tobiko Cloud Authentication
    """


@auth.command()
def status() -> None:
    """Display current session status"""
    SSO.status()


@auth.command(hidden=True)
def token() -> None:
    """Copy the current token onto clipboard"""
    SSO.copy_token()


@auth.command()
def refresh() -> None:
    """Refresh your current token"""
    SSO.refresh_token()


@auth.command()
def logout() -> None:
    """Logout of any current session"""
    SSO.logout()


@auth.command()
@click.option(
    "-f",
    "--force",
    is_flag=True,
    default=False,
    help="Create a new session even when one already exists.",
)
def login(force: bool) -> None:
    """Login to Tobiko Cloud"""
    SSO.login() if force else SSO.id_token(login=True)
    SSO.status()
