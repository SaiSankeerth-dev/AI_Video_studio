# Contributing to AI Video Studio

Thank you for your interest in contributing to the **AI Video Studio** platform. This document outlines our architectural standards, code quality expectations, test requirements, and Git contribution workflow.

---

## Architectural Principles

1. **Multi-Track Separation:**
   * Short-form vertical production belongs under `Instagram/`.
   * YouTube documentary workflows belong under `Youtube/` or `projects/`.
   * Modular director agents belong under `agents/` and engine abstractions under `engines/`.
2. **Schema-First Design:**
   * Every production artifact (narrative arcs, claims, audio plans, shot plans, timeline IR) must validate against a formal schema in `schemas/`.
   * Never bypass schema validation or emit arbitrary untyped payloads.
3. **Zero Hardcoded Environment Secrets:**
   * Never commit API keys, personal emails, machine user paths, or session tokens.
   * All path resolution must be dynamic (`Path(__file__).resolve()` in Python, `import.meta.url` in Node.js ES modules).
4. **Git Binary Cleanliness:**
   * Intermediate render caches (`downloads/`, `.hyperframes/`, `.remotion/`, raw uncompressed audio beds) must remain gitignored.
   * Only lightweight, web-optimized demonstration media under `docs/assets/` (<15 MB) may be tracked.

---

## Development Setup

### Python Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt  # Or install faster-whisper, scenedetect, pillow, scipy
```

### Node.js Environment
```bash
# In short-form projects (HyperFrames / Remotion)
cd Instagram/projects/04-openshorts-gta6
npm install
```

---

## Running the Test Suites

Before opening a pull request or pushing commits, ensure all test suites pass without regression:

```bash
# 1. Modular V2 Architecture Test (Tasks 01 to 23)
python tests/test_v2_documentary_architecture.py

# 2. 19-Section Production Logic Blueprint Test
python tests/test_production_logic_spec.py

# 3. Video-003 Data Contract Integrity Audit
python tests/test_video_003_astra.py
```

---

## Contribution Workflow

1. Fork the repository and create a feature branch:
   ```bash
   git checkout -b feat/your-feature-name
   ```
2. Make your changes adhering to the coding standards.
3. Run the complete test suite.
4. Commit using Conventional Commits:
   ```bash
   git commit -m "feat(agents): add multi-modal scene critic director"
   ```
5. Open a Pull Request detailing your changes and test evidence.
