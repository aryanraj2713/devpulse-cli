"""Port management command."""

import typer
import psutil
import signal
import sys
from typing import Optional
from devpulse.core.models import PortProcess
from devpulse.core.formatter import print_success, print_error, print_info


def find_process_by_port(port: int) -> Optional[PortProcess]:
    """Find process using specified port.

    Args:
        port: Port number to check

    Returns:
        PortProcess if found, None otherwise
    """
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            connections = proc.net_connections()
            for conn in connections:
                if conn.laddr.port == port:
                    return PortProcess(
                        pid=proc.info['pid'],
                        name=proc.info['name'],
                        port=port
                    )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return None


def kill_process(pid: int, force: bool = False) -> bool:
    """Kill process by PID.

    Args:
        pid: Process ID to kill
        force: Use SIGKILL instead of SIGTERM

    Returns:
        True if successful, False otherwise
    """
    try:
        proc = psutil.Process(pid)

        if force:
            proc.kill()  # SIGKILL
        else:
            proc.terminate()  # SIGTERM

        proc.wait(timeout=3)
        return True
    except psutil.NoSuchProcess:
        return False
    except psutil.TimeoutExpired:
        if not force:
            # Try force kill if terminate didn't work
            return kill_process(pid, force=True)
        return False
    except psutil.AccessDenied:
        raise PermissionError(f"Permission denied to kill process {pid}")


def kill_command(
    port: int = typer.Argument(..., help="Port number to free"),
    force: bool = typer.Option(False, "--force", "-f", help="Force kill (SIGKILL)"),
) -> None:
    """Kill process using specified port.

    Examples:
        devpulse kill 3000
        devpulse kill 8080 --force
    """
    if not (0 < port < 65536):
        print_error(f"Invalid port number: {port}")
        raise typer.Exit(1)

    print_info(f"Searching for process on port {port}...")

    process = find_process_by_port(port)

    if not process:
        print_info(f"No process found using port {port}")
        raise typer.Exit(0)

    print_info(f"Found process: {process.name} (PID: {process.pid})")

    try:
        if kill_process(process.pid, force=force):
            signal_type = "SIGKILL" if force else "SIGTERM"
            print_success(f"Killed process {process.pid} ({process.name}) on port {port} using {signal_type}")
        else:
            print_error(f"Failed to kill process {process.pid}")
            raise typer.Exit(1)
    except PermissionError as e:
        print_error(str(e))
        print_info("Try running with sudo/administrator privileges")
        raise typer.Exit(1)
    except Exception as e:
        print_error(f"Error: {str(e)}")
        raise typer.Exit(1)
