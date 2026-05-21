import pytest

from app.agents import orchestrator


@pytest.mark.asyncio
async def test_resume_topic_rejected_sets_failed():
    state = {
        "task_id": "t1",
        "niche": "ai",
        "keywords": [],
        "language": "en",
        "current_step": "viral_detection",
        "status": "awaiting_topic_approval",
        "error": None,
        "viral_detection_result": {},
        "selected_topic": None,
        "script_result": None,
        "thumbnail_brief": None,
        "assets_result": None,
        "video_result": None,
        "linkedin_posts": None,
        "topic_approved": False,
        "script_approved": False,
        "thumbnail_approved": False,
        "assets_approved": False,
    }

    result = await orchestrator.resume_pipeline(state, step="topic", approved=False)
    assert result["status"] == "failed"
    assert "Topic rejected" in result["error"]


@pytest.mark.asyncio
async def test_resume_assets_approved_continues(monkeypatch):
    async def fake_video_producer(updated_state):
        return {
            **updated_state,
            "current_step": "video_render",
            "status": "repurposing",
            "video_result": {"output_path": "/tmp/out.mp4"},
            "error": None,
        }

    async def fake_repurposer(updated_state):
        return {
            **updated_state,
            "current_step": "linkedin_repurposing",
            "status": "completed",
            "linkedin_posts": {"posts": {}},
            "error": None,
        }

    async def fake_seo(updated_state):
        return {
            **updated_state,
            "current_step": "seo_optimization",
            "status": "newsletter_generating",
            "seo_result": {"youtube_title_options": ["a", "b", "c"]},
            "error": None,
        }

    async def fake_newsletter(updated_state):
        return {
            **updated_state,
            "current_step": "newsletter_generation",
            "status": "analyzing",
            "newsletter_result": {"subject_line": "hello"},
            "error": None,
        }

    async def fake_analyst(updated_state):
        return {
            **updated_state,
            "current_step": "performance_analysis",
            "status": "completed",
            "analyst_result": {"kpis": ["views"]},
            "error": None,
        }

    monkeypatch.setattr(orchestrator, "video_producer_node", fake_video_producer)
    monkeypatch.setattr(orchestrator, "repurposer_node", fake_repurposer)
    monkeypatch.setattr(orchestrator, "seo_node", fake_seo)
    monkeypatch.setattr(orchestrator, "newsletter_node", fake_newsletter)
    monkeypatch.setattr(orchestrator, "analyst_node", fake_analyst)

    state = {
        "task_id": "t1",
        "niche": "ai",
        "keywords": [],
        "language": "en",
        "current_step": "asset_generation",
        "status": "awaiting_assets_approval",
        "error": None,
        "viral_detection_result": {},
        "selected_topic": {},
        "script_result": {"script": {"full_script_text": "test."}},
        "thumbnail_brief": {},
        "assets_result": {"manifest_path": "/tmp/manifest.json"},
        "video_result": None,
        "linkedin_posts": None,
        "topic_approved": True,
        "script_approved": True,
        "thumbnail_approved": True,
        "assets_approved": False,
    }

    result = await orchestrator.resume_pipeline(state, step="assets", approved=True)
    assert result["status"] == "completed"
    assert result["video_result"]["output_path"] == "/tmp/out.mp4"
    assert result["current_step"] == "performance_analysis"
