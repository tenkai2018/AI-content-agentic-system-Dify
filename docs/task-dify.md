# Dify System Delivery Task Board (with Owner Assignment)

## Team Members and Ownership
- **PM/Integrator**: Delivery planning, dependency control, acceptance sign-off.
- **Infra Engineer**: VPS, Docker Compose, reverse proxy, SSL, backup/restore.
- **Backend Engineer**: FastAPI gateway, event ingestion, DB schema, audit trail.
- **Admin FE Engineer**: Admin Control Center (config, connections, env, secrets, observability).
- **Workspace FE Engineer**: Content Workflow Workspace (7-step user interaction UI).
- **Dify Engineer**: Dify app/agent design, DSL versioning, output schema alignment.
- **n8n Engineer**: Workflow orchestration, retry/failure paths, webhook integration.
- **QA Engineer**: E2E/UAT, regression, smoke/failure tests.

---

## Phase 0 - Project Setup and Governance
- [ ] Create branch strategy and release checklist.
  - Owner: PM/Integrator
  - Required Skill: project governance, release management
- [ ] Define Definition of Done for P0/P1/P2.
  - Owner: PM/Integrator
  - Required Skill: delivery governance
- [ ] Freeze canonical contracts: event schema + result contract.
  - Owner: Backend Engineer
  - Required Skill: API design, contract-first design

---

## Phase 1 - Infrastructure and Deployment Baseline (P0)
- [ ] Prepare per-client single-tenant deployment baseline (VPS + Docker Compose + reverse proxy + SSL).
  - Owner: Infra Engineer
  - Required Skill: Docker, Nginx/Caddy, Linux ops
- [ ] Finalize environment templates (`.env.template`) for admin/workspace/backend/infra.
  - Owner: Infra Engineer
  - Required Skill: environment management, secure configuration
- [ ] Implement backup and restore for Postgres + critical artifacts.
  - Owner: Infra Engineer
  - Required Skill: database ops, disaster recovery
- [ ] Produce handover runbook (deploy, restart, rollback, incident response).
  - Owner: PM/Integrator
  - Required Skill: operational documentation

---

## Phase 2 - Backend Gateway and Data Foundation (P0)
- [ ] Implement minimum workflow APIs:
  - `POST /workflow/start`
  - `GET /workflow/{task_id}`
  - `POST /workflow/{task_id}/action`
  - `GET /workflow/{task_id}/artifacts`
  - `GET /workflow/{task_id}/history`
  - Owner: Backend Engineer
  - Required Skill: FastAPI, REST API
- [ ] Implement admin APIs for config/connections/secrets.
  - Owner: Backend Engineer
  - Required Skill: FastAPI, RBAC/security
- [ ] Implement standardized event ingestion:
  - `run_started`, `step_completed`, `approval_required`, `run_failed`, `run_completed`
  - Owner: Backend Engineer
  - Required Skill: event-driven integration
- [ ] Finalize DB schema:
  - `runs`, `run_steps`, `events`, `approvals`, `artifacts`, `config_versions`, `secret_audit_logs`
  - Owner: Backend Engineer
  - Required Skill: PostgreSQL, schema design

---

## Phase 3 - Admin Control Center (P0)
- [ ] Split admin UI into dedicated app (`frontend-admin`).
  - Owner: Admin FE Engineer
  - Required Skill: Next.js App Router
- [ ] Build Config Center screens:
  - Connections
  - Environment Variables by environment
  - Secrets (masked, rotate/revoke)
  - Test connection actions
  - Owner: Admin FE Engineer
  - Required Skill: Next.js, secure UI patterns
- [ ] Build observability screens (status, timeline, error/failure, latency).
  - Owner: Admin FE Engineer
  - Required Skill: data visualization, dashboard UX
- [ ] Add audit view for config changes.
  - Owner: Admin FE Engineer
  - Required Skill: admin UX, audit UX

---

## Phase 4 - Workflow Workspace for Content Machine (P0)
- [ ] Create dedicated workspace app (`frontend-workspace-content`).
  - Owner: Workspace FE Engineer
  - Required Skill: Next.js App Router
- [ ] Implement 7-step interactive flow UI:
  1. Research Input
  2. Research Results (video cards + thumbnails + outlier score)
  3. Script Draft (edit + approve)
  4. Thumbnail Brief (approve/regenerate)
  5. Assets Preview (scene image/audio)
  6. Video Output
  7. Repurpose Output
  - Owner: Workspace FE Engineer
  - Required Skill: workflow UI architecture, interaction design
- [ ] Bind workspace UI to result contract and allowed actions.
  - Owner: Workspace FE Engineer
  - Required Skill: schema-driven rendering
- [ ] Implement state handling for canonical statuses:
  - `awaiting_topic_approval`
  - `awaiting_script_approval`
  - `awaiting_thumbnail_approval`
  - `awaiting_assets_approval`
  - `rendering_video`
  - `repurposing`
  - `completed`
  - `failed`
  - Owner: Workspace FE Engineer
  - Required Skill: state machine UI mapping

---

## Phase 5 - Dify and n8n Integration (P0)
- [ ] Finalize Dify apps/agents for Content Machine and align outputs to schema.
  - Owner: Dify Engineer
  - Required Skill: Dify workflow/app design
- [ ] Export and version Dify DSL for packaging.
  - Owner: Dify Engineer
  - Required Skill: Dify DSL lifecycle
- [ ] Finalize n8n orchestration flows (webhooks/retry/error handling).
  - Owner: n8n Engineer
  - Required Skill: n8n workflow engineering
- [ ] Export and version n8n workflow JSON for packaging.
  - Owner: n8n Engineer
  - Required Skill: n8n template packaging
- [ ] Ensure both Dify and n8n emit canonical events to backend.
  - Owner: Backend Engineer
  - Required Skill: integration contracts

---

## Phase 6 - QA, UAT, and Go-Live (P0)
- [ ] Create E2E test checklist for full 7-step flow.
  - Owner: QA Engineer
  - Required Skill: E2E test design
- [ ] Run smoke tests (happy path), failure tests, and approval/resume tests.
  - Owner: QA Engineer
  - Required Skill: integration testing
- [ ] Execute UAT with business acceptance criteria.
  - Owner: PM/Integrator
  - Required Skill: UAT facilitation
- [ ] Go-live readiness review and sign-off.
  - Owner: PM/Integrator
  - Required Skill: release governance

---

## Phase 7 - Template/Kit Packaging (P0 for commercialization)
- [ ] Package client delivery bundle:
  - `.env.template`
  - Dify DSL export
  - n8n workflow export
  - DB migration/seed
  - operations runbook
  - Owner: PM/Integrator
  - Required Skill: productization
- [ ] Validate clean install from bundle on fresh VPS.
  - Owner: Infra Engineer
  - Required Skill: reproducible deployment
- [ ] Write onboarding guide for next client reuse.
  - Owner: PM/Integrator
  - Required Skill: implementation playbook design

---

## P1 - Stability and Reuse Enhancements
- [ ] Schema registry for versioned step outputs.
  - Owner: Backend Engineer
  - Required Skill: schema governance
- [ ] Artifact versioning + diff + rollback.
  - Owner: Backend Engineer
  - Required Skill: content version control model
- [ ] Checkpoint replay (rerun from selected step).
  - Owner: Backend Engineer
  - Required Skill: workflow state control
- [ ] Flow definition engine to reduce hardcoded workspace logic.
  - Owner: Workspace FE Engineer
  - Required Skill: config-driven UI architecture
- [ ] Config export/import (config-as-code).
  - Owner: Admin FE Engineer
  - Required Skill: configuration lifecycle tooling

---

## P2 - Optimization and Operational Scale
- [ ] SLA-based alerting (latency/failure thresholds).
  - Owner: Infra Engineer
  - Required Skill: monitoring and alerting
- [ ] RAG namespace strategy (`knowledge`, `context`, `approved_outputs`).
  - Owner: Dify Engineer
  - Required Skill: RAG architecture
- [ ] Post-deploy automation QA scripts.
  - Owner: QA Engineer
  - Required Skill: test automation
- [ ] Standardized client onboarding playbook.
  - Owner: PM/Integrator
  - Required Skill: service standardization

---

## Delivery Gates (Must Pass)
- [ ] Gate A - Deploy and handover ready.
- [ ] Gate B - Sellable as template/kit.
- [ ] Gate C - Reusable for new project packs.

## Notes
- This board is for the current Content Machine implementation.
- Future projects should reuse core layers and replace only the business-pack flow/UI.
