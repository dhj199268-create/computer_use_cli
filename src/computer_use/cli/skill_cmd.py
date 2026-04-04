import os
from pathlib import Path

import click
import yaml
from rich.console import Console
from rich.table import Table

console = Console()


@click.group(name="skill")
def skill():
    """Automation skills operations."""
    pass


@skill.command(name="list")
def skill_list():
    """List available skills."""
    skills_dir = Path("skills")
    if not skills_dir.exists():
        console.print("[yellow]No skills directory found[/]")
        return

    skill_files = list(skills_dir.glob("*.yaml")) + list(skills_dir.glob("*.yml"))

    if not skill_files:
        console.print("[yellow]No skill files found[/]")
        return

    table = Table(title="Available Skills")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="white")

    for skill_file in sorted(skill_files):
        try:
            with open(skill_file, "r") as f:
                data = yaml.safe_load(f)
                name = data.get("name", skill_file.stem)
                description = data.get("description", "")
                table.add_row(name, description)
        except Exception as e:
            console.print(f"[red]Error reading {skill_file}: {e}[/]")

    console.print(table)


@skill.command(name="show")
@click.argument("name")
def skill_show(name: str):
    """Show details of a specific skill."""
    skills_dir = Path("skills")
    if not skills_dir.exists():
        console.print("[yellow]No skills directory found[/]")
        return

    # Try to find the skill file
    skill_file = skills_dir / f"{name}.yaml"
    if not skill_file.exists():
        skill_file = skills_dir / f"{name}.yml"

    if not skill_file.exists():
        console.print(f"[red]Skill not found: {name}[/]")
        return

    try:
        with open(skill_file, "r") as f:
            data = yaml.safe_load(f)
            console.print(f"[bold cyan]Skill:[/] {data.get('name', name)}")
            console.print(f"[bold cyan]Description:[/] {data.get('description', '')}")

            if "steps" in data:
                console.print("\n[bold cyan]Steps:[/]")
                for i, step in enumerate(data["steps"], 1):
                    console.print(f"  {i}. {step}")

    except Exception as e:
        console.print(f"[red]Error reading skill: {e}[/]")


@skill.command(name="help")
def skill_help():
    """Show detailed help for skill commands."""
    table = Table(title="Skill Commands")
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="white")

    table.add_row("list", "List available skills")
    table.add_row("show <name>", "Show details of a skill")

    console.print(table)
