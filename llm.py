"""LLM interface.

Two implementations behind one method, `complete(system, user)`:

  - MockLLM   : returns structured, valid fake data so the whole pipeline runs
                with no API key and no cost. Use it to build and test the graph.
  - OpenAILLM : the real model. Swap it in once the flow is proven, one agent
                at a time if you like.

Each agent's system prompt starts with a stable `ROLE: <name>` line. The mock
switches on that line; the real model just reads the whole prompt. Same code
path either way, so there is no "mock branch" scattered through the agents.
"""

from __future__ import annotations

import json
import os


class LLM:
    def complete(self, system: str, user: str, json_mode: bool = False) -> str:
        raise NotImplementedError


class OpenAILLM(LLM):
    """Real OpenAI client. Requires `pip install openai` and OPENAI_API_KEY."""

    def __init__(self, model: str = "gpt-4o-mini") -> None:
        from openai import OpenAI  # imported lazily so mock mode needs no install

        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.model = model

    def complete(self, system: str, user: str, json_mode: bool = False) -> str:
        kwargs: dict = {}
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.7,
            **kwargs,
        )
        return resp.choices[0].message.content


class GeminiLLM(LLM):
    """Real Google Gemini client. Requires `pip install google-genai` and GEMINI_API_KEY.

    Same `complete(system, user, json_mode)` contract as OpenAILLM, so it drops
    straight into the pipeline. The agent's `system` prompt is passed as Gemini's
    system_instruction; `json_mode` maps to response_mime_type=application/json.
    """

    def __init__(self, model: str = "gemini-2.0-flash") -> None:
        from google import genai  # imported lazily so mock mode needs no install
        from google.genai import types

        self.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        self.model = model
        self._types = types

    def complete(self, system: str, user: str, json_mode: bool = False) -> str:
        config = self._types.GenerateContentConfig(
            system_instruction=system,
            temperature=0.7,
            response_mime_type="application/json" if json_mode else "text/plain",
        )
        resp = self.client.models.generate_content(
            model=self.model,
            contents=user,
            config=config,
        )
        return resp.text


class OllamaLLM(LLM):
    """Local Ollama client. Requires `pip install ollama` and a running Ollama
    server with the model pulled (`ollama pull qwen3:8b`).

    Fully offline and key-free, like MockLLM, but with a real model. Same
    `complete(system, user, json_mode)` contract. `json_mode` uses Ollama's
    grammar-constrained `format="json"`, which also suppresses qwen3 thinking
    tokens so the output parses cleanly.
    """

    def __init__(self, model: str = "qwen3:8b", host: str | None = None) -> None:
        from ollama import Client  # imported lazily so mock mode needs no install

        self.client = Client(host=host) if host else Client()
        self.model = model

    def complete(self, system: str, user: str, json_mode: bool = False) -> str:
        resp = self.client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            format="json" if json_mode else "",
            think=False,
            options={"temperature": 0.7},
        )
        return resp["message"]["content"]


# --- canned responses for offline mode, keyed by the ROLE tag --------------
# These use the "Messi 2022 World Cup" example so the output is recognizable.
# Note one deliberately false fact in research (a "hat-trick") that the Fact
# Checker removes -- so you can watch hallucination-filtering actually happen.
_MOCK_RESPONSES: dict[str, str] = {
    "ceo": json.dumps(
        {
            "length_seconds": 30,
            "audience": "Football fans",
            "goal": "High retention",
            "emotion": "Excitement",
            "style": "Fast-cut highlight",
        }
    ),
    "research": json.dumps(
        {
            "facts": [
                "Messi won the 2022 World Cup with Argentina",
                "Argentina beat France in the final",
                "The final went to a penalty shootout",
                "Messi scored twice in the final",
                "Messi scored a hat-trick in the final",  # FALSE - he scored twice
                "It was Messi's first World Cup title",
            ]
        }
    ),
    # Fact Checker returns a rule the agent applies to whatever facts exist,
    # rather than a fixed list (which could not match dynamic input).
    "fact_checker": json.dumps(
        {
            "reject_if_contains": ["hat-trick"],
            "reason": "Messi scored twice in the 2022 final, not a hat-trick.",
        }
    ),
    "story_architect": json.dumps(
        {
            "hook": "Nobody thought it would come down to this.",
            "conflict": "Argentina led, France clawed back, and it went to penalties.",
            "payoff": "Messi finally lifts the World Cup - the last piece of his career.",
            "cta": "Follow for more football moments.",
        }
    ),
    "visual_director": json.dumps(
        {
            "shots": [
                {"start": 0, "end": 3, "description": "Crowd erupts in the stadium"},
                {"start": 3, "end": 5, "description": "Messi close-up, locked in"},
                {"start": 5, "end": 9, "description": "Goal replay in slow motion"},
                {"start": 9, "end": 12, "description": "Penalty shootout tension"},
                {"start": 12, "end": 16, "description": "Decisive save, players sprint"},
                {"start": 16, "end": 20, "description": "Messi lifts the trophy"},
                {"start": 20, "end": 24, "description": "Confetti and teammates pile on"},
                {"start": 24, "end": 28, "description": "Messi kisses the trophy"},
                {"start": 28, "end": 30, "description": "Argentina champions title card"},
            ]
        }
    ),
    "music_director": json.dumps(
        {
            "segments": [
                {"start": 0, "end": 5, "mood": "Suspense", "intensity": "low"},
                {"start": 5, "end": 16, "mood": "Build-up", "intensity": "rising"},
                {"start": 16, "end": 26, "mood": "Epic", "intensity": "high"},
                {"start": 26, "end": 30, "mood": "Victory", "intensity": "resolve"},
            ]
        }
    ),
    # Caption timing in production comes from Whisper word-alignment, NOT the
    # model. The "director" only chooses which words to emphasize.
    "caption_director": json.dumps(
        {"emphasis_words": ["MESSI", "WORLD", "CUP", "CHAMPIONS", "PENALTY", "TROPHY"]}
    ),
}


class MockLLM(LLM):
    """Returns canned, structurally-valid responses based on the ROLE tag."""

    def complete(self, system: str, user: str, json_mode: bool = False) -> str:
        role = system.splitlines()[0].replace("ROLE:", "").strip()
        return _MOCK_RESPONSES.get(role, "{}")
