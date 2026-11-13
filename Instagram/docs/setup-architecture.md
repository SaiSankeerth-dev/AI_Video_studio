# Workspace & Environment Architecture

All active projects, downloaded media, renders, helper scripts, logs, and config snapshots live under `E:\AI_Videos`.
Runtime binaries and browser profiles remain in their required OS paths so Windows security policies and Linux tools continue to function cleanly.

## Architecture Overview

```text
Windows 11 (Smart App Control, Code Integrity, McAfee active; host setups preserved)
  ├── E:\AI_Videos\                  <-- Primary organized workspace for all work
  ├── %USERPROFILE%\video-tools\     <-- Windows Python venv
  ├── %USERPROFILE%\lemo-opuscar\    <-- Cloned lemo-opuscar repository
  └── WSL2 (Ubuntu 26.04 LTS / Linux 6.6.114.1-microsoft-standard-WSL2)
        ├── Node.js v22.23.5 (/usr/bin/node), npm 10.9.9 (/usr/bin/npm)
        ├── Python 3.14.4 (/usr/bin/python3), uv 0.13.7 (~/.local/bin/uv)
        ├── OpenCLI 2.0.3 (/usr/bin/opencli -> /usr/lib/node_modules/@jackwener/opencli)
        │     ├── Daemon: port 19825
        │     └── User overrides: ~/.opencli/clis/instagram/ (backed up under logs/backups/opencli-instagram/)
        ├── Agent Reach 1.6.1 (~/.local/bin/agent-reach)
        │     ├── Skill: ~/.agents/skills/agent-reach/SKILL.md
        │     ├── Private tools: cloakbrowser 0.6.3 (+ playwright 1.58.0), ffmpeg 0.8.1, bili-cli 0.6.2
        │     ├── Browser binary: ~/.agent-reach/cloak-binaries/chromium-146.0.7680.177.5/chrome
        │     ├── Persistent profile: ~/.agent-reach/browser/profile (OpenCLI context 7v6wdpkp)
        │     └── Unpacked extension: ~/.agent-reach/browser/extension (v1.0.27)
        └── yt-dlp 2026.10.26 (~/.local/bin/yt-dlp) + ffmpeg symlink (~/.local/bin/ffmpeg)
```

## Key Repairs Applied in Ubuntu WSL2

1. **Chromium Runtime Libraries (`libnspr4`, `libnss3`, `libasound2t64`, `fonts-liberation`)**: Installed in Ubuntu 26.04 so CloakBrowser (`chromium-146.0.7680.177.5`) launches natively in both headless mode and WSLg GUI mode (`agent-reach login instagram`).
2. **CloakBrowser / Playwright Compatibility**: Pinned `playwright==1.58.0` inside `~/.agent-reach/tools/cloakbrowser/venv/` so `cloakbrowser 0.6.3` can import `playwright._impl._js_handle`.
3. **Instagram Adapter Overrides (`~/.opencli/clis/instagram/`)**:
   - `search.js` (upstream PR `#2790`): `/api/v1/fbsearch/account_serp/`
   - `profile.js` + `_shared/profile-web-client.js` (upstream PR `#2799`): in-page XHR/fetch observer for `PolarisProfilePageContentQuery`
   - `user.js` + `_shared/evaluate-result.js` (adapted from upstream PR `#2522`): observes `/graphql/` (`PolarisProfilePostsQuery` -> `/api/graphql`, `xdt_api__v1__feed__user_timeline_graphql_connection`)
   - Note: `opencli instagram whoami` (`auth.js`) still hits Instagram `HTTP 429` on `/api/v1/users/<uid>/info/` upstream; Search, Profile, Posts, Explore, and Saved work independently.
4. **Video Downloading (`yt-dlp` + `ffmpeg`)**: Installed `yt-dlp 2026.10.26` with `ffmpeg` on `$PATH` in Ubuntu WSL2 after `opencli instagram download` hit `fetch failed` on Node media download.

## Service & Update Commands (Ubuntu WSL2)

```bash
# Check status
opencli daemon status
opencli doctor
agent-reach browser status
agent-reach doctor --text

# Start / stop
opencli daemon restart
agent-reach login instagram
agent-reach browser stop
opencli daemon stop

# Future OpenCLI update (reset temporary overrides once upstream merges search/profile/user fixes)
sudo npm install -g @jackwener/opencli@latest
opencli adapter reset instagram
opencli daemon restart

# Future Agent Reach update (re-pin playwright==1.58.0 if cloakbrowser 0.6.3 breaks on newer playwright)
agent-reach update --check
agent-reach update
```
