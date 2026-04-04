import os
import click
from rich.console import Console
from rich.table import Table

from ..tools.screen import ScreenTool

console = Console()


@click.group(name="screen")
def screen():
    """Screen operations."""
    pass


@screen.command(name="size")
def screen_size():
    """Get screen size."""
    width, height = ScreenTool.screenshot().size
    console.print(f"[bold cyan]Screen size:[/] {width} x {height}")


@screen.command(name="screenshot")
@click.option("--output", "-o", type=str, help="Output file path (e.g., screenshot.png)")
@click.option("--region", "-r", type=(int, int, int, int), help="Region (left top width height)")
def screen_screenshot(output: str, region: tuple):
    """Take a screenshot."""
    try:
        output_path = None
        if output:
            # Resolve to absolute path for clarity
            output_path = os.path.abspath(os.path.expanduser(output))
        img = ScreenTool.screenshot(filename=output_path, region=region)
        if output_path:
            console.print(f"[green]✓[/] Screenshot saved to: {output_path}")
        else:
            console.print(f"[green]✓[/] Screenshot taken: {img.size[0]} x {img.size[1]}")
    except Exception as e:
        console.print(f"[red]✗[/] {e}")


@screen.command(name="pixel")
@click.option("--x", "-x", type=int, required=True, help="X coordinate")
@click.option("--y", "-y", type=int, required=True, help="Y coordinate")
def screen_pixel(x: int, y: int):
    """Get RGB color of a pixel."""
    try:
        r, g, b = ScreenTool.pixel(x, y)
        console.print(f"[bold cyan]Pixel color at ({x}, {y}):[/] RGB({r}, {g}, {b})")
    except Exception as e:
        console.print(f"[red]✗[/] {e}")


@screen.command(name="help")
def screen_help():
    """Show detailed help for screen commands."""
    table = Table(title="Screen Commands")
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="white")

    table.add_row("size", "Get screen size")
    table.add_row("screenshot", "Take a screenshot")
    table.add_row("pixel", "Get pixel color")

    console.print(table)
