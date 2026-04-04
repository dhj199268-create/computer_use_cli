import click
from rich.console import Console

from .. import __version__

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="computer-use")
def cli():
    """
    Computer Use CLI - Control your computer via the command line.

    A set of tools for mouse control, keyboard input, screen operations,
    and automation skills.
    """
    pass


# Import subcommands
from .mouse_cmd import mouse
from .keyboard_cmd import keyboard
from .screen_cmd import screen
from .skill_cmd import skill

# Add subcommands
cli.add_command(mouse)
cli.add_command(keyboard)
cli.add_command(screen)
cli.add_command(skill)
