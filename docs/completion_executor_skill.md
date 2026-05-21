# Skill: AI Content Agentic System Completion Executor

## Purpose
This skill guides implementation of all unfinished functions listed in `docs/task.md`.
Use this as the operational playbook to execute work in correct order, with clear done criteria.

## Scope
- Backend (FastAPI + LangGraph + DB)
- Frontend (Next.js HITL UI)
- Remotion video layer
- Reliability, tests, and quality gates

## Inputs
- `docs/task.md` (source of truth for backlog)
- `knowledge/*` (business workflow and agent skill context)
- Current source code under `backend/`, `frontend/`, `remotion_app/`

## Global Rules
1. Execute by phases; do not start a later phase before acceptance criteria of current phase are met.
2. Persist state before adding more workflow complexity.
3. Every checkpoint (topic/script/thumbnail/assets) must support approve + reject path.
4. No hardcoded placeholder behavior in production paths.
5. Every new behavior must have at least one automated verification.

---

## Phase 1 - Make Pipeline Operable (Critical)

### Step 1. Implement DB state persistence
Actions:
- Add DB session/repository layer.
- Persist task creation, state updates, and step outputs.

Done when:
- A new run creates one `content_tasks` record.
- Every step writes status/output to DB.
- Failure writes `error_message` and sets `FAILED`.

### Step 2. Implement `/api/status/{task_id}`
Actions:
- Replace placeholder status endpoint with DB query.
- Return structured status + outputs.

Done when:
- Valid `task_id` returns real current state.
- Invalid `task_id` returns 404.

### Step 3. Implement `/api/approve` resume
Actions:
- Load persisted state by task id.
- Update approval flags by `step`.
- Resume orchestrator from next node.

Done when:
- Topic approval moves to script step.
- Script approval moves to thumbnail step.
- Thumbnail approval moves to repurposer (or assets in extended flow).

---

## Phase 2 - Data-first Research and Output Integrity

### Step 4. Integrate real research data source
Actions:
- Connect YouTube data acquisition (direct or via n8n).
- Compute Outlier Score from real metrics.

Done when:
- At least 20 videos are analyzed per request.
- Results are ranked and filtered by score threshold.

### Step 5. Add strict schema validation for all agent outputs
Actions:
- Define Pydantic schemas for each step output.
- Validate before persisting and routing.

Done when:
- Malformed LLM output is rejected with explicit error state.
- Valid output is persisted and routed forward.

---

## Phase 3 - Video Automation Completion

### Step 6. Extend pipeline state for video flow
Actions:
- Add `assets_result`, `assets_approved`, `video_result`, render status/error fields.

Done when:
- State can represent full lifecycle from script to rendered MP4.

### Step 7. Implement `asset_generator_node`
Actions:
- Split script into scenes/slides.
- Generate TTS and image assets for each scene.
- Save under `remotion_app/public/assets/generated/{task_id}`.

Done when:
- Asset map contains local paths for image/audio per scene.
- Asset generation errors are captured and persisted.

### Step 8. Implement assets HITL checkpoint
Actions:
- Pause pipeline awaiting user approval of assets.
- Support reject path (regen/stop).

Done when:
- Approve continues to render node.
- Reject produces deterministic behavior and status.

### Step 9. Implement `video_producer_node`
Actions:
- Build manifest from approved assets.
- Run Remotion render subprocess with timeout.
- Persist output path and render logs.

Done when:
- Successful run returns MP4 path.
- Render failure returns actionable error.

---

## Phase 4 - Remotion Runtime Integration

### Step 10. Replace mock screens with manifest-driven input
Actions:
- Read screens/audio/image from props or manifest.

Done when:
- CLI render uses backend-generated manifest data.

### Step 11. Dynamic duration from audio
Actions:
- Compute `durationInFrames` from summed scene audio durations + transitions.

Done when:
- Total duration matches actual playback.

### Step 12. Add per-slide voiceover and global BGM
Actions:
- Attach slide TTS with `<Audio />`.
- Add low-volume background music for full composition.

Done when:
- Voiceover timing and BGM are correct without overlaps/glitches.

---

## Phase 5 - Frontend HITL and Monitoring

### Step 13. Replace dashboard mock state
Actions:
- Poll status API or use SSE/WebSocket.
- Bind UI stepper and result panels to real backend state.

Done when:
- Dashboard reflects real task progression live.

### Step 14. Build approve/reject actions
Actions:
- Add buttons/forms for checkpoint approvals.
- Send correct payload to `/api/approve`.

Done when:
- User can complete full HITL loop from UI only.

### Step 15. Improve startup and runtime error UX
Actions:
- Surface actionable API errors.
- Add retry on start and transient failures.

Done when:
- User can recover from common failures without reload hacks.

---

## Phase 6 - Reliability and Quality Gates

### Step 16. Standardize error handling/logging
Actions:
- Classify errors by type (LLM/API/validation/render/file I/O).
- Return consistent API error payload.

Done when:
- Errors are searchable and understandable in DB/logs.

### Step 17. Add automated tests
Minimum required:
- Unit: routing + approval transitions.
- Integration: run -> approve -> status.
- Failure cases: timeout, invalid output, render fail.

Done when:
- Test suite passes locally and blocks regressions.

### Step 18. Encoding cleanup
Actions:
- Normalize docs/source to UTF-8.

Done when:
- No mojibake in user-facing text or docs.

---

## Definition of Done (Project-level)
- End-to-end flow runs from niche input to rendered video output.
- All HITL checkpoints are functional in UI.
- State is persisted and resumable by `task_id`.
- No placeholder/TODO logic remains on core APIs.
- Core test suite passes.

## Suggested Execution Order
1. Phase 1
2. Phase 2
3. Phase 3
4. Phase 4
5. Phase 5
6. Phase 6

## File Location
- This skill file: `docs/completion_executor_skill.md`
- Backlog source: `docs/task.md`

