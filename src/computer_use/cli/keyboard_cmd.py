import click
from rich.console import Console
from rich.table import Table

from ..tools.keyboard import KeyboardTool

console = Console()


@click.group(name="keyboard")
def keyboard():
    """Keyboard operations."""
    pass


@keyboard.command(name="write")
@click.option("--text", "-t", type=str, required=True, help="Text to type")
@click.option("--interval", "-i", type=float, default=0.0, help="Interval between keystrokes")
def keyboard_write(text: str, interval: float):
    """Type out text."""
    try:
        KeyboardTool.write(text, interval=interval)
        console.print(f"[green]✓[/] Wrote text: {text[:50]}{'...' if len(text) > 50 else ''}")
    except Exception as e:
        console.print(f"[red]✗[/] {e}")


@keyboard.command(name="press")
@click.argument("keys", nargs=-1, required=True)
@click.option("--presses", "-c", type=int, default=1, help="Number of presses")
@click.option("--interval", "-i", type=float, default=0.0, help="Interval between presses")
def keyboard_press(keys: tuple, presses: int, interval: float):
    """Press and release a key or keys."""
    try:
        key_list = list(keys)
        KeyboardTool.press(key_list, presses=presses, interval=interval)
        console.print(f"[green]✓[/] Pressed: {', '.join(key_list)}")
    except Exception as e:
        console.print(f"[red]✗[/] {e}")


@keyboard.command(name="hotkey")
@click.argument("keys", nargs=-1, required=True)
@click.option("--interval", "-i", type=float, default=0.0, help="Interval between key presses")
def keyboard_hotkey(keys: tuple, interval: float):
    """Press a hotkey combination (e.g., ctrl c, cmd shift 4)."""
    try:
        KeyboardTool.hotkey(*keys, interval=interval)
        console.print(f"[green]✓[/] Pressed hotkey: {'+'.join(keys)}")
    except Exception as e:
        console.print(f"[red]✗[/] {e}")


@keyboard.command(name="copy")
def keyboard_copy():
    """Copy selected text (Ctrl+C or Cmd+C)."""
    try:
        KeyboardTool.copy()
        console.print(f"[green]✓[/] Copied to clipboard")
    except Exception as e:
        console.print(f"[red]✗[/] {e}")


@keyboard.command(name="paste")
def keyboard_paste():
    """Paste from clipboard (Ctrl+V or Cmd+V)."""
    try:
        KeyboardTool.paste()
        console.print(f"[green]✓[/] Pasted from clipboard")
    except Exception as e:
        console.print(f"[red]✗[/] {e}")


@keyboard.command(name="cut")
def keyboard_cut():
    """Cut selected text (Ctrl+X or Cmd+X)."""
    try:
        KeyboardTool.cut()
        console.print(f"[green]✓[/] Cut to clipboard")
    except Exception as e:
        console.print(f"[red]✗[/] {e}")


@keyboard.command(name="undo")
def keyboard_undo():
    """Undo (Ctrl+Z or Cmd+Z)."""
    try:
        KeyboardTool.undo()
        console.print(f"[green]✓[/] Undo")
    except Exception as e:
        console.print(f"[red]✗[/] {e}")


@keyboard.command(name="select-all")
def keyboard_select_all():
    """Select all (Ctrl+A or Cmd+A)."""
    try:
        KeyboardTool.select_all()
        console.print(f"[green]✓[/] Selected all")
    except Exception as e:
        console.print(f"[red]✗[/] {e}")


@keyboard.command(name="list-keys")
def keyboard_list_keys():
    """List all available keyboard keys."""
    from rich.columns import Columns
    from rich.panel import Panel

    keys = sorted(KeyboardTool.KEYBOARD_KEYS)
    columns = Columns(keys, column_first=True, equal=True, expand=True)
    console.print(Panel(columns, title="Available Keyboard Keys", border_style="cyan"))


@keyboard.command(name="help")
def keyboard_help():
    """Show detailed help for keyboard commands."""
    table = Table(title="Keyboard Commands")
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="white")

    table.add_row("write", "Type out text")
    table.add_row("press", "Press and release a key or keys")
    table.add_row("hotkey", "Press a hotkey combination")
    table.add_row("copy", "Copy selected text")
    table.add_row("paste", "Paste from clipboard")
    table.add_row("cut", "Cut selected text")
    table.add_row("undo", "Undo last action")
    table.add_row("select-all", "Select all")
    table.add_row("list-keys", "List all available keys")

    console.print(table)
