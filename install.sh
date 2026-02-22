#!/bin/bash
set -e

echo "📦 Installing DevPulse..."

# Check if uv is installed
if command -v uv &> /dev/null; then
    echo "✓ Found uv"
    uv tool install .
    echo "✓ DevPulse installed with uv tool"
    echo ""
    echo "Run: devpulse --help"
    exit 0
fi

# Check if pipx is installed
if command -v pipx &> /dev/null; then
    echo "✓ Found pipx"
    pipx install .
    echo "✓ DevPulse installed with pipx"
    echo ""
    echo "Run: devpulse --help"
    exit 0
fi

# Fallback to pip
if command -v pip &> /dev/null; then
    echo "⚠ Using pip (consider installing uv or pipx for isolated installs)"
    pip install -e .
    echo "✓ DevPulse installed with pip"
    echo ""
    echo "Run: devpulse --help"
    exit 0
fi

echo "❌ No Python package manager found"
echo "Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
exit 1
