# Installation Guide

## Easiest Methods

### 1. **One-line install script** (recommended)
```bash
./install.sh
```
Auto-detects and uses the best available package manager (uv → pipx → pip)

### 2. **uv tool install** (best for daily use)
```bash
uv tool install .
```
**Benefits:**
- Isolated environment (no conflicts)
- Globally available `devpulse` command
- Easy updates: `uv tool upgrade devpulse`
- Clean uninstall: `uv tool uninstall devpulse`

### 3. **pipx install** (if you don't have uv)
```bash
pipx install .
```
**Benefits:**
- Similar to uv tool
- Widely adopted standard
- Install: `pip install pipx`

## Development Setup

```bash
# Clone and install in editable mode
git clone <repo>
cd devpulse
pip install -e .
```

## Publishing to PyPI (future)

Once published, users can install directly:
```bash
uv tool install devpulse
# or
pipx install devpulse
# or
pip install devpulse
```

## Comparison

| Method | Isolated | Global CLI | Best For |
|--------|----------|------------|----------|
| `uv tool` | ✅ | ✅ | Daily use |
| `pipx` | ✅ | ✅ | No uv available |
| `pip -e` | ❌ | ⚠️ | Development |
| `install.sh` | ✅ | ✅ | Quick setup |

## Uninstalling

```bash
# uv
uv tool uninstall devpulse

# pipx
pipx uninstall devpulse

# pip
pip uninstall devpulse
```
