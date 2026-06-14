"""Shared state passed between every agent in the pipeline.

This single object flows CEO -> Research -> ... -> Export. Each agent reads
the fields it needs and writes the fields it owns. One shared state (instead
of agents calling each other directly) is what makes the system debuggable:
dump the state at any step and you see exactly what every agent produced.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Shot:
    """A single visual on screen for a span of time."""
    start: float
    end: float
    description: str
    asset: str | None = None      # filled by Asset Manager
    motion: str | None = None     # filled by Senior Editor (zoom/pan/...)
    sfx: str | None = None        # filled by Senior Editor

    @property
    def duration(self) -> float:
        return round(self.end - self.start, 2)


@dataclass
class Caption:
    """A word-level caption chunk."""
    start: float
    end: float
    text: str
    emphasis: bool = False


@dataclass
class VideoState:
    # ---- input (exactly one is typically provided) ----
    topic: str = ""
    script: str = ""

    # ---- per-agent outputs ----
    brief: dict[str, Any] = field(default_factory=dict)        # CEO
    facts: list[str] = field(default_factory=list)             # Research
    verified_facts: list[str] = field(default_factory=list)    # Fact Checker
    rejected_facts: list[str] = field(default_factory=list)    # Fact Checker
    story: dict[str, str] = field(default_factory=dict)        # Story Architect
    shots: list[Shot] = field(default_factory=list)            # Visual Director
    assets: dict[str, Any] = field(default_factory=dict)       # Asset Manager
    music_plan: list[dict] = field(default_factory=list)       # Music Director
    captions: list[Caption] = field(default_factory=list)      # Caption Director
    timeline: dict[str, Any] = field(default_factory=dict)     # Senior Editor
    qa_report: dict[str, Any] = field(default_factory=dict)    # QA
    qa_passed: bool = False                                    # QA gate
    exports: dict[str, str] = field(default_factory=dict)      # Export

    # ---- control / meta ----
    target_seconds: int = 30
    qa_attempts: int = 0
    log: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def note(self, agent: str, msg: str) -> None:
        line = f"[{agent}] {msg}"
        self.log.append(line)
        print(line)

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)
