# Sync to Home Assistant

## What it does

[sync-to-ha.sh](./sync-to-ha.sh) copies files from this repo into the Home Assistant `/config/` directory, so that HA picks them up automatically.

| Repo path | Copied to | HA config directive |
|---|---|---|
| `1-configuration/automations/` | `/config/automations/` | `automation: !include_dir_merge_list automations/` |
| `1-configuration/scenes/` | `/config/scenes/` | `scene: !include_dir_merge_list scenes/` |
| `1-configuration/scripts/` | `/config/scripts/` | `script: !include_dir_merge_named scripts/` |
| `1-configuration/pyscript/…/*.py` | `/config/pyscript/` | `pyscript:` |
| `1-configuration/configuration.yaml` | `/config/configuration.yaml` | — |
| `2-dashboards/global-dashboard/` | `/config/global-dashboard/` | `lovelace.dashboards.lovelace-global` |
| `2-dashboards/hifi-dashboard/` | `/config/hifi-dashboard/` | `lovelace.dashboards.lovelace-hifi` |

It also creates an empty `/config/ui-lovelace.yaml` if it doesn't exist (required by `lovelace: mode: yaml`).

## Prerequisites

- SSH or VS Code add-on terminal access to HA
- Git installed on HA (available via the SSH add-on)

## Usage

```bash
# First time: clone the repo
cd /root/custom-git-repo
# Tip: the VS Code add-on terminal does not support paste, so create a
# small shell script with the git clone command, chmod u+x it, and run it.
git clone git@github.com:scoulomb/home-assistant-routines-and-dashboard.git

# Sync (first time and after each change)
cd /root/custom-git-repo/home-assistant-routines-and-dashboard
git pull && bash sync-to-ha.sh
```

Then reload or restart from [Developer Tools → YAML](http://homeassistant.local:8123/developer-tools/yaml).

## Notes

- The script is **idempotent** — safe to run multiple times, it overwrites existing files.
- It does **not** delete files from `/config/` that were removed from the repo. If you delete a file from the repo, remove it manually from `/config/`.
- The `configuration.yaml` in this repo includes `!include_dir_merge_list` and `!include_dir_merge_named` directives, so HA auto-discovers all YAML files dropped into the `automations/`, `scenes/`, and `scripts/` folders — no manual merge needed.
