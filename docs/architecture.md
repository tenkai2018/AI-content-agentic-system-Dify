# Agentic AI Content Machine - Architecture (Clean UTF-8)

## 1. M?c tiêu
H? th?ng t? d?ng hóa quy trình s?n xu?t n?i dung da n?n t?ng theo mô hình multi-agent, có Human-in-the-loop (HITL), và có th? m? r?ng sang video rendering t? d?ng.

## 2. Ki?n trúc 4 l?p
1. Frontend Layer
- Dashboard nh?p niche/topic
- Theo dõi tr?ng thái task theo `task_id`
- Duy?t ho?c t? ch?i t?ng checkpoint

2. Orchestration Layer
- FastAPI + LangGraph di?u ph?i state machine
- Các agent chuyên trách:
  - Researcher
  - Scriptwriter
  - Visual Director
  - Asset Generator
  - Video Producer
  - Repurposer

3. LLM Layer
- H? tr? OpenAI / Anthropic / Ollama qua `llm_factory`
- Tách role theo m?c dích: reasoning / writing / vision

4. Memory & Persistence Layer
- PostgreSQL luu tr?ng thái và output theo task
- File-based knowledge trong `knowledge/`
- Asset/manifest/video luu trong `remotion_app/public/assets/generated/{task_id}`

## 3. Lu?ng th?c thi hi?n t?i (v1)
1. `run-workflow`
2. Researcher (YouTube data th?t + outlier score)
3. Ch? duy?t topic
4. Scriptwriter
5. Ch? duy?t script
6. Visual Director
7. Ch? duy?t thumbnail
8. Asset Generator (TTS + image)
9. Ch? duy?t assets
10. Video Producer (Remotion render)
11. Repurposer (LinkedIn posts)
12. Completed / Failed

## 4. Tr?ng thái tr?ng y?u
- `awaiting_topic_approval`
- `awaiting_script_approval`
- `awaiting_thumbnail_approval`
- `awaiting_assets_approval`
- `repurposing`
- `completed`
- `failed`

## 5. Thi?t k? k? thu?t quan tr?ng
- Schema validation b?t bu?c cho output các agent
- Error payload chu?n hóa (`code`, `message`, `task_id`, `step`)
- Resume pipeline qua `/api/approve`
- Status query qua `/api/status/{task_id}`

## 6. Thành ph?n c?n hardening thêm
- Full runtime verification trong môi tru?ng CI/local chu?n
- Tang coverage test integration/failure paths
- Hoàn t?t cleanup encoding cho toàn b? docs/knowledge

