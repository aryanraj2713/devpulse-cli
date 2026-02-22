# DevPulse

Developer CLI for API latency testing, port management, and curl-to-code conversion.

## Installation

**Quick install (auto-detects uv/pipx/pip)**
```bash
curl -sSL https://raw.githubusercontent.com/aryanraj2713/devpulse-cli/main/install.sh | bash
# or locally: ./install.sh
```

**Manual install**
```bash
# Option 1: uv tool (recommended - isolated)
uv tool install .

# Option 2: pipx (isolated)
pipx install .

# Option 3: pip (development)
pip install -e .
```

> **Coming soon:** `pip install devpulse-cli` (once published to PyPI)

## Quick Start

```bash
# Test API latency
devpulse latency urls.txt
devpulse latency "https://google.com,https://github.com"

# Kill process on port
devpulse kill 3000

# Convert curl to code
devpulse curl 'curl -X POST https://api.com -H "Auth: token"' --lang python
```

## Commands

### `latency [FILE|URLS]`
Test URLs and measure response times (color-coded: green <200ms, yellow <500ms, red >500ms)

```bash
devpulse latency urls.txt
devpulse latency "url1.com,url2.com" --timeout 5
```

### `kill [PORT]`
Find and kill process using specified port

```bash
devpulse kill 3000 --force
```

### `curl [COMMAND]`
Convert curl commands to Python or JavaScript

```bash
devpulse curl 'curl https://api.com' --lang js
```

## Example Output

```
                    Latency Test Results
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┓
┃ URL                    ┃ STATUS ┃ TIME(ms) ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━┩
│ https://google.com     │ 200    │ 145      │
│ https://github.com     │ 200    │ 312      │
└────────────────────────┴────────┴──────────┘

Statistics:
  Average: 228ms | Fastest: 145ms | Slowest: 312ms | Success: 2/2
```

## TODO

- [ ] Publish to PyPI
- [ ] Concurrency for latency tester
- [ ] `--timeout` flag for port killer
- [ ] JSON output mode (`--json`)
- [ ] `--dry-run` for port killer

## Requirements

Python 3.11+ • Built with Typer, Rich, Pydantic, psutil
