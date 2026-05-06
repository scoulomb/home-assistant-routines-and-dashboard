
# HiFi dashboard

## Screenshots

![Dashboard preview 1](media/Screenshot%202026-05-05%20at%2016.10.53.png)
![Dashboard preview 2](media/Screenshot%202026-05-05%20at%2016.11.16.png)
![Dashboard preview 3](media/Screenshot%202026-05-05%20at%2016.11.30.png)

## Generate a Dashboard from IR Scripts

This dashboard is built on top of the IR scripts defined in [zigbee-ZS06-and-UFO-R11.md](../../1-configuration/script/zigbee-tuya-ir-module-with-slzb/zigbee-ZS06-and-UFO-R11.md) (Steps 1–6 cover learning IR codes, creating scripts, and industrializing the solution) and other integrations (HUE, Heos, pyscript...).

Configure input button: https://www.home-assistant.io/integrations/input_button/#automation-examples:~:text=The%20input_button%20entity%20is%20stateless,%20as%20in,%20it%20cannot%20have%20a%20state%20like

Upload [scripts.yaml](../../1-configuration/script/zigbee-tuya-ir-module-with-slzb/scripts.yaml) in AI (or use agentic mode).
Use this prompt.

```chatinput
I have a list of Home Assistant scripts for devices like HD120, MS120, AVR, and Optoma. I want to create a YAML configuration for a dashboard that:

Groups buttons into logical sections using vertical-stack cards.
Each group should have a title using a markdown card (e.g., “HD120 Controls”, “MS120 Controls”, etc.).
Inside each group, use a grid layout to display buttons for the scripts.
Each button should include:
show_name: true
show_icon: true
type: button
tap_action: { action: toggle }
Output the full YAML configuration.
Example script names include:

hd120_turn_on_off, hd120_mute, hd120_disp, ...
ms120_turn_on_off, ms120_vol_plus, ...
avr_on_off, avr_vol_plus, ...
optoma_on, optoma_off
Please generate a clean, readable YAML layout that I can paste into my Home Assistant dashboard configuration.
```

In `HA dashboard` > `add card` > `manual` (at bottom)

```yaml
type: vertical-stack
cards:
# <copy-paste AI generated output>
```

Rather than adding individual cards manually, generate the entire dashboard YAML. See [hifi-dashboard.yaml](./hifi-dashboard.yaml).

## Discovering Entities

To build additional dashboard tabs (plugs, HEOS, Apple TV, DLNA, lights), you need to discover available entities:

- Use [HA MCP](https://github.com/homeassistant-ai/ha-mcp) to discover entities via AI tooling (e.g., Claude/Copilot).
- Alternatively, create an auto-generated dashboard in HA and take manual control of it to inspect all available entities.
- To ensure entity IDs stay in sync with the Hue/Apple TV app names, remove and re-add the respective integration.

See [hifi-dashboard.yaml](./hifi-dashboard.yaml) for the full result.

