"""Agent CLI — interact with agents from the terminal."""
import asyncio
import click
from rich.console import Console
from rich.table import Table

console = Console()

@click.group()
def cli():
    """BlackRoad Agent CLI"""
    pass

@cli.command()
@click.argument("agent_name")
@click.argument("message")
def chat(agent_name: str, message: str):
    """Send a message to an agent."""
    console.print(f"[bold magenta]→ {agent_name}[/]: {message}")

@cli.command()
def roster():
    """Show all registered agents."""
    table = Table(title="Agent Roster")
    table.add_column("Name", style="cyan")
    table.add_column("Role", style="green")
    table.add_column("Group")
    table.add_column("Status", style="bold")
    agents = [
        ("cece", "executive-assistant", "leadership", "online"),
        ("lucidia", "researcher", "intelligence", "online"),
        ("operator", "fleet-manager", "infrastructure", "online"),
        ("alice", "gateway", "infrastructure", "online"),
        ("cecilia", "inference", "compute", "online"),
        ("octavia", "platform", "services", "online"),
        ("aria", "edge", "networking", "online"),
        ("gematria", "tls-edge", "networking", "online"),
        ("anastasia", "compute", "compute", "online"),
        ("alexandria", "dev-workstation", "development", "online"),
    ]
    for name, role, group, status in agents:
        table.add_row(name, role, group, f"[green]{status}[/green]")
    console.print(table)

if __name__ == "__main__":
    cli()
