# Comprehensive QA/QC Test Plan
**Project:** AI Content Agentic System (v1)
**Date:** 2026-05-17
**Phase:** Pre-Launch / Runtime Verification

## 1. Introduction & Objectives
The purpose of this Test Plan is to outline the strategy, scope, environment, and specific test scenarios required to validate the AI Content Agentic System v1. The objective is to ensure the pipeline is robust, handles external API failures gracefully, strictly enforces schema validation, and guarantees reliable state transitions during the Human-in-the-Loop (HITL) approval process.

## 2. Scope of Testing
**In-Scope:**
*   **Backend API Endpoints:** `/api/run-workflow`, `/api/approve`, `/api/status`, `/api/health`.
*   **Agent Pipeline (LangGraph):** All state transitions and step resumptions (Research -> Script -> Thumbnail -> Assets -> Video -> Repurposer).
*   **External API Integrations:** YouTube Data API, OpenAI (LLM, TTS, DALL-E), Remotion CLI subprocess.
*   **State Persistence:** PostgreSQL database (`content_tasks` table) read/write validation.
*   **Frontend Dashboard:** UI polling, state visualizations, and accept/reject action handling.

**Out of Scope:**
*   Performance/Load testing for thousands of concurrent users (system is designed for internal/orchestrated use in v1).
*   Long-term memory vector database (ChromaDB) which is planned for future phases.

## 3. Test Strategy
Testing will be conducted across three primary levels:
1.  **Unit Testing:** Validate individual utility functions (e.g., JSON parsers, YouTube API mock responses).
2.  **Integration Testing:** Test API endpoints, DB persistence, and LangGraph node orchestration without triggering real paid external APIs (using mocked LLM/TTS responses).
3.  **End-to-End (E2E) Testing:** Complete dry-run and live-run pipeline execution from initiating a workflow on the frontend to producing the final Remotion MP4 video.

## 4. Test Scenarios & Cases

### 4.1 Backend Orchestration & Database (HITL Pipeline)
| Test Case ID | Description | Pre-conditions | Expected Result |
| :--- | :--- | :--- | :--- |
| `ORCH-01` | Initializing workflow creates new task ID in DB. | Valid prompt/niche provided. | DB inserts new row, status = `generating_topic`, returns HTTP 200. |
| `ORCH-02` | Pipeline pauses at `topic_approval`. | Workflow reaches topic generation. | State transitions to `awaiting_topic_approval` and waits. |
| `ORCH-03` | Rejecting a step resubmits it for generation. | Task is in `awaiting_topic_approval`. | Status reverts to `generating_topic`, LLM is called again. |
| `ORCH-04` | Approving a step progresses pipeline. | Task is in `awaiting_script_approval`. | Status moves to `generating_thumbnail`. |
| `ORCH-05` | Resuming task with invalid task ID. | Unknown task ID used. | HTTP 404/400 returned, system does not crash. |

### 4.2 External Data & Generation (LLM, Audio, Visual)
| Test Case ID | Description | Pre-conditions | Expected Result |
| :--- | :--- | :--- | :--- |
| `GEN-01` | YouTube API Outlier detection failure (broad keywords). | Keyword yielding 0 outlier score videos. | Pipeline catches error, halts, sets status to `error`. |
| `GEN-02` | Invalid YouTube API Key provided. | API Key revoked or malformed. | Exception caught, pipeline logs specific API authentication error. |
| `GEN-03` | LLM returns malformed JSON structure. | Mock LLM returns raw text instead of JSON. | Schema validator catches `ValidationError`, raises exception, task moves to `error`. |
| `GEN-04` | TTS/Image generation rate limits or timeouts. | OpenAI API throws 429 or timeout. | Appropriate error is stored in task metadata. |

### 4.3 Remotion Runtime Execution
| Test Case ID | Description | Pre-conditions | Expected Result |
| :--- | :--- | :--- | :--- |
| `REM-01` | Subprocess executes valid render command. | Valid assets downloaded, manifest generated. | MP4 successfully generated at target path, DB stores `video_result`. |
| `REM-02` | Subprocess times out. | Artificial delay injected in Remotion script. | Subprocess killed after timeout (e.g., 5 mins), task errors out gracefully. |
| `REM-03` | Asset paths in manifest are missing. | An image or audio file fails to download. | Remotion returns failure code, orchestrator captures subprocess stderr. |

### 4.4 Frontend Dashboard Behavior
| Test Case ID | Description | Pre-conditions | Expected Result |
| :--- | :--- | :--- | :--- |
| `UI-01` | Live polling respects error boundaries. | API goes down during polling. | UI displays "Connection Lost" or equivalent without breaking the application. |
| `UI-02` | Dashboard reflects correct state based on DB. | Backend task manually updated in DB. | Polling UI updates to new status within N seconds. |
| `UI-03` | Approve button disables during processing. | User clicks 'Approve'. | Button enters loading state immediately to prevent double submission. |

## 5. Execution Environment Prerequisites
*   **Database:** Local PostgreSQL instance running (`docker-compose up`).
*   **APIs:** Valid `.env` variables for `OPENAI_API_KEY`, `YOUTUBE_API_KEY`.
*   **Video Runtime:** Node.js installed, `npm install` run inside `/remotion_app`.
*   **Frontend:** Next.js dev server running on port `3000`.
*   **Backend:** FastAPI running on port `8000` via Uvicorn.

## 6. Defect Reporting Protocol
When filing bugs discovered during this testing phase, QA will provide:
1.  **Task ID** associated with the failure.
2.  **State** of the database for the given Task ID.
3.  **Logs:** Snippet of FastAPI backend logs and Frontend console logs.
4.  **Payloads:** Exact payload submitted to `/api/run-workflow` or `/api/approve`.

