# Integrating Zigbee ZS06 and UFO-R11 IR Controller with Atoll HD 120 HiFi Receiver



This guide explains how to integrate a Zigbee IR controller (ZS06 or UFO-R11) to control an IR HiFi system via Home Assistant scripts, using the Atoll MS120, HD120, and PR300 receivers as examples.

We then build a full Home Assistant dashboard that includes:
- IR remote controls (preamp, streamer, DAC)
- HiFi smart plugs
- Atoll Signature web UI (iframe)
- Apple TV remote
- HEOS devices
- DLNA renderers
- Lights and shutter (for cinema mode)


## Screenshots

![Dashboard preview 1](media/Screenshot%202026-05-05%20at%2016.10.53.png)
![Dashboard preview 2](media/Screenshot%202026-05-05%20at%2016.11.16.png)
![Dashboard preview 3](media/Screenshot%202026-05-05%20at%2016.11.30.png)

## Useful Links

- [Bitboxer Zigbee IR Integration](https://bitboxer.de/2024/01/20/tuya-zigbee-ir/)
- [Tuya Zigbee IR Remote ZS06 Review](https://smarthomescene.com/reviews/tuya-zigbee-infrared-ir-remote-zs06-review/)
- [Home Assistant Script Integration](https://www.home-assistant.io/integrations/script/)


## 🧰 What You Need

- ZS06 or UFO-R11 Zigbee IR Blaster (Tuya-based)
- Home Assistant with Zigbee2MQTT integration
- Original Atoll remote control (not a universal remote)
- A stable 5V/1A–2.4A USB power supply (e.g., Belkin USB charger)
- Access to Home Assistant at http://homeassistant.local:8123

## ⚙️ Step 1: Power and Placement

Power the ZS06 using a USB port that supplies 5V, 1A.
In the manual they specify 5V, 1A and believed it was not working but I confirmed it works with a Belkin 5V/2.4A charger.
<!-- I also did a test with Ugreen KVM and usb-c to usb-c wire, see also Tahoma 5v/2a from https://asset.somfy.com/Document/8e23bd99-207a-4d1d-a16f-51837aedc229_TaHoma%20switch_Spec%20Sheet_2024.03.18.pdf?__hstc=149881833.1fff4bc756e3af1090162dfd03c9298e.1752316855278.1752316855278.1752316855278.1&__hssc=149881833.1.1752316855278&__hsfp=2679447906 -->

See more inputs on USB voltage: https://en.wikipedia.org/wiki/USB#Power

Position the ZS06 in front of the Atoll HD120 receiver’s IR sensor. Avoid placing it behind the receiver (though it works in my case and initial issue were not caused by that).

## 📡 Step 2: Learn IR Codes from the Atoll Remote

**Zigbee stack choice:** [ZHA](https://www.home-assistant.io/integrations/zha/) vs [Zigbee2MQTT](https://www.zigbee2mqtt.io/) — community consensus is that Z2M offers better device support and flexibility, though with a higher initial setup cost. This guide uses Zigbee2MQTT.

⚠️ Important: Use the original Atoll remote, not a universal remote like “One For All,” as the learning process may fail otherwise.


Go to:
http://homeassistant.local:8123/45df7312_zigbee2mqtt/ingress

Click “Learn IR Code” (e.g., for the Power ON or Mute button).

Press the corresponding button on the Atoll remote while pointing it at the ZS06.

The learned IR code will appear, e.g.:

BZ8N4wa6AUABAzIFugHgIwHgFy9AH0AD4BMBwB/AB+APAeALH0ATAuwBumABAf//gMdAD0AX4CMBQC9AN+APAUAfQAPgEwHAH8AHwAHgB1fgBx9AAQsyBboBugG6AboBugE=

When moving new code toogle on/off learn ir mode.

## 🚀 Step 3: Test the IR Code

Paste the learned code into the IR Send field.
Click outside the text box to trigger the IR signal.
Confirm the Atoll receiver responds (e.g., mutes or powers on).

## 🧪 Step 4: Use the HA Dashboard as an Alternative to Learn & Test IR Codes

On your Home Assistant dashboard:

Click the ⚡ (lightning bolt) icon to send a command.
Press the Mute button twice to generate history.
Click the 👁️ (eye) icon to view the IR code.
Copy the code, e.g.:

BZQN9gasAUABA0cFrAFAAQLmAaxgAUAH4AMDwAHAE0AvwAvAB8ABQA9AH0ADQAtAAUAHQAPAAUALQB9AAUAHQA9AA0AB4AMHQAtAH0ABQAtAA0AB4AMTAf//4AnHwAHAL+AHAcAX4ANHwAFAG0ADQAFAH0ADwA9AAcALQAdAA8AfQAdAAUATwAPAAUAPQB9AB0ABQAdAAwtHBawBrAGsAawBrAE=

in Send. (Note: retrying from the dashboard sometimes fails — using a script as in Step 5 is more reliable.)

## 🧾 Step 5: Create a Script in Home Assistant
Go to:
http://homeassistant.local:8123/config/script/

Create a new script with the learned IR code.

http://homeassistant.local:8123/config/script/dashboard
> create new script > edit in yaml

Example YAML:

````yaml
#Replace Device ID (Friendly name from Zigbee2MQTT) and IR Code
alias: "HD120 Turn ON OFF" #Zigbee2MQTT Script
sequence:
  - service: mqtt.publish
    data:
      payload: >-  #Replace IR Code
        {"ir_code_to_send": "BZkN8wa6AUABAx4FugHgCQEC6QG64AwBAekB4A0v4AEBQB8EHgXpAbrgEAEF6QEeBboB4AkBAukBuuAaAeADOwH//0DHgDcBHgWAB+AFAeALE4ABAx4FugHgEwECHgXpYAMAuuASAUAjALrgGAHgDSMLHgXpAboBugG6AboB"} 
      topic: zigbee2mqtt/0x70c59cfffef600c8/set #Replace Device ID
````


The `0x70c59cfffef600c8` in the topic is the device's friendly name in Zigbee2MQTT (http://homeassistant.local:8123/45df7312_zigbee2mqtt/ingress). By default it equals the IEEE address. Recommended: do not rename it. See: https://www.zigbee2mqtt.io/guide/usage/mqtt_topics_and_messages.html#zigbee2mqtt-friendly-name

**Pro Tips:**
- Install the VS Code add-on to edit scripts in bulk: http://homeassistant.local:8123/a0d7b954_vscode/ingress → edit `scripts.yaml`
- You can duplicate scripts via UI or directly in YAML.
- After editing YAML directly, reload via: **Developer Tools** → **YAML** → **Scripts: Reload**.


## 🧾 Step 6: Industrialize the Solution

<!-- initial yaml built via VS Code + Copilot -->

Workflow for adding new IR commands:

1. **Learn** the IR code: http://homeassistant.local:8123/45df7312_zigbee2mqtt/ingress — [See Step 2](#-step-2-learn-ir-codes-from-the-atoll-remote)
2. **Copy-paste** the script YAML: http://homeassistant.local:8123/a0d7b954_vscode/ingress — [See Step 5](#-step-5-create-a-script-in-home-assistant)
3. **Reload** the config: http://homeassistant.local:8123/developer-tools/yaml
4. **Test** the script: http://homeassistant.local:8123/config/script/dashboard

See [Generated scripts.yaml](scripts.yaml).

**Notes:**
- The device ID in the MQTT topic differs between ZS06 and UFO-R11.
- IR codes learned on one device (UFO-R11 or ZS06) can be used across both.
- In scripts.yaml, each script notes whether it was learned from the global or streamer Atoll remote.

## Step 7: Generate a dashboard

Configure input button: https://www.home-assistant.io/integrations/input_button/#automation-examples:~:text=The%20input_button%20entity%20is%20stateless,%20as%20in,%20it%20cannot%20have%20a%20state%20like

Upload [script.yaml](./scripts.yaml) in AI (or use agentic mode).
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


## 🧠 Tips & Troubleshooting


- If a code doesn’t work (happens when code very long):
  - Ensure re-learning it with the Atoll remote.
  - Power cycle the Atoll receiver before retrying.

- Tuya IR codes are not consistent across learning attempts.
   - This is not due to rolling codes, as mentioned here: https://smarthomescene.com/reviews/tuya-zigbee-infrared-ir-remote-zs06-review/
   - but Tuya’s own encoding format: https://www.reddit.com/r/homeassistant/comments/1di1zs7/ir_codes_formatting/


- On HD120 vol_less and vol_plus needs a long press >5 sec when learning IR code
  - But on PR300 can cause high gap (to fix)
<!-- also mentioned in related section of yaml doc -->
- Solved issue on UFO-R11 by removing batteries
- If a HEOS device disappears, unplug and reconnect/reset it.

## Discovering Entities

To build additional dashboard tabs (plugs, HEOS, Apple TV, DLNA, lights), you need to discover available entities:

- Use [HA MCP](https://github.com/homeassistant-ai/ha-mcp) to discover entities via AI tooling (e.g., Claude/Copilot).
- Alternatively, create an auto-generated dashboard in HA and take manual control of it to inspect all available entities.
- To ensure entity IDs stay in sync with the Hue/Apple TV app names, remove and re-add the respective integration.

See [hifi-dashboard.yaml](./hifi-dashboard.yaml) for the full result.

## TODO

- PR300 volume step improvements (long press causes large jumps)