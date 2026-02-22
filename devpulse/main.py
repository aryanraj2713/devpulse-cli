"""Main entry point for DevPulse CLI."""

import typer

from devpulse.commands import curl, latency, port

app = typer.Typer(
    name="devpulse",
    help="DevPulse - Developer utility CLI for latency testing, port management, and curl conversion",
    add_completion=False,
)

app.command("latency")(latency.latency_command)
app.command("kill")(port.kill_command)
app.command("curl")(curl.curl_command)


def main() -> None:
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
