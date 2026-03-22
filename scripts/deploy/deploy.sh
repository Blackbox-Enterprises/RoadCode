#!/bin/bash
set -e

# Deploy RoadCode to target node
PINK='\033[38;5;205m'
GREEN='\033[38;5;82m'
RESET='\033[0m'

TARGET="${1:-all}"
VERSION="${2:-latest}"

echo -e "${PINK}╔═══════════════════════════════════════╗${RESET}"
echo -e "${PINK}║  RoadCode Deploy — v${VERSION}            ║${RESET}"
echo -e "${PINK}╚═══════════════════════════════════════╝${RESET}"

NODES=(
  "alice:192.168.4.49"
  "cecilia:192.168.4.96"
  "octavia:192.168.4.101"
  "aria:192.168.4.98"
  "lucidia:192.168.4.38"
)

deploy_node() {
  local NAME="${1%%:*}"
  local IP="${1##*:}"
  echo -e "${GREEN}Deploying to ${NAME} (${IP})...${RESET}"
  ssh -o ConnectTimeout=5 "blackroad@${IP}" "cd /opt/roadcode && git pull && systemctl restart roadcode" 2>/dev/null || \
    echo "  Warning: Could not deploy to ${NAME}"
}

if [ "$TARGET" = "all" ]; then
  for node in "${NODES[@]}"; do
    deploy_node "$node"
  done
else
  for node in "${NODES[@]}"; do
    if [[ "$node" == "$TARGET:"* ]]; then
      deploy_node "$node"
    fi
  done
fi

echo -e "${GREEN}Deploy complete.${RESET}"
