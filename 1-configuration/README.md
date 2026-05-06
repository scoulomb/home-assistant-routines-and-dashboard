# Configuration


## configuration.yaml 

Each folder here maps to an element in Home Assistant's `configuration.yaml`:

Access via vs code plugin: http://homeassistant.local:8123/a0d7b954_vscode

```yaml
pyscript:
  allow_all_imports: true
  hass_is_global: true
  legacy_decorators: true

automation: !include automations.yaml
script: !include scripts.yaml
scene: !include scenes.yaml

shell_command:
  hello: "echo hello"
  play_qobuz_dressing: "/bin/sh -c 'python3 /config/scripts/play_qobuz_favorites.py 192.168.8.190 dressing 42 &'"
```

| Folder | `configuration.yaml` element | Description |
|--------|------------------------------|-------------|
| [automation/](./automation/) | `automation: !include automations.yaml` | Triggered automations |
| [pyscript/](./pyscript/) | `pyscript:` | Python scripts with full HA access |
| [scene/](./scene/) | `scene: !include scenes.yaml` | Predefined entity states |
| [script/](./script/) | `script: !include scripts.yaml` | Reusable action sequences |
| [shell-command/](./shell-command/) | `shell_command:` | OS-level shell commands |


## HA UI

The automation dashboard at http://homeassistant.local:8123/config/automation/dashboard exposes:

- **Automations** — trigger-based logic (from `automations.yaml`)
- **Scenes** — predefined entity states (from `scenes.yaml`, or imported from integrations like Tahoma and Hue)
- **Scripts** — reusable action sequences (from `scripts.yaml`)
- **Blueprints** — reusable automation/script templates that can be shared ([Blueprint Exchange](https://community.home-assistant.io/c/blueprints-exchange/53))

## Actions Made Directly in Dashboard

Some actions bypass scripts/automations entirely and are defined inline in the dashboard YAML (e.g., HEOS group/ungroup buttons in the [HiFi Dashboard](../2-dashboards/hifi-dashboard/hifi-dashboard.yaml)).