"""
Aitronos CLI tool for interacting with Aitronos services.
"""

import click
from .commands.init_project import init_project, init_hello_world_project, create_project_structure


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
@click.argument('project_name')
def init_hello_world(project_name):
    """Initialize a new Hello World example project."""
    result = init_hello_world_project(project_name)
    click.echo(result)


@cli.command()
@click.argument('project_name')
def init_hello_world_params(project_name):
    """Initialize a new Hello World with parameters example project."""
    result = create_project_structure(project_name, template_type="hello_world_params")
    click.echo(result)


@cli.command()
@click.option('--name', '-n', default='World', help='Name to greet')
@click.option('--count', '-c', default=1, type=int, help='Number of times to greet')
def hello(name, count):
    """Run a Hello World example with parameters."""
    for _ in range(count):
        click.echo(f"Hello, {name}!")


if __name__ == '__main__':
    cli() 