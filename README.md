# Home Assistant Routines & Dashboard

Content originally in https://github.com/scoulomb/home-assistant/blob/main/2025-new-gen-setup/README.md, moved to this external repo.

## Table of Contents

- **0 — [Gateways Selection & Configuration](./0-gateways-selection-and-configuration/slzb/)**
- **1 — [Configuration](./1-configuration/)**
- **2 — [Dashboards](./2-dashboards/)**

## TODO

- **HiFi Dashboard**: Adjust PR300 volume step (long press causes large jumps)
- **Global scenes in dashboard**:
  - "Leave Home", "Go to Bed"
  - "Start Qobuz Music" (leverage completed pyscript)
  - (see [1-configuration/README.md](./1-configuration/README.md))
- **Physical button trigger**: Hardware button to invoke scripts/automations
- **AC / climate control** integration (via Tahoma or Onecta)



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
