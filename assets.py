"""Asset sourcing layer -- one interface, three modes.

This is the seam the whole "where do clips come from" question lives behind, so
the rest of the pipeline never hard-codes a source.

  1. User Assets Mode
     You provide clips, voiceovers, scripts, images, and audio.

  2. Autonomous Asset Collection Mode
     The agent researches the topic and gathers legally usable assets
     automatically: stock footage from a licensed API (Pexels), and -- with no
     API key, fully offline -- generated B-roll cards. Both are copyright-safe.

  3. Hybrid Mode (preferred)
     You provide some assets; the agent fills the missing shots automatically.

All three implement the same `AssetSource` contract, so callers never change.

Config (env):
  ASSET_MODE   = user | auto | hybrid     (default: user)
  ASSETS_DIR   = folder of your assets     (user / hybrid)
  PEXELS_API_KEY = stock API key           (auto / hybrid; optional)
  ASSET_CACHE  = download/B-roll cache dir  (default: ./auto_assets)
"""

from __future__ import annotations

import glob
import json
import os
import shutil
import subprocess
import urllib.parse
import urllib.request
from dataclasses import dataclass

VIDEO_EXTS = (".mp4", ".mov", ".mkv", ".webm", ".m4v", ".avi")
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".bmp")
AUDIO_EXTS = (".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg")

VERTICAL = (1080, 1920)


@dataclass
class Asset:
    path: str
    kind: str  # "video" | "image" | "audio"


def _ffmpeg() -> str | None:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    # known winget install location on this machine
    cand = os.path.expandvars(
        r"%LOCALAPPDATA%\Microsoft\WinGet\Packages"
        r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
        r"\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
    )
    return cand if os.path.exists(cand) else None


# ---------------------------------------------------------------------------
# Contract
# ---------------------------------------------------------------------------
class AssetSource:
    mode = "base"

    def visuals(self) -> list[Asset]:
        raise NotImplementedError

    def audios(self) -> list[Asset]:
        raise NotImplementedError

    def match(self, shot_description: str, index: int, strict: bool = False) -> Asset | None:
        """Pick a visual for one shot. None = no asset (caller uses fallback).

        strict=True returns a match ONLY on a real keyword hit (used by Hybrid
        to decide which shots are genuine gaps to fill).
        """
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Mode 1: User Assets
# ---------------------------------------------------------------------------
class UserAssetSource(AssetSource):
    """Everything comes from a user-provided folder (scanned recursively)."""

    mode = "user"

    def __init__(self, root: str) -> None:
        self.root = os.path.abspath(root)
        if not os.path.isdir(self.root):
            raise FileNotFoundError(f"assets folder not found: {self.root}")
        self._visuals = self._scan(VIDEO_EXTS, "video") + self._scan(IMAGE_EXTS, "image")
        self._audios = self._scan(AUDIO_EXTS, "audio")

    def _scan(self, exts: tuple[str, ...], kind: str) -> list[Asset]:
        found: list[str] = []
        for ext in exts:
            found += glob.glob(os.path.join(self.root, "**", "*" + ext), recursive=True)
        return [Asset(os.path.abspath(p), kind) for p in sorted(set(found))]

    def visuals(self) -> list[Asset]:
        return self._visuals

    def audios(self) -> list[Asset]:
        return self._audios

    def match(self, shot_description: str, index: int, strict: bool = False) -> Asset | None:
        vids = self._visuals
        if not vids:
            return None
        keywords = [w for w in shot_description.lower().split() if len(w) > 3]
        for a in vids:
            name = os.path.basename(a.path).lower()
            if any(k in name for k in keywords):
                return a
        if strict:
            return None  # no real match -> let Hybrid fill the gap
        return vids[index % len(vids)]  # round-robin so every shot gets a clip


# ---------------------------------------------------------------------------
# Mode 2: Autonomous Asset Collection
# ---------------------------------------------------------------------------
class AutoAssetSource(AssetSource):
    """Fetch legally usable assets automatically.

    Order per shot:
      1. Pexels stock video (license: free to use) if PEXELS_API_KEY is set.
      2. Generated B-roll card via ffmpeg (no copyright, works offline).

    Both are safe to publish; nothing unclearable can reach the timeline.
    """

    mode = "auto"

    def __init__(self, topic: str = "", cache_dir: str = "auto_assets") -> None:
        self.topic = topic
        self.cache = os.path.abspath(cache_dir)
        os.makedirs(self.cache, exist_ok=True)
        self.api_key = os.environ.get("PEXELS_API_KEY", "").strip()
        self._collected: list[Asset] = []

    # -- stock ---------------------------------------------------------------
    def _stock(self, query: str, index: int) -> Asset | None:
        if not self.api_key:
            return None
        try:
            url = ("https://api.pexels.com/videos/search?"
                   + urllib.parse.urlencode({"query": query, "per_page": 1,
                                             "orientation": "portrait"}))
            req = urllib.request.Request(url, headers={"Authorization": self.api_key})
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode())
            videos = data.get("videos") or []
            if not videos:
                return None
            files = sorted(videos[0].get("video_files", []),
                           key=lambda f: f.get("height", 0), reverse=True)
            if not files:
                return None
            link = files[0]["link"]
            dst = os.path.join(self.cache, f"stock_{index:02d}.mp4")
            urllib.request.urlretrieve(link, dst)
            return Asset(dst, "video")
        except Exception:
            return None

    # -- generated B-roll ----------------------------------------------------
    def _broll(self, text: str, index: int) -> Asset | None:
        ff = _ffmpeg()
        dst = os.path.join(self.cache, f"broll_{index:02d}.mp4")
        if os.path.exists(dst):
            return Asset(dst, "video")
        if not ff:
            return None
        w, h = VERTICAL
        hue = (index * 47) % 360
        label = (text[:40].replace(":", "").replace("'", "")
                 .replace("\\", "").replace("%", "")) or "scene"
        try:
            subprocess.run(
                [ff, "-y",
                 "-f", "lavfi", "-i",
                 f"color=c=gray:s={w}x{h}:d=4,hue=h={hue}",
                 "-vf", (f"drawtext=text='{label}':fontcolor=white:fontsize=54:"
                         f"x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor=black@0.4:boxborderw=24"),
                 "-r", "30", "-pix_fmt", "yuv420p", dst],
                capture_output=True, timeout=60, check=True,
            )
            return Asset(dst, "video")
        except Exception:
            return None

    def match(self, shot_description: str, index: int, strict: bool = False) -> Asset | None:
        query = shot_description or self.topic
        asset = self._stock(query, index) or self._broll(shot_description, index)
        if asset and asset not in self._collected:
            self._collected.append(asset)
        return asset

    def visuals(self) -> list[Asset]:
        return self._collected

    def audios(self) -> list[Asset]:
        return []


# ---------------------------------------------------------------------------
# Mode 3: Hybrid (preferred)
# ---------------------------------------------------------------------------
class HybridAssetSource(AssetSource):
    """User assets first; agent fills the gaps automatically."""

    mode = "hybrid"

    def __init__(self, root: str | None, topic: str = "",
                 cache_dir: str = "auto_assets") -> None:
        self.user = UserAssetSource(root) if root and os.path.isdir(root) else None
        self.auto = AutoAssetSource(topic, cache_dir)

    def match(self, shot_description: str, index: int, strict: bool = False) -> Asset | None:
        if self.user:
            hit = self.user.match(shot_description, index, strict=True)
            if hit:
                return hit
        return self.auto.match(shot_description, index)  # fill the gap

    def visuals(self) -> list[Asset]:
        u = self.user.visuals() if self.user else []
        return u + self.auto.visuals()

    def audios(self) -> list[Asset]:
        return self.user.audios() if self.user else []


# ---------------------------------------------------------------------------
def get_asset_source(mode: str | None, root: str | None = None,
                     topic: str = "", cache_dir: str = "auto_assets") -> AssetSource:
    mode = (mode or "user").lower()
    if mode == "user":
        return UserAssetSource(root or "assets")
    if mode == "auto":
        return AutoAssetSource(topic, cache_dir)
    if mode == "hybrid":
        return HybridAssetSource(root, topic, cache_dir)
    raise ValueError(f"unknown asset mode: {mode!r} (use user|auto|hybrid)")
