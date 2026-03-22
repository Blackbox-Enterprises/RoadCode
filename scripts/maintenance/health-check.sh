#!/bin/bash
# Fleet health check — run from any node
NODES=("192.168.4.49" "192.168.4.96" "192.168.4.101" "192.168.4.98" "192.168.4.38")
NAMES=("Alice" "Cecilia" "Octavia" "Aria" "Lucidia")

for i in "${!NODES[@]}"; do
  if ping -c1 -W2 "${NODES[$i]}" &>/dev/null; then
    echo -e "\033[32m✓\033[0m ${NAMES[$i]} (${NODES[$i]})"
  else
    echo -e "\033[31m✗\033[0m ${NAMES[$i]} (${NODES[$i]})"
  fi
done
