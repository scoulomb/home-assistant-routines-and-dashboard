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

(Example of Ikea MYGGBETT Capteur fenêtre/porte, Eve Weather (thread))

1. Enable Bluetooth on your phone
2. In the HA app go to **Settings → Devices & Services → Devices** tab
3. Tap **+ ADD DEVICE → Add Matter device**
4. For a **standard Matter device**: say new device and scan the QR code on the device
5. For an **IKEA Thread/matter device** (even if new and unpaired): first factory reset it (hold the reset button for 10 seconds until it blinks red), then select **Yes, it's already in use** → **Other controllers** → enter the setup code printed on the device (what works for myggbet device)


> If the device doesn't pair, it may need a factory reset to re-enter pairing mode. Also try turning off any Google Home / Nest Hub devices before starting the OTBR add-on.

> **Note:** We did not explore using Google Nest Hub or Apple TV 4K as Thread Border Routers here. These can coexist on the same Thread mesh and allow sharing Matter devices across controllers (HA, Google Home, Apple Home) via multi-fabric. However, Apple border routers block mDNS, which prevents OTA updates from HA. The SLZB OTBR remains the best option for a fully local, vendor-independent setup.


## Verify

Once paired, the device should appear in your HA Dashboard and under **Devices**. You can control it from there.

## Notes

- This setup uses **Radio 1 (EFR32MG24)** for Thread/Matter on port `6638`, while **Radio 2 (CC2652P10)** stays on Zigbee Coordinator for Z2M on port `7638` (see [slzb-zigbee.md](slzb-zigbee.md)). Both radios run simultaneously. But each radio can be set to either Zigbee or Thread mode, but not both at the same time — configure via http://192.168.8.192/mode
- HA Thread/Matter docs: https://www.home-assistant.io/integrations/thread/
- SMLIGHT video tutorial: https://www.youtube.com/watch?v=WwYVRuVpAJI

- See https://www.youtube.com/watch?v=6NqeShjuBuU (with MRW-10 which I did not use mine here, which support z-wave)

## Note on devices

### IKEA Devices

#### Second generation of Ikea devices

Some IKEA devices support both Matter-over-Thread and Zigbee (e.g. **MYGGBETT** contact sensor). These could alternatively be converted to Zigbee mode and paired via Z2M on Radio 2 — see [slzb-zigbee.md](slzb-zigbee.md) for the Zigbee setup.

#### First generation of Ikea devices

Older IKEA devices are **pure Zigbee** and cannot use Matter at all:
- **RODRET** (E2201) — wireless dimmer/power switch, 1 x AAA battery (1.2V rechargeable recommended)
- **SOMRIG** (E2213) — shortcut button, 1 x AAA battery (1.2V rechargeable recommended)
<-- I will use hue button -->

These pair directly via Z2M on Radio 2 (port `7638`), not through the Matter flow described above. See [SLZB Zigbee](./slzb-zigbee.md) (they use [radio 2](#notes))


### Hue devices

Hue bulbs have shipped with three different radio sets over time, so "generation" is ambiguous. What actually matters for this setup is **which radios a bulb has** — and specifically whether it has **Thread**. Bluetooth never mattered for Hue/HA routing; it only ever enabled app-only control of a single bulb without a bridge.

| Era | Radios | What it means here |
|-----|--------|--------------------|
| Pre-2019 | Zigbee only | Needs a bridge (or Z2M) for any control |
| Mid-2019 → 2025 | Zigbee **+ Bluetooth** | Bluetooth = app-only control without a bridge; still **Zigbee** for Hue Bridge / HA |
| Late 2025 → | Zigbee + Bluetooth **+ Thread** | Can do **Matter-over-Thread** directly — see below |

Sources: [Wikipedia — Philips Hue](https://en.wikipedia.org/wiki/Philips_Hue), [Signify 2019 Bluetooth launch](https://www.signify.com/en-us/our-company/news/press-releases/2019/20190627-signify-launches-philips-hue-with-bluetooth).


#### Zigbee bulbs (everything before late 2025)

> **Note:** Whether or not a bulb also has Bluetooth, all pre-2025 Hue devices are **Zigbee** for our purposes — they have no Thread radio and no native Matter. (Bluetooth only lets the Hue app talk to one bulb directly; it can't join HA's Zigbee or Thread mesh.)

The Hue Bridge can expose these Zigbee devices to Matter controllers via **Matter bridging**, but we don't use that path here. The [native HA Hue integration](https://www.home-assistant.io/integrations/hue/) talks to the bridge directly and offers richer features (scenes, dynamic scenes, effects, entertainment zones).

To skip the bridge entirely, Hue devices (dimmer switches, motion sensors, bulbs) can be paired directly to [Z2M on Radio 2](#notes) — see [slzb-zigbee.md](slzb-zigbee.md).

> **Note — Hue Smart Plug:** the Hue Smart Plug is **Zigbee + Bluetooth** (no Thread, no native Matter), so it behaves exactly like the Zigbee bulbs above. Bluetooth is only for app-only control of the plug without a bridge; for Hue/HA it runs over Zigbee. Use it via the Hue Bridge (optionally Matter-bridged over IP) or pair it directly to [Z2M on Radio 2](#notes). There is no Thread/Matter-over-Thread Hue plug. ([product page](https://www.philips-hue.com/en-gb/p/hue-smart-plug/8719514342323))

> **Note — Matter transports:** Matter can run over different links. The Hue Bridge bridges its Zigbee devices to Matter **over IP** (Ethernet on the standard square Bridge V2; Bridge Pro adds Wi-Fi; the old round v1 Bridge never got Matter). By contrast, the [second-generation IKEA devices](#second-generation-of-ikea-devices) used here are **Matter-over-Thread**. See [Netatmo's Matter guide](https://www.netatmo.com/en-eu/smart-home-guide/matter-standard-smart-home) for an overview.


#### Thread-capable bulbs (late 2025 onward)

> **Note (future):** Newer Hue bulbs ship with a **Thread** radio alongside Zigbee and Bluetooth.

Today you must choose **one** protocol at setup — Zigbee (via the Hue Bridge) **or** Matter-over-Thread (direct to a Thread border router).

Signify and Silicon Labs have announced **concurrent multiprotocol (CMP)**: a software update due later in 2026 will let a single bulb run **Zigbee and Matter-over-Thread simultaneously**, so a bulb can stay on the Hue Bridge *and* expose a direct Matter-over-Thread connection at the same time. See [Hueblog](https://hueblog.com/2026/06/23/hue-bulbs-will-soon-connect-simultaneously-via-thread-and-zigbee/) and [The Verge](https://www.theverge.com/tech/955767/philips-hue-thread-matter-zigbee-update-silicon-labs).

For these bulbs we therefore have three options:

1. **Hue Bridge (Zigbee)** — same as the [Zigbee bulbs](#zigbee-bulbs-everything-before-late-2025) above, with optional Matter bridging over IP if you want to expose them to other Matter controllers.
2. **Z2M on Radio 2 (Zigbee)** — paired directly, bypassing the Hue Bridge (see [slzb-zigbee.md](slzb-zigbee.md)).
3. **Matter-over-Thread** — paired directly to our SLZB OTBR (Radio 1) or any other Thread border router, exactly like the [second-generation IKEA devices](#second-generation-of-ikea-devices). The bulb becomes a Matter-over-Thread device.

> **Important — the Hue Bridge is not a Thread border router:** Both the standard Hue Bridge and the newer **Bridge Pro** connect to lights over **Zigbee**, and bridge them to Matter over IP (the Bridge Pro adds Wi-Fi/bluetooth for its own uplink to your router, plus the same IP-based Matter bridging as the standard Bridge). Neither bridge acts as a **Thread border router**: a Thread-capable Hue bulb does **not** join the Hue Bridge over Thread. Its Matter-over-Thread connection goes to a *separate* Thread border router — our SLZB OTBR (Radio 1), or an Apple/Google/Amazon/Nanoleaf hub.
>
> The official [spec sheet](https://www.philips-hue.com/fr-fr/p/hue-bridge-pro/8720169155114) confirms that.

Reportedly Thread-capable models include the Hue Essential GU10/E27, current-gen E27, E12/E14 candle, and Hue Slim recessed, with more to follow (per [Hueblog](https://hueblog.com/2026/06/23/hue-bulbs-will-soon-connect-simultaneously-via-thread-and-zigbee/)).

> **Don't rely on the "Matter" logo to spot Thread bulbs:** *every* Hue bulb "works with Matter" — the older ones only via the bridge (Matter bridging over IP). So a Matter logo on the box says nothing about whether the bulb has a built-in **Thread** radio. To get a bulb that can do **Matter-over-Thread directly (no bridge)**, confirm explicit **Thread** support in the product specs — or check it's one of the new Thread-capable models listed above — rather than trusting the Matter badge alone.


#### Hue Bridge generations

The bridge itself has gone through three hardware generations. Only the square v2 and the Bridge Pro matter today; both are **Zigbee** hubs that bridge to Matter over IP (neither is a Thread border router — see the note above).

| Generation | Shape | Released | Matter | Network uplink | Status |
|------------|-------|----------|--------|----------------|--------|
| **v1** | Round | 2012 | ❌ never | Ethernet only | **Ethernet + Zigbee only — no Bluetooth, no Wi-Fi.** End of support since 30 Apr 2020 — local control only, no updates/remote ([Hue dev blog](https://developers.meethue.com/important-news-about-bridge-v1/)) |
| **v2** | Square | 2015 | ✅ via free software update | Ethernet only | **Ethernet + Zigbee only — no Bluetooth, no Wi-Fi.** Also added HomeKit; even 7-year-old units got the Matter update |
| **Bridge Pro** | Square (larger) | 2025 | ✅ (via the bridge) | **Ethernet + Wi-Fi + Bluetooth + Zigbee — no Thread in the hub (only the bulbs can be Thread)** | First bridge with **Bluetooth + Wi-Fi**. "Hue Chip Pro", ~150 lights / 50 accessories, MotionAware ([spec sheet](https://www.philips-hue.com/fr-fr/p/hue-bridge-pro/8720169155114)) |

> **Note — the Bridge Pro's Bluetooth/Wi-Fi (new with this model):** the v1 and v2 bridges connect only over **Ethernet** and have no Bluetooth or Wi-Fi (Bluetooth on Hue was a *bulb/plug* feature from 2019, for bridge-free app control — not a bridge feature). The Bridge Pro is the first to add both, and its official [spec sheet](https://www.philips-hue.com/fr-fr/p/hue-bridge-pro/8720169155114) lists its protocols as **Bluetooth + Zigbee*** (compatibility) (no Thread; Matter is "via the bridge"). Bluetooth is for **setup**, not for running your lights — because the Bridge Pro can join the network over Wi-Fi instead of Ethernet, the Hue app uses Bluetooth during onboarding to hand the bridge its Wi-Fi credentials and complete guided setup. Day-to-day, lights still run over **Zigbee**. The absence of a Thread radio also confirms the Bridge Pro is **not** a Thread border router.<!-- assume OK -->

> **Note:** If you want Hue devices in Home Assistant via the native [Hue integration](https://www.home-assistant.io/integrations/hue/), you need a **v2 or Bridge Pro** (the v1 round bridge is out of support and has no Matter). Or skip the bridge entirely and pair devices to [Z2M on Radio 2](#notes).

> **Footnote — take Hue's roadmap statements with a grain of salt:** back in 2022, Hue's Head of Technology George Yianni said the company had no plans to build Thread bulbs — interview titled ["We don't have plans to build Thread light bulbs"](https://matter-smarthome.de/en/interview/we-dont-have-plans-to-build-thread-light-bulbs/). He hedged it ("I don't say never... very much a wait-and-see approach"), arguing that a bridge would still be needed as the system's local intelligence and that Thread at scale was unproven. By late 2025 they shipped Thread bulbs anyway — so treat any "no plans" / "coming later" claims (including the CMP update above) as subject to change.

<!-- recent e14 june 26 no thread written in box -->
<!-- OK CCL -->