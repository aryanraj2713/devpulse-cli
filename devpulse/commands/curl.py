"""Curl to code converter command."""

import contextlib
import json
import shlex
from enum import StrEnum

import typer

from devpulse.core.formatter import console, print_error
from devpulse.core.models import CurlRequest


class Language(StrEnum):
    """Supported output languages."""

    PYTHON = "python"
    JAVASCRIPT = "javascript"
    JS = "js"


def parse_curl_command(curl_str: str) -> CurlRequest:
    """Parse curl command string into structured request.

    Args:
        curl_str: Curl command string

    Returns:
        CurlRequest model

    Raises:
        ValueError: If curl command cannot be parsed
    """
    # Remove 'curl' prefix if present
    curl_str = curl_str.strip()
    if curl_str.startswith("curl "):
        curl_str = curl_str[5:]

    # Parse using shlex to handle quotes properly
    try:
        parts = shlex.split(curl_str)
    except ValueError as e:
        raise ValueError(f"Failed to parse curl command: {e}") from e

    url = None
    method = "GET"
    headers = {}
    data = None
    json_data = None

    i = 0
    while i < len(parts):
        part = parts[i]

        if part in ["-X", "--request"]:
            if i + 1 < len(parts):
                method = parts[i + 1].upper()
                i += 2
                continue

        elif part in ["-H", "--header"]:
            if i + 1 < len(parts):
                header = parts[i + 1]
                if ":" in header:
                    key, value = header.split(":", 1)
                    headers[key.strip()] = value.strip()
                i += 2
                continue

        elif part in ["-d", "--data", "--data-raw"]:
            if i + 1 < len(parts):
                data = parts[i + 1]
                with contextlib.suppress(json.JSONDecodeError):
                    json_data = json.loads(data)
                i += 2
                continue

        elif part.startswith("http://") or part.startswith("https://"):
            url = part
            i += 1
            continue

        else:
            # Skip unknown flags
            i += 1

    if not url:
        raise ValueError("No URL found in curl command")

    # If data is provided but no method specified, default to POST
    if data and method == "GET":
        method = "POST"

    return CurlRequest(
        url=url, method=method, headers=headers, data=data if not json_data else None, json_data=json_data
    )


def generate_python_code(request: CurlRequest) -> str:
    """Generate Python requests code.

    Args:
        request: Parsed curl request

    Returns:
        Python code string
    """
    lines = ["import requests"]
    lines.append("")

    # Build request call
    args = [f'"{request.url}"']

    if request.headers:
        headers_str = "{\n"
        for key, value in request.headers.items():
            headers_str += f'    "{key}": "{value}",\n'
        headers_str += "}"
        args.append(f"headers={headers_str}")

    if request.json_data:
        json_str = json.dumps(request.json_data, indent=4)
        args.append(f"json={json_str}")
    elif request.data:
        args.append(f'data="{request.data}"')

    method_lower = request.method.lower()
    call = f"response = requests.{method_lower}(\n    " + ",\n    ".join(args) + "\n)"
    lines.append(call)
    lines.append("")
    lines.append("print(response.status_code)")
    lines.append("print(response.text)")

    return "\n".join(lines)


def generate_javascript_code(request: CurlRequest) -> str:
    """Generate JavaScript fetch code.

    Args:
        request: Parsed curl request

    Returns:
        JavaScript code string
    """
    lines = []

    # Build options object
    options = {}
    options["method"] = request.method

    if request.headers:
        options["headers"] = request.headers

    if request.json_data:
        options["headers"] = options.get("headers", {})
        options["headers"]["Content-Type"] = "application/json"
        options["body"] = json.dumps(request.json_data)
    elif request.data:
        options["body"] = request.data

    lines.append(f'fetch("{request.url}", {{')

    for key, value in options.items():
        if key == "headers":
            lines.append(f"  {key}: {{")
            for hkey, hvalue in value.items():
                lines.append(f'    "{hkey}": "{hvalue}",')
            lines.append("  },")
        elif key == "body":
            if isinstance(value, str) and value.startswith("{"):
                lines.append(f"  {key}: {value},")
            else:
                lines.append(f'  {key}: "{value}",')
        else:
            lines.append(f'  {key}: "{value}",')

    lines.append("})")
    lines.append("  .then(response => response.json())")
    lines.append("  .then(data => console.log(data))")
    lines.append('  .catch(error => console.error("Error:", error));')

    return "\n".join(lines)


def curl_command(
    curl_str: str = typer.Argument(..., help="Curl command string to convert"),
    lang: Language = typer.Option(Language.PYTHON, "--lang", "-l", help="Output language"),
) -> None:
    """Convert curl command to code.

    Examples:
        devpulse curl 'curl https://api.com'
        devpulse curl 'curl -X POST https://api.com -H "Auth: token" -d "{\"key\":\"value\"}"' --lang js
    """
    try:
        request = parse_curl_command(curl_str)
    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1) from None

    # Normalize language
    if lang in [Language.JS, Language.JAVASCRIPT]:
        code = generate_javascript_code(request)
        lang_name = "JavaScript"
    else:
        code = generate_python_code(request)
        lang_name = "Python"

    console.print(f"\n[bold cyan]{lang_name} Code:[/bold cyan]\n")
    console.print(f"[dim]{'-' * 60}[/dim]")

    # Syntax highlighting based on language
    from rich.syntax import Syntax

    syntax = Syntax(code, lang_name.lower(), theme="monokai", line_numbers=False)
    console.print(syntax)

    console.print(f"[dim]{'-' * 60}[/dim]\n")
