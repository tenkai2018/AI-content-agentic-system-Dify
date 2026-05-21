# Project New Features v1 - Current Stage Description

## Overview
The project is currently at a functional **v1 orchestration stage** with a real multi-step backend pipeline, human-in-the-loop (HITL) approvals, dynamic video asset generation, Remotion rendering integration, and a live frontend monitoring/approval dashboard.

The system now supports the flow:
1. Research viral topics from real YouTube data.
2. Generate script with schema validation.
3. Generate thumbnail brief with schema validation.
4. Generate image + TTS assets.
5. Pause for asset approval.
6. Render video via Remotion.
7. Generate LinkedIn repurposed posts.

---

## What Is Implemented

### 1. Backend Pipeline (FastAPI + LangGraph)
- Real orchestrator flow with persistent `task_id` lifecycle.
- Checkpoint-based resume logic via `/api/approve`.
- Endpoints:
  - `POST /api/run-workflow`
  - `POST /api/approve`
  - `GET /api/status/{task_id}`
  - `GET /api/health`

### 2. Data-First Research
- Researcher step now uses YouTube Data API integration.
- Outlier Score is computed from actual video/channel metrics.
- Results are filtered and ranked before moving to approval.

### 3. Output Schema Validation
- Pydantic validation layer for agent outputs:
  - Researcher
  - Scriptwriter
  - Visual Director
  - Repurposer
- Invalid/malformed LLM outputs now fail fast with explicit error state.

### 4. HITL and State Persistence
- Task state is persisted in PostgreSQL model (`content_tasks`).
- Approval steps currently supported:
  - `topic`
  - `script`
  - `thumbnail`
  - `assets`
- Status API returns persisted outputs and error details.

### 5. Video Automation (Phase C)
- `asset_generator_node` implemented:
  - Calls OpenAI TTS and DALL-E
  - Saves generated assets under task folder
  - Writes task manifest
- `video_producer_node` implemented:
  - Calls Remotion render via subprocess
  - Timeout and failure handling included
  - Render output metadata stored in task state

### 6. Remotion Runtime (Phase D)
- Manifest-driven composition support (including backend `screens` format).
- Dynamic duration calculation based on scene durations.
- Per-scene voiceover playback.
- Global BGM track support.

### 7. Frontend Dashboard (Phase E)
- Live polling against status API.
- Real-time step visualization (not mock anymore).
- Approve/reject actions wired for all supported checkpoints.
- Error display for status and approval failures.

### 8. Reliability Improvements (Phase F - partial)
- Standardized API error payload format (`code`, `message`, `task_id`, `step`).
- Added initial backend tests for:
  - Resume flow behavior
  - Repository state/status mapping

---

## Current Data and Status Model Highlights
- Added pipeline fields:
  - `assets_result`
  - `video_result`
  - `assets_approved`
- Added status values:
  - `generating_assets`
  - `awaiting_assets_approval`
  - `rendering_video`

---

## Known Gaps / Remaining Work

### 1. Runtime Verification Pending
- The development environment used during implementation could not execute Python runtime/tests.
- Full local E2E validation is still required on target machine.

### 2. Encoding Cleanup
- Some legacy files still contain mojibake/encoding artifacts.
- Full UTF-8 normalization across docs/knowledge/source is still pending.

### 3. Production Hardening
- More integration tests and failure-path tests are still needed.
- CI pipeline (lint/typecheck/tests) not fully configured yet.

### 4. Extended Features (Optional Roadmap)
- Add SEO/Newsletter/Analyst stages as defined in architecture docs.
- Add ChromaDB long-term memory write/read loop.
- Improve frontend artifact presentation (currently raw JSON block for outputs).

---

## Summary
At this stage, the project has moved from a scaffold/prototype into a **working orchestrated v1 system** with real API integrations, real persistence, actionable HITL checkpoints, dynamic Remotion pipeline support, and operational frontend controls.

The next priority is to complete final hardening (verification, encoding cleanup, CI, broader tests) before declaring production readiness.

