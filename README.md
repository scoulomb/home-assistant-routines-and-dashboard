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
  - "Play random music"  (leverage completed pyscript)
  - "Stop all music"
  - "Cut music plug"
  - "Leave Home"

- **AC / climate control** integration (via Tahoma or Onecta)  (see [1-configuration/README.md](./1-configuration/README.md#ha-ui))



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
