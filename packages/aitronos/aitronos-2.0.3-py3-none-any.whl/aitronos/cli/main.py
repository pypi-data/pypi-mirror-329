"""
Aitronos CLI tool for interacting with Aitronos services.
"""

import click
from .commands.init_project import init_project
from .commands.hello_world import hello_world
from .commands.streamline import handle_streamline_command


@click.group()
def cli():
    """Aitronos CLI tool for managing Aitronos projects and services."""
    pass


@cli.command()
@click.argument('project_name')
def init(project_name):
    """Initialize a new Aitronos project."""
    result = init_project(project_name)
    click.echo(result)


@cli.command()
def hello():
    """Run the hello world example."""
    result = hello_world()
    click.echo(result)


@cli.command()
@click.option('--input', '-i', help='Input for StreamLine processing')
@click.option('--output', '-o', help='Output file for results')
def streamline(input, output):
    """Use StreamLine functionality."""
    handle_streamline_command(input, output)


if __name__ == '__main__':
    cli() 