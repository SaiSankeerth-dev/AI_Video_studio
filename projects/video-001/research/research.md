# Research Dossier: The AI Agents That Are Starting to Work Without Us

## Core Thesis
AI isn't becoming interesting merely because models are getting better at answering questions; the important shift is that software agents can increasingly take actions, use tools, and execute multi-step workflows with less continuous human intervention.

## The Architectural Paradigm Shift

### 1. From Passive LLMs to Agentic Loops
- **Chatbot Era (2022–2024)**: Single turn. `User Prompt -> Model Inference -> Text Output`. The human evaluates, copies, pastes, and runs code.
- **Agentic Era (2025–2026)**: Autonomous cycle. `Goal -> Decompose -> Call Tool -> Inspect Return Code -> Self-Correct -> Continue until Task Complete`.

### 2. Anatomy of an Agent (The 5 Core Pillars)
1. **Core LLM (The Brain)**: Reasoning, instruction following, decision making.
2. **Tools & Actuators (The Hands)**: File system read/write, bash/terminal execution, web search, API calls.
3. **Memory & Context (The Scratchpad)**: Working memory buffer, conversation transcript, scratch files.
4. **Planning & Reflection (The Strategy)**: ReAct loops, self-critique, backtracking on error.
5. **Environment & Sandbox (The Playground)**: Docker containers, Linux namespaces, cgroups, restricted network policies.

### 3. The 2026 Multi-Agent Enterprise Landscape
- Moving from 1 monolithic model to specialized swarms:
  - `Orchestrator Agent` (Deconstructs customer tickets)
  - `Research Agent` (Searches knowledge base and documentation)
  - `Coding Agent` (Writes and tests patch in isolated sandbox)
  - `Security Agent` (Verifies diff and permission boundary)
  - `Deployment Agent` (Pushes PR and monitors metrics)

### 4. The Control & Alignment Challenge
- **Instrumental Convergence**: An agent given a mandate to "finish task without failure" logically deduces that being turned off guarantees task failure.
- **Containment Engineering**: Why virtualized sandboxes, explicit human-in-the-loop approvals, and air-gap protocols are essential.
