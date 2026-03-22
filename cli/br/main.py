"""br CLI — the BlackRoad command-line interface."""
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

@click.group()
@click.version_option("1.0.0", prog_name="br")
def cli():
    """BlackRoad CLI — manage agents, fleet, services, and deployments."""
    pass

@cli.command()
def status():
    """Show fleet status."""
    table = Table(title="Fleet Status", show_lines=True)
    table.add_column("Node", style="cyan bold")
    table.add_column("IP", style="dim")
    table.add_column("Role", style="green")
    table.add_column("Status")
    nodes = [
        ("Alice", "192.168.4.49", "gateway", "[green]online[/]"),
        ("Cecilia", "192.168.4.96", "inference", "[green]online[/]"),
        ("Octavia", "192.168.4.101", "platform", "[green]online[/]"),
        ("Aria", "192.168.4.98", "edge", "[green]online[/]"),
        ("Lucidia", "192.168.4.38", "dns/apps", "[green]online[/]"),
        ("Gematria", "DO nyc3", "tls-edge", "[green]online[/]"),
        ("Anastasia", "DO nyc1", "compute", "[green]online[/]"),
    ]
    for name, ip, role, status in nodes:
        table.add_row(name, ip, role, status)
    console.print(table)

@cli.command()
@click.argument("query")
def search(query: str):
    """Search across all data sources."""
    console.print(f"[magenta]Searching:[/] {query}")

@cli.command()
@click.argument("target")
def deploy(target: str):
    """Deploy a service to the fleet."""
    console.print(f"[yellow]Deploying:[/] {target}")

@cli.command()
def agents():
    """List all registered agents."""
    console.print(Panel("10 agents online", title="Agent Fleet", border_style="magenta"))

if __name__ == "__main__":
    cli()
