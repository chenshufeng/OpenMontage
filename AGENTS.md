# OpenMontage — Agent Instructions

## First read

**`AGENT_GUIDE.md`** — routing rules, pipeline system, decision contract, reviewer protocol, tool registry usage. Must read before acting. Skipping it causes wrong actions.

**`PROJECT_CONTEXT.md`** — architecture, key files, file map, pipeline list.

Both are pointed to by `CLAUDE.md`, `CURSOR.md`, `COPILOT.md`, `CODEX.md`, `.windsurfrules`, and `.github/copilot-instructions.md`.

## Quick reference

### Setup

- **Prerequisites:** Python ≥3.10, Node.js ≥18 (≥22 for HyperFrames), FFmpeg
- **`make setup`** — create venv, pip install, npm install in `remotion-composer/`, Piper TTS, copy `.env.example`.
- **Without `make` (Windows):** `py -3 -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt; cd remotion-composer; npm install; cd ..; python -m pip install piper-tts; Copy-Item .env.example .env`
- If `npm install` fails with `ERR_INVALID_ARG_TYPE`, use `npx --yes npm install` instead.

### Key commands

| Command | What it does |
|---------|-------------|
| `make test` | Run all tests (`pytest tests/ -v`) |
| `make test-contracts` | Run contract tests only |
| `make lint` | Smoke-check key Python files via `py_compile` |
| `make preflight` | Discover tools via `registry.provider_menu()` |
| `make demo` | Render zero-key demo videos |
| `make install-gpu` | Install local GPU video gen (diffusers + WAN/Hunyuan/etc) |
| `make hyperframes-doctor` | Validate HyperFrames runtime |
| `make hyperframes-warm` | Refresh npx cache to latest HyperFrames version |
| `python -m backlot open <project-id>` | Open Backlot board for a project |

### Architecture (3 layers)

1. **`tools/`** — Python `BaseTool` subclasses. Capabilities, not orchestration.
2. **`skills/`** — Markdown pipeline director skills + creative/meta skills. How OpenMontage wants tools used.
3. **`.agents/skills/`** — Vendor/technology knowledge packs. Read these before calling any generation tool.

**The agent is the orchestrator.** Python has no pipeline state machine, no reviewer, no production logic. The agent reads pipeline manifests → reads stage director skills → calls tools → self-reviews → checkpoints → presents for human approval.

### Pipeline system (mandatory)

Every video production goes through a pipeline. **Never write ad-hoc scripts.**

1. Pick a pipeline from `pipeline_defs/<name>.yaml`
2. Read its YAML manifest (stages, tools, approval gates)
3. For each stage, read `skills/pipelines/<pipeline>/<stage>-director.md`
4. Use tools per the manifest's `tools_available` field

Pipeline state machine (varies by pipeline): `research → proposal → script → scene_plan → assets → edit → compose → publish`

### Tool conventions

- **Naming:** PascalCase, no `Tool` suffix (e.g. `VideoCompose`, `ElevenLabsTTS`, `AudioMixer`)
- **Invocation:** `tool.execute(params_dict)` returns `ToolResult` (`.success`, `.data`, `.error`)
- **Discovery:** always via `tools/tool_registry.py` — never hardcode tool lists
  ```
  python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.capability_catalog(), indent=2))"
  ```
- **Selector pattern** for multi-provider capabilities: `tts_selector` / `image_selector` / `video_selector`
- **All tools** declare: capability, provider, agent_skills[], install_instructions, runtime, status

### Output contract

All generated assets go to `projects/<project-id>/`:
```
projects/<project-id>/
  artifacts/     # JSON artifacts from each stage
  assets/        # images/ video/ audio/ music/ subtitles.srt
  renders/       # final.mp4
```

Never write outputs to the repo root, cwd, or temp dirs.

### Critical rules

- **Read Layer 3 skills** (`.agents/skills/`) before calling any generation tool. The tool's `agent_skills[]` field names them.
- **No hardcoded provider names, API key names, or setup URLs.** Read from registry `install_instructions` and `dependencies` fields.
- **No silent runtime swaps.** Present both Remotion and HyperFrames at proposal when both are available.
- **Decision log is append-only.** Never mutate existing entries; append new ones with same `(category, subject)` pair.
- **Escalate blockers** — do not continue with substitute paths without user approval.
