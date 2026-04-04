import click
from rich.console import Console
from rich.table import Table

from ..tools.mouse import MouseTool

console = Console()


@click.group(name="mouse")
def mouse():
    """Mouse operations."""
    pass


@mouse.command(name="size")
def mouse_size():
    """Get screen size."""
    width, height = MouseTool.size()
    console.print(f"[bold cyan]Screen size:[/] {width} x {height}")


@mouse.command(name="position")
def mouse_position():
    """Get current mouse position."""
    x, y = MouseTool.position()
    console.print(f"[bold cyan]Mouse position:[/] ({x}, {y})")


@mouse.command(name="move-to")
@click.option("--x", "-x", type=int, required=True, help="Target X coordinate")
@click.option("--y", "-y", type=int, required=True, help="Target Y coordinate")
@click.option("--duration", "-d", type=float, default=0.0, help="Movement duration in seconds")
def mouse_move_to(x: int, y: int, duration: float):
    """Move mouse to absolute coordinates."""
    try:
        MouseTool.move_to(x, y, duration=duration)
        console.print(f"[green]✓[/] Moved mouse to ({x}, {y})")
    except Exception as e:
        console.print(f"[red]✗[/] {e}")


@mouse.command(name="move")
@click.option("--x-offset", "-dx", type=int, required=True, help="X offset")
@click.option("--y-offset", "-dy", type=int, required=True, help="Y offset")
@click.option("--duration", "-d", type=float, default=0.0, help="Movement duration in seconds")
def mouse_move(x_offset: int, y_offset: int, duration: float):
    """Move mouse relative to current position."""
    try:
        MouseTool.move(x_offset, y_offset, duration=duration)
        console.print(f"[green]✓[/] Moved mouse by ({x_offset}, {y_offset})")
    except Exception as e:
        console.print(f"[red]✗[/] {e}")


@mouse.command(name="click")
@click.option("--x", "-x", type=int, help="X coordinate")
@click.option("--y", "-y", type=int, help="Y coordinate")
@click.option("--button", "-b", type=click.Choice(["left", "right", "middle"]), default="left", help="Mouse button")
@click.option("--clicks", "-c", type=int, default=1, help="Number of clicks")
@click.option("--interval", "-i", type=float, default=0.0, help="Interval between clicks")
def mouse_click(x: int, y: int, button: str, clicks: int, interval: float):
    """Click mouse at current or specified position."""
    try:
        MouseTool.click(x=x, y=y, button=button, clicks=clicks, interval=interval)
        pos_str = f" at ({x}, {y})" if x is not None and y is not None else ""
        console.print(f"[green]✓[/] Clicked {clicks} times with {button} button{pos_str}")
    except Exception as e:
        console.print(f"[red]✗[/] {e}")


@mouse.command(name="double-click")
@click.option("--x", "-x", type=int, help="X coordinate")
@click.option("--y", "-y", type=int, help="Y coordinate")
@click.option("--button", "-b", type=click.Choice(["left", "right", "middle"]), default="left", help="Mouse button")
def mouse_double_click(x: int, y: int, button: str):
    """Double-click mouse at current or specified position."""
    try:
        MouseTool.double_click(x=x, y=y, button=button)
        pos_str = f" at ({x}, {y})" if x is not None and y is not None else ""
        console.print(f"[green]✓[/] Double-clicked with {button} button{pos_str}")
    except Exception as e:
        console.print(f"[red]✗[/] {e}")


@mouse.command(name="right-click")
@click.option("--x", "-x", type=int, help="X coordinate")
@click.option("--y", "-y", type=int, help="Y coordinate")
def mouse_right_click(x: int, y: int):
    """Right-click mouse at current or specified position."""
    try:
        MouseTool.right_click(x=x, y=y)
        pos_str = f" at ({x}, {y})" if x is not None and y is not None else ""
        console.print(f"[green]✓[/] Right-clicked{pos_str}")
    except Exception as e:
        console.print(f"[red]✗[/] {e}")


@mouse.command(name="scroll")
@click.argument("clicks", type=int)
@click.option("--x", "-x", type=int, help="X coordinate")
@click.option("--y", "-y", type=int, help="Y coordinate")
def mouse_scroll(clicks: int, x: int, y: int):
    """Scroll vertically (positive = up, negative = down)."""
    try:
        MouseTool.scroll(clicks, x=x, y=y)
        pos_str = f" at ({x}, {y})" if x is not None and y is not None else ""
        console.print(f"[green]✓[/] Scrolled {clicks} clicks{pos_str}")
    except Exception as e:
        console.print(f"[red]✗[/] {e}")


@mouse.command(name="drag-to")
@click.option("--x", "-x", type=int, required=True, help="Target X coordinate")
@click.option("--y", "-y", type=int, required=True, help="Target Y coordinate")
@click.option("--duration", "-d", type=float, default=0.0, help="Drag duration in seconds")
@click.option("--button", "-b", type=click.Choice(["left", "right", "middle"]), default="left", help="Mouse button")
def mouse_drag_to(x: int, y: int, duration: float, button: str):
    """Drag mouse to absolute coordinates."""
    try:
        MouseTool.drag_to(x, y, duration=duration, button=button)
        console.print(f"[green]✓[/] Dragged to ({x}, {y}) with {button} button")
    except Exception as e:
        console.print(f"[red]✗[/] {e}")


@mouse.command(name="help")
def mouse_help():
    """Show detailed help for mouse commands."""
    table = Table(title="Mouse Commands")
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="white")

    table.add_row("size", "Get screen size")
    table.add_row("position", "Get current mouse position")
    table.add_row("move-to", "Move mouse to absolute coordinates")
    table.add_row("move", "Move mouse relative to current position")
    table.add_row("click", "Click mouse")
    table.add_row("double-click", "Double-click mouse")
    table.add_row("right-click", "Right-click mouse")
    table.add_row("scroll", "Scroll vertically")
    table.add_row("drag-to", "Drag mouse to coordinates")

    console.print(table)
