# MOES UFO-R11 Stops Responding After 15-30 Minutes

Reference: [zigbee2mqtt#23686](https://github.com/Koenkk/zigbee2mqtt/issues/23686) (closed as not planned)

## Problem

The MOES UFO-R11 (battery-powered Zigbee IR blaster) stops responding to MQTT commands after 15-30 minutes of inactivity. Once unresponsive, it silently ignores any published topics (IR code send, learn mode toggle, etc.). The device appears to enter a low-power sleep mode and never recovers on its own.

### Symptoms

- IR codes sent via MQTT silently fail after 15-30 minutes of idle time
- Device shows as online in Zigbee2MQTT but does not execute commands
- In some cases, the device starts spamming updates several times per second and refuses to send codes while in that state
- The only recovery is removing the batteries or re-pairing the device

### Reproduction

1. Join a UFO-R11 to the Zigbee network
2. Do not interact with it for 15-30 minutes
3. Try to send an IR code — it will silently fail

## Workarounds & Solutions

### Solution 1: Change reporting interval (recommended first try)

Reduce the reporting interval in Zigbee2MQTT so the device reports battery level frequently (e.g., every 60 seconds). This keeps the device awake and responsive.

In Zigbee2MQTT, go to the device's **Reporting** tab and set:
- **Cluster:** genPowerCfg
- **Attribute:** batteryPercentageRemaining
- **Minimum report interval:** 60 seconds
- **Maximum report interval:** 60 seconds
- **Minimum change:** 1

This forces the device to report battery level every minute, preventing it from entering deep sleep. Trade-off: increased battery drain.

> *"With this setting, the device reports the battery level every minute and thus remains responsive. I haven't had a single problem since I started using these settings."* — @zinserjan

Note: this workaround does not work reliably for everyone. Some users report the device becomes unresponsive again after a few hours even with aggressive reporting.

### Solution 2: Send a '0' before the actual IR code

Before sending the real IR code, first set `ir_code_to_send` to `'0'`, wait ~100ms, then send the actual code. This resets something internally and makes the send more reliable.

```yaml
sequence:
  - service: mqtt.publish
    data:
      payload: '{"ir_code_to_send": "0"}'
      topic: zigbee2mqtt/DEVICE_ID/set
  - delay:
      milliseconds: 100
  - service: mqtt.publish
    data:
      payload: '{"ir_code_to_send": "YOUR_IR_CODE_HERE"}'
      topic: zigbee2mqtt/DEVICE_ID/set
```

> This workaround reportedly stopped working after updating to Zigbee2MQTT 1.40.0.

### Solution 3: Add delays between consecutive IR sends

If your automations send multiple IR codes in sequence, add a small delay between each send. This prevents the device from entering the "spamming" state where it sends rapid updates and stops processing commands.

> *"Mine can run for months now without getting into the funky spam state. That may or may not be because I have changed my home assistant automations to wait a little between sending consecutive IR codes."* — @DanielKinsman

### Solution 4: Switch to a USB-powered alternative

If none of the above work reliably, consider replacing the battery-powered UFO-R11 with a USB-powered Zigbee IR blaster such as the [Tuya iH-F8260](https://www.zigbee2mqtt.io/devices/iH-F8260.html). It presents identically in Zigbee2MQTT (same chipset and code) but does not have the sleep/power issue since it is always powered.

Trade-off: requires USB power, limiting placement options.

> IR codes learned on the UFO-R11 may differ in length from those learned on USB-powered devices (3-4x longer codes reported on the USB version for the same remote button).

### What we did

We use the **ZS06** (USB-powered) as primary IR blaster. When using the UFO-R11, we apply **Solution 1** (reduced reporting interval).

See also the troubleshooting section in [zigbee-ZS06-and-UFO-R11.md](zigbee-ZS06-and-UFO-R11.md#-tips--troubleshooting).
