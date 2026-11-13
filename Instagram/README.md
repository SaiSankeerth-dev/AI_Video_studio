# E:\AI_Videos\Instagram Workspace

Central organized home for all Instagram AI video production work, reference downloads, assets, final exports, automation scripts, documentation, and logs.

> **Directory Rule:** All files, downloads, projects, renders, assets, and reports created in this conversation and all future sessions are strictly stored inside `E:\AI_Videos\Instagram`.

## Folder Layout

```text
E:\AI_Videos\Instagram\
├── downloads\
│   ├── instagram\     # Downloaded Instagram reels & posts
│   ├── youtube\       # Downloaded YouTube reference videos
│   └── other\         # Other downloaded media
├── projects\          # Active video production projects
│   ├── 01-one-small-fix\          # Project 1: Indie Dev vs Rogue AI
│   └── 02-four-hundred-messages\  # Project 2: "I Tried Codex" Confession & Mascot Bond
├── assets\
│   ├── audio\         # Voiceovers, music, SFX
│   └── images\        # Stills, thumbnails, character art
├── exports\           # Final master rendered videos (e.g. 01_one_small_fix_final.mp4)
├── scripts\
│   ├── download-video.ps1     # Download any video URL into downloads\<platform>\ via Ubuntu yt-dlp
│   └── workspace-status.ps1   # Check Node/Python/yt-dlp/OpenCLI/Agent Reach health in Ubuntu WSL2
├── docs\
│   └── setup-architecture.md  # Full system architecture, repairs, and update instructions
└── logs\
    ├── work-log.md            # Chronological log of completed setup, downloads, and tasks
    └── backups\               # Snapshot copies of configurations
```

## Quick Commands (PowerShell from `E:\AI_Videos\Instagram`)

```powershell
# Download an Instagram Reel cleanly into E:\AI_Videos\Instagram\downloads\instagram\
.\scripts\download-video.ps1 "https://www.instagram.com/reels/DeL--GHALuW/"

# Check WSL2 tools, daemon, browser bridge, and channel status
.\scripts\workspace-status.ps1
```
