# AI Content Agentic System - Unfinished Functions Task List

## Scope
This checklist tracks all unfinished functions across Backend (FastAPI + LangGraph), Frontend (Next.js), and Video Layer (Remotion), based on current source code state.

## A. Critical Pipeline Completion

### [x] A1. Implement HITL approval resume flow (`/api/approve`)
Description:
- Make approval endpoint actually resume pipeline from stored state.

Acceptance criteria:
- Load task state by `task_id` from DB.
- Update approval flags (`topic_approved`, `script_approved`, `thumbnail_approved`, `assets_approved` when available).
- Resume LangGraph from correct node.
- Persist updated state and status after each resume.
- Return structured response with `current_step`, `status`, and latest artifacts.

Files:
- `backend/app/api/routes.py`
- `backend/app/agents/orchestrator.py`
- `backend/app/db/*` (session/repository layer)

### [x] A2. Implement task status API (`/api/status/{task_id}`)
Description:
- Replace placeholder response with real task progress and artifacts.

Acceptance criteria:
- Query DB by `task_id`.
- Return current status enum, current step, timestamps, and available outputs.
- Return `404` when task does not exist.

Files:
- `backend/app/api/routes.py`
- `backend/app/db/*`

### [x] A3. Add database persistence for pipeline state
Description:
- Persist all task lifecycle data instead of keeping state in-memory only.

Acceptance criteria:
- Create DB engine/session setup.
- Create repository/service functions: create task, update step status, save agent outputs, mark completed/failed.
- Persist error details and stack-safe message on failure.

Files:
- `backend/app/db/models.py` (validate/update schema)
- `backend/app/db/` (new: session.py, repository.py)
- `backend/app/agents/orchestrator.py`

## B. Data-first Research Integration

### [x] B1. Integrate YouTube data source (via n8n or direct API)
Description:
- Replace LLM-only niche suggestion with real video/channel metrics.

Acceptance criteria:
- Fetch at least 20 videos per request.
- Compute Outlier Score from real `video_views` and `channel_average_views`.
- Filter out score < 200.
- Return structured ranked results.
- Handle API errors/rate limits with retries + fallback status.

Files:
- `backend/app/agents/orchestrator.py`
- `backend/app/core/*` (new client/tool wrapper)

### [x] B2. Enforce structured JSON validation for all agent outputs
Description:
- Ensure each node output matches required schema before storing/forwarding.

Acceptance criteria:
- Add Pydantic schemas per step.
- Reject malformed output and mark task `failed` or `needs_regen`.
- Log validation errors with step context.

Files:
- `backend/app/agents/orchestrator.py`
- `backend/app/api/routes.py` (response shaping)
- `backend/app/schemas/` (new)

## C. Video Automation (Spec Compliance)

### [x] C1. Extend `PipelineState` for video flow
Description:
- Add missing state keys for asset generation and rendering.

Acceptance criteria:
- Add `assets_result`, `assets_approved`, `video_result`, `render_status`, `render_error`.
- Add corresponding transitions in LangGraph.

Files:
- `backend/app/agents/orchestrator.py`

### [x] C2. Implement `asset_generator_node`
Description:
- Generate TTS and DALL-E assets from script and save under task folder.

Acceptance criteria:
- Split script into slides/scenes.
- Call `generate_tts_openai()` and `generate_image_dalle()` per slide.
- Save files under `remotion_app/public/assets/generated/{task_id}`.
- Return manifest-ready asset map.

Files:
- `backend/app/agents/orchestrator.py`
- `backend/app/core/api_clients.py`
- `backend/app/utils/file_manager.py`

### [x] C3. Implement assets HITL checkpoint
Description:
- Pause after assets creation and wait for user approval.

Acceptance criteria:
- Status set to `awaiting_assets_approval`.
- `/approve` supports step `assets`.
- Reject path allows regenerate assets or stop pipeline.

Files:
- `backend/app/agents/orchestrator.py`
- `backend/app/api/routes.py`

### [x] C4. Implement `video_producer_node`
Description:
- Build manifest and run Remotion render from backend.

Acceptance criteria:
- Generate `manifest_{task_id}.json` (or equivalent) from approved assets.
- Execute `npx remotion render WalkthroughVideo ... --props=...` with timeout.
- Capture stdout/stderr and surface failure reason.
- Save final output path in `video_result`.

Files:
- `backend/app/agents/orchestrator.py`
- `backend/app/utils/file_manager.py`

## D. Remotion App Functional Completion

### [x] D1. Make composition consume dynamic manifest/props
Description:
- Replace hardcoded `defaultScreens` with external input.

Acceptance criteria:
- `WalkthroughComposition` reads screen list from props/manifest.
- Works when called from backend CLI render.

Files:
- `remotion_app/src/WalkthroughComposition.tsx`
- `remotion_app/src/Composition.tsx`

### [x] D2. Dynamic duration calculation based on audio
Description:
- Remove fixed `durationInFrames` in root composition.

Acceptance criteria:
- `calculateMetadata` or equivalent computes total duration from audio durations.
- Composition duration matches total playback length + transitions.

Files:
- `remotion_app/src/Root.tsx`

### [x] D3. Add per-slide voiceover + global BGM
Description:
- Render TTS audio per slide and background music across full video.

Acceptance criteria:
- `<Audio />` attached to each slide voiceover.
- BGM track runs across full timeline at controlled volume.
- No overlap timing glitches.

Files:
- `remotion_app/src/ScreenSlide.tsx`
- `remotion_app/src/WalkthroughComposition.tsx`
- `remotion_app/public/audio/bgm/`

## E. Frontend Integration Completion

### [x] E1. Replace dashboard mock state with live task polling
Description:
- Show real-time pipeline state.

Acceptance criteria:
- Poll `/api/status/{task_id}` (or SSE/WebSocket).
- Stepper reflects real `current_step` and `status`.
- Result panel renders actual artifacts from each step.

Files:
- `frontend/src/app/dashboard/page.tsx`

### [x] E2. Build approval actions in UI
Description:
- Allow user to approve/reject at each checkpoint.

Acceptance criteria:
- Buttons call `/api/approve` with correct payload.
- Topic selection UI supports `selected_item`.
- UI handles loading/error/success transitions.

Files:
- `frontend/src/app/dashboard/page.tsx`
- `frontend/src/app/dashboard/dashboard.module.css`

### [x] E3. Improve workflow start error handling
Description:
- Keep UX resilient for backend failures/timeouts.

Acceptance criteria:
- Actionable error messages for API unreachable, validation error, rate-limit.
- Retry mechanism on start action.

Files:
- `frontend/src/app/page.tsx`

## F. Reliability, Security, and Quality

### [x] F1. Add robust error model and logging
Description:
- Standardize exception handling across all steps.

Acceptance criteria:
- Catch and classify errors: LLM/API timeout, render fail, file I/O fail, validation fail.
- Persist error type + message in DB.
- Return consistent API error payload format.

Files:
- `backend/app/api/routes.py`
- `backend/app/agents/orchestrator.py`

### [x] F2. Add automated tests for core flows
Description:
- Add minimum test coverage for production confidence.

Acceptance criteria:
- Unit tests for state routing and approval logic.
- Integration test for `run-workflow -> approve -> status`.
- Failure tests for API timeout and render subprocess error.

Files:
- `backend/tests/*` (new)
- Optional frontend API integration tests

### [x] F3. Encoding and documentation cleanup
Description:
- Fix mojibake/garbled Vietnamese text in docs and source comments.

Acceptance criteria:
- All `.md`, `.py`, `.tsx` files saved as UTF-8.
- Key docs readable in Vietnamese/English without broken characters.

Files:
- `docs/*`
- `knowledge/*`
- affected source files
Progress note:
- UTF-8 normalization executed for all Markdown files under:
  - `docs/*`
  - `knowledge/*`
  - `reference/*`
- Core docs were rewritten with clean content where needed:
  - `docs/architecture.md`
  - `docs/techstack.md`
  - `docs/video-generation-remotion.md`

## G. Extended Phases (SEO, Newsletter, Analyst & UI Polish)

### [ ] G1. Database & API integration for SEO, Newsletter, Analyst
Description:
- Nodes already exist in LangGraph, but we need to persist their results and expose them.
Acceptance criteria:
- `seo_result`, `newsletter_result`, `analyst_result` columns added to `ContentTask` model.
- `update_task_from_state` maps these fields correctly.
- `GET /api/status/{task_id}` returns the extended data.
Files:
- `backend/app/db/models.py`
- `backend/app/db/repository.py`
- `backend/app/api/routes.py`

### [ ] G2. Dashboard UI/UX Polish & Extended Steps
Description:
- Display the extended 3 steps on the stepper and replace raw JSON output with a rich UI.
Acceptance criteria:
- Steps SEO, Newsletter, and Analyst appear in the stepper.
- Output uses native `<audio>`, `<img>`, `<video>` tags and card layouts instead of `<pre>` tags.
- Uses existing CSS Modules (no new UI libraries).
Files:
- `frontend/src/app/dashboard/page.tsx`
- `frontend/src/app/dashboard/dashboard.module.css`

## H. Optional but Recommended Next

### [ ] H1. Add ChromaDB memory write/read pipeline for long-term optimization
### [ ] H2. Add CI checks (lint + typecheck + tests)

---

## Progress Tracking Rule
- Mark task as `[x]` only when code is merged and acceptance criteria are verified locally.
- If partially done, keep `[ ]` and add sub-notes in PR description instead.

## Verification Notes
- Lint verification executed successfully via absolute NVM path provided by user:
  - `C:\nvm4w\nodejs\npm.cmd run lint` in `remotion_app` (exit code 0)
  - `C:\nvm4w\nodejs\npm.cmd run lint` in `frontend` (exit code 0)
- Environment caveat for this agent session: direct `npm` in PATH was unavailable, so absolute path execution was required.


