import click
from ...config import remove


@click.command()
def logout():
    remove("token")
