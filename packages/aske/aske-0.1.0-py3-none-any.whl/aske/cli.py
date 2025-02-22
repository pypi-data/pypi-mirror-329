import click
from aske import __version__

@click.group()
@click.version_option(version=__version__)
def main():
    """ASKE - Platform Architect Development Framework"""
    pass

@main.command()
@click.argument('name')
def init(name):
    """Initialize a new platform project"""
    click.echo(f"Initializing new platform project: {name}")

@main.command()
def validate():
    """Validate the current platform configuration"""
    click.echo("Validating platform configuration...")

if __name__ == '__main__':
    main()
