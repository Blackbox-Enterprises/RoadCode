#!/bin/bash
set -e

# Bootstrap a new RoadCode node
echo "Initializing RoadCode..."
python3 -m venv .venv 2>/dev/null || true
source .venv/bin/activate 2>/dev/null || true
pip install -e . 2>/dev/null || true
npm install 2>/dev/null || true
mkdir -p data/{cache,logs,snapshots}
echo "RoadCode initialized."
