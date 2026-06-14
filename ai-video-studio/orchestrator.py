"""Top-level multi-agent orchestrator -- the part you actually asked for.

This is the "CEO graph": the thing that wires all ten roles into one system
and runs them. It is a tiny, dependency-free graph executor that mirrors
LangGraph's node / edge / conditional-edge model. Because every node is already
a `state -> state` callable, porting to LangGraph later is mechanical:

    # LangGraph equivalent
    g = StateGraph(VideoState)
    g.add_node("ceo", ceo_agent)        # (bind llm via functools.partial)
    g.add_edge("ceo", "research")
    g.add_conditional_edges("qa", qa_router, {"export": "export", "senior_editor": "senior_editor"})
    g.set_entry_point("ceo")
"""

from __future__ import annotations

from functools import partial
from typing import Callable

import agents
from llm import LLM
from state import VideoState

Node = Callable[[VideoState], VideoState]
END = "__end__"


class Graph:
    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
        self.edges: dict[str, str] = {}
        self.conditional: dict[str, Callable[[VideoState], str]] = {}
        self.entry: str | None = None

    def add_node(self, name: str, fn: Node) -> "Graph":
        self.nodes[name] = fn
        return self

    def add_edge(self, src: str, dst: str) -> "Graph":
        self.edges[src] = dst
        return self

    def add_conditional_edge(self, src: str, router: Callable[[VideoState], str]) -> "Graph":
        self.conditional[src] = router
        return self

    def set_entry(self, name: str) -> "Graph":
        self.entry = name
        return self

    def run(self, state: VideoState, max_steps: int = 100) -> VideoState:
        current = self.entry
        for _ in range(max_steps):
            if not current or current == END:
                return state
            state = self.nodes[current](state)
            if current in self.conditional:
                current = self.conditional[current](state)
            else:
                current = self.edges.get(current, END)
        state.errors.append("Orchestrator hit max_steps -- possible loop.")
        return state


def qa_router(state: VideoState) -> str:
    """Conditional edge: pass -> export, fail -> re-edit (capped), then export anyway."""
    if state.qa_passed:
        return "export"
    if state.qa_attempts >= 2:
        state.note("Orchestrator", "QA still failing after retries; exporting best-effort.")
        return "export"
    state.note("Orchestrator", "QA failed; looping back to Senior Editor.")
    return "senior_editor"


def build_studio(llm: LLM) -> Graph:
    """Wire the full pipeline. `llm` is bound into each reasoning node."""
    n = lambda fn: partial(fn, llm=llm)  # bind the model into every node

    g = Graph()
    (
        g.add_node("ceo", n(agents.ceo_agent))
        .add_node("research", n(agents.research_agent))
        .add_node("fact_checker", n(agents.fact_checker_agent))
        .add_node("story_architect", n(agents.story_architect_agent))
        .add_node("visual_director", n(agents.visual_director_agent))
        .add_node("asset_manager", n(agents.asset_manager_agent))
        .add_node("music_director", n(agents.music_director_agent))
        .add_node("caption_director", n(agents.caption_director_agent))
        .add_node("senior_editor", n(agents.senior_editor_agent))
        .add_node("qa", n(agents.qa_agent))
        .add_node("export", n(agents.export_agent))
    )

    g.set_entry("ceo")
    g.add_edge("ceo", "research")
    g.add_edge("research", "fact_checker")
    g.add_edge("fact_checker", "story_architect")
    g.add_edge("story_architect", "visual_director")
    g.add_edge("visual_director", "asset_manager")
    g.add_edge("asset_manager", "music_director")
    g.add_edge("music_director", "caption_director")
    g.add_edge("caption_director", "senior_editor")
    g.add_edge("senior_editor", "qa")
    g.add_conditional_edge("qa", qa_router)   # the only branch: the QA feedback loop
    g.add_edge("export", END)
    return g
