# cli.py
import sys
from aitronos_cli.commands import streamline
import click
from commands.init_project import init_project
from commands.hello_world_project.src.main.hello_world import main as hello_world

def main():
    if len(sys.argv) < 2:
        print("Usage: aitronos <command> [options]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "streamLine":
        streamline.handle_streamLine_command(sys.argv[2:])
    # Add future commands here:
    # elif command == "feature_x":
    #     feature_x.handle_feature_x_command(sys.argv[2:])
    else:
        print(f"Unknown command: {command}")
        print("Available commands: streamLine")
        sys.exit(1)

@click.group()
def cli():
    """Aitronos CLI tool"""
    pass

@cli.command()
@click.argument('project_name')
def init(project_name):
    """Initialize a new Aitronos project"""
    result = init_project(project_name)
    click.echo(result)

@cli.command()
def hello():
    """Run the hello world example"""
    result = hello_world()
    click.echo(result)

if __name__ == "__main__":
    cli()