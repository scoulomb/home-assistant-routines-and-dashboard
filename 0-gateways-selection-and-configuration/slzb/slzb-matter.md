# SLZB Matter-over-Thread Setup

> **Prerequisite:** Read [slzb-zigbee.md](slzb-zigbee.md) first, which covers the Zigbee setup with Z2M on Radio 2.

Reference: https://smlight.tech/manual/slzb-06/guide/thread-matter/

## Prerequisites

- Home Assistant OS running
- SLZB-MR3 connected via Ethernet (IP: `192.168.8.192`)
- A Matter-over-Thread end device to pair
- An Android smartphone (iOS pairing may not work reliably)

## Step 1 — Flash the Radio to Matter-over-Thread Mode

1. Go to the SLZB Mode page: http://192.168.8.192/mode
2. Under **Radio 1 [EFR32MG24]**, select **Matter-over-Thread**
3. The device will reflash the radio firmware automatically — wait for it to complete

After flashing, Radio 1 settings should be:
- Socket Port: `6638`
- Serial Speed: `460800`

> Radio 2 [CC2652P10] can remain on Zigbee Coordinator for Z2M usage (port `7638`). Both radios work independently. See [slzb-zigbee.md](slzb-zigbee.md).

## Step 2 — Install the OpenThread Border Router App (formerly called add-ons)

1. Go to http://homeassistant.local:8123/config/apps/available
2. Search for **OpenThread Border Router** and click **Install**
3. Wait for the installation to complete
4. Set this configuration:

```yaml
device: /dev/ttyAMA10
baudrate: "460800"
flow_control: false
otbr_log_level: notice
firewall: false
nat64: false
beta: false
network_device: 192.168.8.192:6638
```

5. Start the add-on

> Here we connect over the network (not via USB). USB is usually recommended.

> **Note:** Hostname is `core-openthread-border-router` and we use the default port `8081`.

## Step 3 — Install the Matter Server Add-on and Integration

1. Go to **Settings → Devices & Services** http://homeassistant.local:8123/config/integrations/dashboard
2. Click **Add Integration** and search for **Matter**
3. Keep the checkbox **Use the official Matter Server Supervisor add-on** and click **Submit**
4. Wait for installation to complete
5. Go to **Settings → Add-ons → Matter Server**, start it, and enable **Start on boot** and **Watchdog**

## Step 4 — Configure Thread Integration

1. Go to **Settings → Devices & Services**
2. Both **Thread** and **OpenThread Border Router** integrations should be auto-discovered — configure/add them
3. For **OpenThread Border Router** — no configuration needed, just add it
4. For **Thread** — click **Configure** and verify that `OpenThread Border Router` appears under **Preferred network** with a key+phone icon. If not:
   - Click the three dots next to `OpenThread Border Router` → **Add to preferred network**
   - Then click the three dots again → **Use router for Android + iOS credentials**

## Step 5 — Reboot Home Assistant

Reboot via **Settings → System → Restart** to ensure all components initialize properly.

## Step 6 — Prepare your Phone

1. Install the **Home Assistant** app on your Android phone
<!-- Install the **Google Home** app (recommended by HA devs; pairing may fail without it) -->
2. Open the HA app and connect it to your server (phone and HA must be on the same Wi-Fi)
3. In the app go to **Settings → Devices & Services → Thread** and tap **Send credentials to phone** (not ~~Companion App → Debug~~)


We also see there Google Nest Border router.

> **Note:** Don't confuse apps (formerly called add-ons), integrations, and HACS (which is itself installed via an app).

## Step 7 — Add a Matter Device

1. Enable Bluetooth on your phone
2. In the HA app go to **Settings → Devices & Services → Devices** tab
3. Tap **+ ADD DEVICE → Add Matter device**
4. For a **standard Matter device**: say nw device and scan the QR code on the device
5. For an **IKEA Thread/matter device** (even if new and unpaired): first factory reset it (hold the reset button for 10 seconds until it blinks red), then select **Yes, it's already in use** → **Other controllers** → enter the setup code printed on the device (what works for myggbet device)


> If the device doesn't pair, it may need a factory reset to re-enter pairing mode. Also try turning off any Google Home / Nest Hub devices before starting the OTBR add-on.

> **Note:** We did not explore using Google Nest Hub or Apple TV 4K as Thread Border Routers here. These can coexist on the same Thread mesh and allow sharing Matter devices across controllers (HA, Google Home, Apple Home) via multi-fabric. However, Apple border routers block mDNS, which prevents OTA updates from HA. The SLZB OTBR remains the best option for a fully local, vendor-independent setup.

> **Note:** Philips Hue devices do not use Matter (the Hue Bridge supports Matter bridging, but the native HA Hue integration provides richer features). See [home-assistant/sound-video](../../sound-video).

> **Note:** Matter can run over different transports. Hue Bridge exposes devices as Matter-over-Ethernet/Wi-Fi (for bridge pro), whereas (new Matter) IKEA devices used here are Matter-over-Thread. See [Netatmo's Matter guide](https://www.netatmo.com/en-eu/smart-home-guide/matter-standard-smart-home) for a good overview.

Alternatively, Hue devices (e.g. dimmer switches, motion sensors, bulbs) can be paired directly to Z2M on Radio 2, bypassing the Hue Bridge entirely — see [slzb-zigbee.md](slzb-zigbee.md).

## Verify

Once paired, the device should appear in your HA Dashboard and under **Devices**. You can control it from there.

## Notes

- This setup uses **Radio 1 (EFR32MG24)** for Thread/Matter on port `6638`, while **Radio 2 (CC2652P10)** stays on Zigbee Coordinator for Z2M on port `7638` (see [slzb-zigbee.md](slzb-zigbee.md)). Both radios run simultaneously. But each radio can be set to either Zigbee or Thread mode, but not both at the same time — configure via http://192.168.8.192/mode
- HA Thread/Matter docs: https://www.home-assistant.io/integrations/thread/
- SMLIGHT video tutorial: https://www.youtube.com/watch?v=WwYVRuVpAJI

- See https://www.youtube.com/watch?v=6NqeShjuBuU (with MRW-10 which I did not use mine here, which support z-wave)


## IKEA Devices

Some IKEA devices support both Matter-over-Thread and Zigbee (e.g. **MYGGBETT** contact sensor). These could alternatively be converted to Zigbee mode and paired via Z2M on Radio 2 — see [slzb-zigbee.md](slzb-zigbee.md) for the Zigbee setup.

Other IKEA devices are **pure Zigbee** and cannot use Matter at all:
- **RODRET** (E2201) — wireless dimmer/power switch, 1 x AAA battery (1.2V rechargeable recommended)
- **SOMRIG** (E2213) — shortcut button, 1 x AAA battery (1.2V rechargeable recommended)
<-- I will use hue button -->

These pair directly via Z2M on Radio 2 (port `7638`), not through the Matter flow described above.


<!-- OK CCL -->