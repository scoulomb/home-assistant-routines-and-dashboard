# Home Assistant Routines & Dashboard

Content originally in https://github.com/scoulomb/home-assistant/blob/main/2025-new-gen-setup/README.md, moved to this external repo.

## Table of Contents

- **0 — [Gateways Selection & Configuration](./0-gateways-selection-and-configuration/slzb/)**
- **1 — [Configuration](./1-configuration/)**
- **2 — [Dashboards](./2-dashboards/)**

## TODO

- **HiFi Dashboard**: Adjust PR300 volume step (long press causes large jumps)
- **Go to bed scenes**:
  - ~~"Go to Bed"~~ — done: [scene](./1-configuration/scene/readme-go-to-bed.md), [automation](./1-configuration/automation/go-to-bed-automation.yaml), [dashboard](./2-dashboards/global-dashboard/global-dashboard.yaml)
  - ~~"Wake-up"~~ — done: [scene](./1-configuration/scene/wake-up-scene.yaml), [automation](./1-configuration/automation/wake-up-automation.yaml), [dashboard](./2-dashboards/global-dashboard/global-dashboard.yaml)
- Other options:
  - ~~"Play random music"~~ — done: [script](./1-configuration/script/play-random-music-script.yaml), [dashboard](./2-dashboards/global-dashboard/global-dashboard.yaml) (uses [pyscript](./1-configuration/pyscript/heos-music-jukebox-button/play_qobuz_favorites_pyscript.py))
  - ~~"Stop all music"~~ — done: [script](./1-configuration/script/stop-music/stop-music-script.yaml), [dashboard](./2-dashboards/global-dashboard/global-dashboard.yaml)
  - ~~"Cut music plug"~~ — done: [script](./1-configuration/script/stop-music/stop-music-script.yaml), [dashboard](./2-dashboards/global-dashboard/global-dashboard.yaml)
  - ~~"Leave Home"~~ — done: [scene](./1-configuration/scene/readme-leave-home.md), [automation](./1-configuration/automation/leave-home-automation.yaml), [dashboard](./2-dashboards/global-dashboard/global-dashboard.yaml)
  - ~~"Cinema On" / "Cinema Off"~~ — done: [script](./1-configuration/scripts/cinema/cinema-script.yaml), [automation](./1-configuration/automations/cinema-automation.yaml), [dashboard](./2-dashboards/global-dashboard/global-dashboard.yaml)
    - ~~AVR control via HEOS/Denon AVR integration~~ — done: [script](./1-configuration/scripts/heos-avr/heos-avr-scripts.yaml), [dashboard](./2-dashboards/hifi-dashboard/hifi-dashboard.yaml) (replaces IR control)
- **Physical buttons**: rework button assignments (subtypes) for new routines
  - ~~Dimmer switch entrance (global)~~ — done: [play-random-music](./1-configuration/automations/play-random-music-automation.yaml), [stop-music](./1-configuration/automations/stop-music-automation.yaml), [leave-home](./1-configuration/automations/leave-home-automation.yaml) (also added a 2-second delay after plug turn-on for PR300 power-up in [play-random-music-script.yaml](./1-configuration/scripts/play-random-music/play-random-music-script.yaml))
  - TODO: assign remaining buttons
  -  (consider IKEA Zigbee or Matter buttons — see [IKEA devices](0-gateways-selection-and-configuration/slzb/slzb-matter.md#ikea-devices)) - Will not
- ~~**Sync**~~: done — [sync-to-ha.sh](./sync-to-ha.sh) copies repo to HA (see [sync-to-ha-README.md](./sync-to-ha-README.md))

- **AC / climate control** integration (via Tahoma or Onecta)  (see [1-configuration/README.md](./1-configuration/README.md#ha-ui))

- Improve dashboards 

- All comments in [configuration.yaml](./1-configuration/configuration.yaml) are reviewed and up to date (includes pyscript)

<!--
Legacy conclusion:
- SLZB IR module: TODO FIX ONLY + optional AC => CCL: https://github.com/scoulomb/home-assistant/commit/52642e2fe2273d89791927f60d153c4ba326b888#commitcomment-162492611 
 - All ccl except new devices and mrw10 optional
 -->

<!--
move from http to ssh 

git remote rm origin 
git remote add origin git@github.com:scoulomb/home-assistant.git
git push --set-upstream origin main

[See also](../../../ACS-sre-manager/learn/git/README.md#note--why-gitgithubcom-may-still-work-by-accident) and 
[and commit identity is gmail](../../../ACS-sre-manager/learn/git/README.md#5-set-git-identity-per-repo)


same with repo home-assistant-routines-and-dashboard

-->
