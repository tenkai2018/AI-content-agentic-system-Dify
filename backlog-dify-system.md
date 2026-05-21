# Backlog Dify System

## 1) Product Direction (Confirmed)
- This is a reusable system template deployed per client (single-tenant per client), not a multi-client platform on a shared instance.
- The current project is the business pack for the Content Machine use case.
- Future clients may use different business flows (for example, Resort Customer Care), while keeping the same reusable core.

## 2) Target System Layers
- FE Admin Control Center: centralized administration, orchestration, connection setup, environment configuration, and operations.
- Workflow Workspace UI (project-specific): user-facing workflow screen for step-by-step input, outputs, approvals, edits, and regenerations.
- Dify: Agentic AI brain (prompt/agent logic/RAG retrieval/model routing).
- n8n: orchestration for flows that are more complex outside Dify (cron/webhook/integration/retry/fan-out).
- PostgreSQL: logs, events, run state, approval state, artifact metadata.
- RAG Layer: knowledge, context, and approved outputs for reuse.

## 3) UI Separation (Must-Have)

### 3.1 Admin Control Center (Reusable Core)
- System Health: Dify/n8n/DB/RAG status.
- Observability: timeline, errors, latency, success/failure rates by step.
- Config Center:
  - Connections (Dify, n8n, DB, RAG, external APIs)
  - Environment Variables (dev/staging/prod)
  - Secrets Management (masked values, rotate/revoke, connection test)
  - Runtime Config (model/provider, timeout/retry/concurrency)
  - Approval Policy (which steps require HITL)
- Audit Log: who changed what and when.

### 3.2 Workflow Workspace (Project-Specific UI)
- Must be separate from the admin screen.
- Must be designed per project business flow.
- For the Content Machine project, the UI flow includes:
  1. Research Input
  2. Research Results (video cards with thumbnails and outlier score)
  3. Script Draft (edit + approve)
  4. Thumbnail Brief (approve/regenerate)
  5. Assets Preview (image/audio per scene)
  6. Video Output
  7. Repurpose Output

## 4) Content Machine Flow States (Canonical)
- awaiting_topic_approval
- awaiting_script_approval
- awaiting_thumbnail_approval
- awaiting_assets_approval
- rendering_video
- repurposing
- completed
- failed

## 5) Integration Principles
- The Workflow Workspace should interact through a Backend API Gateway (thin FastAPI), not through direct fragmented calls to multiple services.
- Dify and n8n must emit standardized events to backend for a single source of truth.
- Backend must normalize outputs into a Result Contract for consistent FE rendering.

## 6) Result Contract v1 (for Workflow Workspace)
- journey_stage
- current_status
- step_data
- cards[] (insight/recommendation/action/asset)
- timeline[]
- artifacts[]
- kpis[]
- allowed_actions[] (approve/edit/regenerate/retry)

## 7) Core vs Business Pack Structure
- core/ (reusable, minimal client-specific edits):
  - admin FE
  - backend gateway + event schema
  - observability + audit
  - config/secret runtime
- business-pack/content-machine/:
  - flow definition
  - dify dsl
  - n8n workflow json
  - knowledge assets
  - workflow workspace renderer
- business-pack/resort-care-machine/ (future): same structure, different business flow.

## 8) Backlog Priority

### P0 - Must Complete (Foundation)
1. Separate the two UI apps:
- frontend-admin/
- frontend-workspace-content/

2. Complete Admin Config Center:
- connection management
- environment variables by environment
- masked secrets + rotation
- connection testing

3. Standardize system-wide Event Schema:
- run_started
- step_completed
- approval_required
- run_failed
- run_completed

4. Minimum Backend API Gateway:
- POST /workflow/start
- GET /workflow/{task_id}
- POST /workflow/{task_id}/action
- GET /workflow/{task_id}/artifacts
- GET /workflow/{task_id}/history
- admin APIs for config/connections/secrets

5. Design DB schema for runtime + audit:
- runs
- run_steps
- events
- approvals
- artifacts
- config_versions
- secret_audit_logs

6. Implement Workflow Workspace for Content Machine with all 7 UI steps.

### P1 - High Value (Stability & Reuse)
1. Schema Registry for versioned step outputs.
2. Artifact Versioning + diff + rollback.
3. Checkpoint Replay (rerun from selected step).
4. Flow Definition Engine (reduce hardcoded UI/workflow logic).
5. Config export/import (config-as-code) for fast client replication.

### P2 - Optimization (Scale & Ops)
1. Advanced alerting by SLA/latency/failure thresholds.
2. RAG namespace strategy (knowledge/context/approved_outputs).
3. Automation QA checklist + post-deploy smoke test scripts.
4. Standardized onboarding playbook for new client deployments.

## 9) Deployment Model (Template-First)
- One client = one dedicated deployment stack (single-tenant).
- Recommended stack: VPS + Docker Compose + reverse proxy + SSL.
- Client delivery artifacts:
  - .env template
  - Dify DSL export
  - n8n workflow export
  - DB migrations/seeds
  - Operations runbook

## 10) Non-Goals (to avoid scope creep)
- No multi-tenant SaaS in this phase.
- Do not merge admin UI and workflow result UI.
- Do not hardcode business logic in core when it can be defined in business packs.

## 11) Definition of Done (This Project Phase)
- Admin Control Center manages config, secrets, connections, logs, and health.
- Content Machine Workflow Workspace completes all 7 steps with approval and resume.
- Dify + n8n + backend are aligned on the standardized event schema.
- DB stores complete audit trail and artifacts by task_id.
- Template packaging is ready for reuse with the next client.
