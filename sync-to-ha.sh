#!/bin/bash
# sync-to-ha.sh
# Run this on the Home Assistant instance (SSH or VS Code add-on terminal)
# after cloning the repo into /root/custom-git-repo/
#
# Usage:
#   cd /root/custom-git-repo/home-assistant-routines-and-dashboard
#   git pull && bash sync-to-ha.sh
#
# What it does:
#   Copies files from the repo's 1-configuration/ and 2-dashboards/ folders
#   into /config/. Run git pull first, then this script to sync.

set -euo pipefail

REPO_DIR="/root/custom-git-repo/home-assistant-routines-and-dashboard"
CONFIG_DIR="/root/config"

echo "=== Syncing repo to Home Assistant config ==="

# --- 1-configuration: automations, scenes, scripts ---
for folder in automations scenes scripts; do
  echo "Copying ${folder}/"
  mkdir -p "${CONFIG_DIR}/${folder}"
  cp -r "${REPO_DIR}/1-configuration/${folder}/"* "${CONFIG_DIR}/${folder}/"
done

# --- pyscript ---
echo "Copying pyscript files"
mkdir -p "${CONFIG_DIR}/pyscript"
cp "${REPO_DIR}/1-configuration/pyscript/heos-music-jukebox-button/"*.py "${CONFIG_DIR}/pyscript/"

# --- configuration.yaml ---
echo "Copying configuration.yaml"
cp "${REPO_DIR}/1-configuration/configuration.yaml" "${CONFIG_DIR}/configuration.yaml"

# --- 2-dashboards: global-dashboard, hifi-dashboard ---
for folder in global-dashboard hifi-dashboard; do
  echo "Copying ${folder}/"
  mkdir -p "${CONFIG_DIR}/${folder}"
  cp -r "${REPO_DIR}/2-dashboards/${folder}/"*.yaml "${CONFIG_DIR}/${folder}/"
done

# --- ui-lovelace.yaml (required by mode: yaml) ---
if [ ! -e "${CONFIG_DIR}/ui-lovelace.yaml" ]; then
  echo "views: []" > "${CONFIG_DIR}/ui-lovelace.yaml"
  echo "Created empty ui-lovelace.yaml"
fi

echo ""
echo "=== Done ==="
echo "Reload YAML or restart Home Assistant to apply changes:"
echo "  http://homeassistant.local:8123/developer-tools/yaml"
