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

> **Warning**: Dashboard name/title updates or the deprecation fix (removing top-level `mode: yaml`) may require a **full HA restart** — a YAML reload is not sufficient.

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

### Scene vs Script

- **Scene** — declares a **snapshot of entity states** (e.g., light brightness, shutter position). HA applies all states simultaneously. Use when you want to set multiple entities to known states.
- **Script** — defines a **sequence of actions** (service calls, delays, conditions, templates). Use when you need logic, ordering, or actions that aren't just setting entity states (e.g., sending IR codes, calling `media_player.volume_up`, toggling with a template).

In short: scenes are *what state*, scripts are *what to do*.

Both scenes and scripts can be triggered(triggers) from [automations](./automations/) (via `action: scene.turn_on` / `action: script.turn_on`), [dashboards](../2-dashboards/) (via button `tap_action`), physical buttons, or voice assistants. 

For example, the [HiFi Dashboard](../2-dashboards/hifi-dashboard/hifi-dashboard.yaml) calls AVR scripts (`script.heos_avr_on_off`, `script.heos_avr_vol_plus`, …) via button tap actions.

 A script can also call other scripts to compose reusable sequences. For example, the [Global Dashboard](../2-dashboards/global-dashboard/global-dashboard.yaml) Cinema button calls [`script.cinema_on`](./scripts/cinema/cinema-script.yaml), which in turn calls [`script.heos_avr_on_off`](./scripts/heos-avr/heos-avr-scripts.yaml) and [`script.heos_avr_8k`](./scripts/heos-avr/heos-avr-scripts.yaml).

## Actions Made Directly in Dashboard

Some actions bypass scripts/scenes entirely and are defined inline in the dashboard YAML (e.g., HEOS group/ungroup buttons in the [HiFi Dashboard](../2-dashboards/hifi-dashboard/hifi-dashboard.yaml)). The tradeoff is that inline actions cannot be reused by automations or other triggers.
