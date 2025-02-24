import click
from .login import login
from .logout import logout


@click.group()
def auth():
    """Authentication commands"""
    pass


auth.add_command(login)
auth.add_command(logout)

__all__ = ['auth', 'login', 'logout']
