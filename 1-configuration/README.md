# Configuration


## configuration.yaml 

Each folder here maps to an element in Home Assistant's `configuration.yaml`:

Access via vs code plugin: http://homeassistant.local:8123/a0d7b954_vscode

### Folder-based includes (instead of single files)

Instead of using a single `automations.yaml`, `scripts.yaml`, or `scenes.yaml`, we use **folder-based includes**. This lets us drop individual YAML files into directories without manual merging:

```yaml
# automation: !include automations.yaml          # old: single file
automation: !include_dir_merge_list automations/  # new: all YAML files in automations/ are merged as a list

# script: !include scripts.yaml
script: !include_dir_merge_named scripts/         # merged as a named mapping (key: value)

# scene: !include scenes.yaml
scene: !include_dir_merge_list scenes/            # merged as a list
```

### Dashboards in YAML mode

Dashboards are configured directly in `configuration.yaml` using `lovelace: mode: yaml`, so they can also be version-controlled and synced:

```yaml
lovelace:
  mode: yaml
  dashboards:
    lovelace-global:
      mode: yaml
      filename: global-dashboard/global-dashboard.yaml
      title: Dream Home
    lovelace-hifi:
      mode: yaml
      filename: hifi-dashboard/hifi-dashboard.yaml
      title: SLZB Remote
```

Note: `mode: yaml` disables the visual dashboard editor in the HA UI — all edits must be done in the YAML files.

### Syncing to HA

The repo can be cloned on the HA instance and synced using the [sync-to-ha.sh](../sync-to-ha.sh) script. See [sync-to-ha-README.md](../sync-to-ha-README.md) for full instructions.

### Folder mapping

| Folder | `configuration.yaml` directive | Description |
|--------|-------------------------------|-------------|
| [automations/](./automations/) | `automation: !include_dir_merge_list automations/` | Triggered automations |
| [scenes/](./scenes/) | `scene: !include_dir_merge_list scenes/` | Predefined entity states |
| [scripts/](./scripts/) | `script: !include_dir_merge_named scripts/` | Reusable action sequences |
| [pyscript/](./pyscript/) | `pyscript:` | Python scripts with full HA access |


## HA UI

The automation dashboard at http://homeassistant.local:8123/config/automation/dashboard exposes:

- **Automations** — trigger-based logic (from `automations.yaml`)
- **Scenes** — predefined entity states (from `scenes.yaml`, or imported from integrations like Tahoma <!-- legacy go to bed --> and Hue)
- **Scripts** — reusable action sequences (from `scripts.yaml`)
- **Blueprints** — reusable automation/script templates that can be shared ([Blueprint Exchange](https://community.home-assistant.io/c/blueprints-exchange/53))

## Scenes

See [scene/readme-go-to-bed.md](./scene/readme-go-to-bed.md) — explains the "Go to Bed" scene: turns off all lights except dimmed bedroom, closes shutter, opens sunilus. Triggered from dashboard and physical button.

A scene defines the desired state once and can be called from multiple triggers (dashboard, button, voice, automation) without duplicating logic.

## Actions Made Directly in Dashboard

Some actions bypass scripts/automations entirely and are defined inline in the dashboard YAML (e.g., HEOS group/ungroup buttons in the [HiFi Dashboard](../2-dashboards/hifi-dashboard/hifi-dashboard.yaml)).

