"""
Template management CLI commands.
"""

from pathlib import Path
from typing import Optional, Tuple

import click
from rich.console import Console
from rich.table import Table

from ..core.logger import get_logger
from ..tools.template import get_template_manager, TemplateManager
from ..tools.image import ImageTool
from ..tools.screen import ScreenTool

logger = get_logger(__name__)
console = Console()


@click.group(name="template")
def template():
    """UI template management operations."""
    pass


@template.command(name="list")
def template_list():
    """List all available templates."""
    template_manager = get_template_manager()
    templates = template_manager.list_templates()

    if not templates:
        console.print("[yellow]No templates found[/]")
        return

    table = Table(title="Available Templates")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Created", style="green")
    table.add_column("Tags", style="yellow")

    for t in templates:
        # Format created date
        from datetime import datetime
        try:
            created = datetime.fromisoformat(t.created_at).strftime("%Y-%m-%d")
        except ValueError:
            created = t.created_at[:10] if t.created_at else "-"

        tags = ", ".join(t.tags) if t.tags else "-"
        table.add_row(t.name, t.description or "-", created, tags)

    console.print(table)


@template.command(name="show")
@click.argument("name")
def template_show(name: str):
    """Show details of a specific template."""
    template_manager = get_template_manager()

    if not template_manager.template_exists(name):
        console.print(f"[red]Template not found: {name}[/]")
        return

    try:
        image, metadata = template_manager.load_template(name)

        console.print(f"[bold cyan]Template:[/] {name}")
        if metadata:
            console.print(f"[bold cyan]Description:[/] {metadata.description or '-'}")
            console.print(f"[bold cyan]Created:[/] {metadata.created_at}")
            console.print(f"[bold cyan]Updated:[/] {metadata.updated_at}")
            if metadata.original_region:
                console.print(f"[bold cyan]Original Region:[/] {metadata.original_region}")
            if metadata.original_screen_size:
                console.print(f"[bold cyan]Original Screen Size:[/] {metadata.original_screen_size}")
            if metadata.tags:
                console.print(f"[bold cyan]Tags:[/] {', '.join(metadata.tags)}")

        console.print(f"[bold cyan]Image Size:[/] {image.size}")
        console.print(f"[bold cyan]Image Path:[/] {template_manager.get_template_image_path(name)}")

    except Exception as e:
        console.print(f"[red]Error loading template: {e}[/]")


@template.command(name="save")
@click.option("--name", "-n", required=True, help="Name for the template")
@click.option("--region", "-r", required=True, type=(int, int, int, int),
              help="Region to capture (left top width height)")
@click.option("--description", "-d", default="", help="Description of the template")
@click.option("--tag", "-t", multiple=True, help="Tags for the template (can use multiple times)")
def template_save(name: str, region: Tuple[int, int, int, int], description: str, tag: tuple):
    """Capture a region and save as a template."""
    template_manager = get_template_manager()

    try:
        console.print(f"[cyan]Capturing template '{name}' from region {region}...[/]")
        template_manager.capture_and_save_template(
            name=name,
            region=region,
            description=description,
            tags=list(tag) if tag else None,
        )
        console.print(f"[green]✓ Template '{name}' saved successfully![/]")
    except Exception as e:
        console.print(f"[red]Error saving template: {e}[/]")


@template.command(name="delete")
@click.argument("name")
@click.confirmation_option(prompt="Are you sure you want to delete this template?")
def template_delete(name: str):
    """Delete a template."""
    template_manager = get_template_manager()

    if not template_manager.template_exists(name):
        console.print(f"[red]Template not found: {name}[/]")
        return

    if template_manager.delete_template(name):
        console.print(f"[green]✓ Template '{name}' deleted[/]")
    else:
        console.print(f"[red]Failed to delete template '{name}'[/]")


@template.command(name="click")
@click.argument("name")
@click.option("--confidence", "-c", type=float, default=None,
              help="Confidence threshold (0.0-1.0, requires OpenCV)")
@click.option("--region", "-r", type=(int, int, int, int), default=None,
              help="Search region (left top width height)")
@click.option("--button", "-b", default="left",
              type=click.Choice(["left", "right", "middle"]),
              help="Mouse button to use")
@click.option("--clicks", "-n", type=int, default=1, help="Number of clicks")
def template_click(name: str, confidence: float, region: tuple, button: str, clicks: int):
    """Locate a template on screen and click it."""
    template_manager = get_template_manager()

    if not template_manager.template_exists(name):
        console.print(f"[red]Template not found: {name}[/]")
        return

    try:
        console.print(f"[cyan]Locating and clicking template '{name}'...[/]")
        region_tuple = region if region else None

        ImageTool.click_by_template_name(
            name,
            confidence=confidence,
            region=region_tuple,
            button=button,
            clicks=clicks,
        )
        console.print(f"[green]✓ Clicked template '{name}'[/]")
    except Exception as e:
        console.print(f"[red]Error clicking template: {e}[/]")


@template.command(name="update")
@click.argument("name")
@click.option("--description", "-d", help="New description")
@click.option("--tag", "-t", multiple=True, help="New tags (replaces existing)")
def template_update(name: str, description: Optional[str], tag: tuple):
    """Update template metadata."""
    template_manager = get_template_manager()

    if not template_manager.template_exists(name):
        console.print(f"[red]Template not found: {name}[/]")
        return

    tags = list(tag) if tag else None

    if description is None and tags is None:
        console.print("[yellow]No updates specified[/]")
        return

    if template_manager.update_template_metadata(name, description=description, tags=tags):
        console.print(f"[green]✓ Template '{name}' updated[/]")
    else:
        console.print(f"[red]Failed to update template '{name}'[/]")


@template.command(name="help")
def template_help():
    """Show detailed help for template commands."""
    table = Table(title="Template Commands")
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="white")

    table.add_row("list", "List all available templates")
    table.add_row("show <name>", "Show details of a template")
    table.add_row("save --name <name> --region <l t w h>", "Capture and save a template")
    table.add_row("delete <name>", "Delete a template")
    table.add_row("click <name>", "Locate and click a template on screen")
    table.add_row("update <name>", "Update template metadata")

    console.print(table)
    console.print("\n[bold]Examples:[/]")
    console.print("  computer-use template list")
    console.print("  computer-use template save --name search_button --region 100 100 80 30")
    console.print("  computer-use template click search_button --confidence 0.8")
    console.print("  computer-use template delete old_button")
