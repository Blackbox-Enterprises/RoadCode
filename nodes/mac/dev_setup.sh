#!/bin/bash
# Mac development environment setup for Alexandria
set -e

echo "Setting up BlackRoad dev environment..."

# Homebrew packages
brew install python@3.11 node git jq shellcheck ruff 2>/dev/null || true

# Python environment
python3 -m pip install --upgrade pip
python3 -m pip install -e '.[dev,ai]'

# Node packages (if web development)
npm install 2>/dev/null || true

# Verify tools
echo "Python: $(python3 --version)"
echo "Node: $(node --version 2>/dev/null || echo 'not installed')"
echo "Git: $(git --version)"

# Create data directories
mkdir -p data/{cache,logs,snapshots,telemetry}

echo "Dev environment ready."
