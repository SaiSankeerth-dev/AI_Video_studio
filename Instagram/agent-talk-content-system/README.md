# Agent Talk — Viral Content SEO & Reel Optimization System

A permanent, automated content strategy, SEO, and multi-platform publishing engine for the **Agent Talk** (`@agent.talk`) media brand.

---

## 1. System Overview & Mission

The **Agent Talk Content System** bridges technical AI video production with high-signal social distribution across Instagram Reels, YouTube Shorts, and TikTok. 

Rather than relying on generic AI news summaries or breathless hype, this system analyzes actual rendered video files, measures cinematography pacing, performs semantic keyword research, and generates platform-native publishing packages designed to optimize:
- **Non-Follower Search Discovery:** Ranking on Instagram Explore, Reels Search, and YouTube Search.
- **Saves & Bookmarks:** High-utility developer takeaways (open-source tool names, security architectures).
- **Shares & Sends:** Relatable developer humor and production incident comedy.
- **Brand Consistency:** Original recurring characters (**Tariq Vance** and **Claude** the terracotta AI mascot).

---

## 2. Directory Structure

```
agent-talk-content-system/
├── README.md                          # Master documentation & operating manual
├── .agents/
│   ├── skills/                        # 23 installed Agent Skills (Social Media + SEO)
│   └── brand/                         # Brand identity, voice guide, audience, keywords, pillars
│       ├── brand-profile.md
│       ├── voice-guide.md
│       ├── audience-profile.md
│       ├── keyword-dictionary.md
│       └── content-pillars.md
├── analysis/
│   ├── video-analysis/                # PySceneDetect + ffprobe analysis reports & keyframes
│   ├── keyword-research/              # Semantic keyword maps & search intent clusters
│   ├── competitor-research/           # Viral reverse-engineering & creator benchmarking
│   └── trend-research/                # Emerging dev trends & AI agent topics
├── publishing/
│   ├── instagram/                     # Reels posting packages (Captions, Hooks, Hashtags, Alt text)
│   ├── youtube/                       # YouTube Shorts metadata (Titles, Descriptions, Tags)
│   └── tiktok/                        # TikTok captions, sound recommendations, search terms
├── analytics/
│   ├── performance-reports/           # Post-launch analytics logging & retention curve audits
│   └── experiments/                   # A/B testing protocols (Search vs Engagement captions)
├── templates/
│   ├── caption-template.md            # Standard multi-platform caption format
│   ├── video-analysis-template.md     # Standard technical inspection framework
│   └── posting-checklist.md           # Pre-flight checklist before scheduling/publishing
└── scripts/
    └── analyze_video.py               # Automated video inspection CLI tool
```

---

## 3. Installed Agent Skills (.agents/skills/)

The system integrates 23 specialized agent skills:

### Foundation & Strategy
- `brand-profile`: Maintains `@agent.talk` brand integrity, positioning, and rules.
- `voice-builder`: Enforces conversational, witty, and developer-authentic tone.
- `audience-research`: Tracks developer pain points, psychographics, and demographics.
- `social-strategy`: High-level multi-platform distribution and content rhythm.

### Research & Sourcing
- `content-research-and-sourcing`: Validates tools, GitHub repositories, and factual claims.
- `competitor-analysis`: Benchmarks top developer and tech storytelling accounts.
- `viral-reverse-engineering`: Deconstructs high-retention short-form hooks and pacing.
- `trend-jacking`: Connects real news/releases (e.g. T3 Code, Claude Code) to Agent Talk storytelling.

### Copywriting & SEO
- `hook-writer`: Crafts 5 high-contrast hooks per video (agony, curiosity, contradiction).
- `caption-writer`: Generates 3 platform-native caption variants (Search, Engagement, Story).
- `instagram-seo`: Optimizes on-screen text, caption keywords, and accessibility alt text.
- `social-seo`: Cross-platform search indexing across TikTok, YouTube, and Google.
- `hashtag-strategy`: Curates high-relevance niche hashtags (5–12 limit; no spam tags).

### SEO Clustering & Google Search (Adapted from claude-seo)
- `seo-cluster`: Semantic keyword clustering and topic authority mapping.
- `seo-content`: Search intent matching and editorial quality evaluation.
- `seo-google`: Google and YouTube search indexing best practices.
- `seo-sxo`: Search Experience Optimization (bridging search intent with immediate retention).

### Video Production & Analytics
- `reels-script`: Formats 9:16 vertical dialogue and camera cues.
- `short-form-video-script`: Pacing, curiosity gap management, and retention loop engineering.
- `instagram-growth`: Organic profile conversion and follower growth tactics.
- `analytics-and-reporting`: Post-publication metric logging and retention diagnostics.
- `experimentation-and-ab-testing`: Systematic A/B tests for hooks, covers, and captions.
- `platform-specs-and-validation`: Checks aspect ratios, bitrates, safe zones, and audio loudness.

---

## 4. Local Tooling Stack

| Tool | Status | Purpose |
|---|:---:|---|
| **FFmpeg & FFprobe** | Installed (`9.0-full`) | Video/audio stream metadata, format validation, frame grabbing |
| **PySceneDetect** | Installed (`0.7.3`) | Scene boundary detection, cuts per minute (CPM), shot duration |
| **faster-whisper** | Installed (`1.2.1`) | Local audio transcription, spoken keyword timestamping |
| **yt-dlp** | Installed (`2026.07.04`) | Reference video downloading and competitive analysis |

---

## 5. Workflow for New Videos

When a new video is rendered (e.g. `exports/video_name.mp4`):

1. **Run Video Inspection CLI:**
   ```bash
   python scripts/analyze_video.py --video "path/to/video.mp4" --slug "video-name" --srt "path/to/subtitles.srt"
   ```
2. **Review Generated Analysis:**
   Inspect `analysis/video-analysis/video-name.md` for shot pacing, keyframe snapshots, and spoken keywords.
3. **Run Keyword Strategy:**
   Generate `analysis/keyword-research/video-name-keywords.md` based on primary audience intent.
4. **Generate Publishing Packages:**
   Populate `publishing/instagram/video-name-posting-package.md`, `publishing/youtube/`, and `publishing/tiktok/`.
5. **Run Pre-Flight Checklist:**
   Review `templates/posting-checklist.md` before scheduling or uploading.
