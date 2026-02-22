"""Output formatting utilities."""

from rich.console import Console
from rich.table import Table

from devpulse.core.models import LatencyStats

console = Console()


def get_latency_color(ms: float) -> str:
    """Get color based on latency threshold.

    Args:
        ms: Response time in milliseconds

    Returns:
        Rich color name
    """
    if ms < 200:
        return "green"
    elif ms < 500:
        return "yellow"
    else:
        return "red"


def print_latency_results(stats: LatencyStats) -> None:
    """Print latency test results in a formatted table.

    Args:
        stats: Latency statistics to display
    """
    table = Table(title="Latency Test Results")

    table.add_column("URL", style="cyan", no_wrap=False)
    table.add_column("STATUS", justify="center", style="magenta")
    table.add_column("TIME(ms)", justify="right")

    for result in stats.results:
        if result.error:
            table.add_row(result.url, "ERROR", result.error, style="red")
        else:
            time_str = f"{result.response_time_ms:.0f}" if result.response_time_ms else "N/A"
            color = get_latency_color(result.response_time_ms) if result.response_time_ms else "white"

            table.add_row(result.url, str(result.status_code), time_str, style=color)

    console.print(table)
    console.print()
    console.print("[bold]Statistics:[/bold]")
    console.print(f"  Average: [yellow]{stats.avg_latency_ms:.0f}ms[/yellow]")
    console.print(f"  Fastest: [green]{stats.fastest_ms:.0f}ms[/green]")
    console.print(f"  Slowest: [red]{stats.slowest_ms:.0f}ms[/red]")
    console.print(f"  Success: {stats.success_count}/{stats.total_count}")


def print_success(message: str) -> None:
    """Print success message."""
    console.print(f"[green]✓[/green] {message}")


def print_error(message: str) -> None:
    """Print error message."""
    console.print(f"[red]✗[/red] {message}", style="red")


def print_info(message: str) -> None:
    """Print info message."""
    console.print(f"[blue]ℹ[/blue] {message}")
