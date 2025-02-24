import sys
import click
from .commands.auth import auth
from .commands.gen import gen


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version 0.1.4')
    ctx.exit()


@click.group()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True, help='Show version information')
@click.option('--debug', '-d', is_flag=True, help='Enable debug mode')
@click.pass_context
def cli(ctx, debug):
    """Zetic AI CLI tool for model management and deployment"""
    # Ensure ctx.obj exists
    ctx.ensure_object(dict)

    # Store debug setting
    ctx.obj['DEBUG'] = debug

    if debug:
        click.echo(click.style('Debug mode is enabled', fg='yellow'))


# Add commands
cli.add_command(auth)
cli.add_command(gen)


def main():
    try:
        cli(obj={})
    except Exception as e:
        click.echo(click.style(f'Error: {str(e)}', fg='red'), err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
