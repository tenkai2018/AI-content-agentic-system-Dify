import os

os.environ["DATABASE_URL"] = "sqlite:///./test_app.db"

from app.api.routes import _next_state_after_approval


def test_next_state_transitions_for_happy_path():
    assert _next_state_after_approval("awaiting_topic_approval", "topic", True) == (
        "awaiting_script_approval",
        "script_writing",
        None,
    )
    assert _next_state_after_approval("awaiting_script_approval", "script", True) == (
        "awaiting_thumbnail_approval",
        "thumbnail_brief",
        None,
    )
    assert _next_state_after_approval("awaiting_thumbnail_approval", "thumbnail", True) == (
        "awaiting_assets_approval",
        "asset_generation",
        None,
    )
    assert _next_state_after_approval("awaiting_assets_approval", "assets", True) == (
        "completed",
        "linkedin_repurposing",
        None,
    )


def test_next_state_reject_fails_run():
    status, step, error = _next_state_after_approval("awaiting_topic_approval", "topic", False)
    assert status == "failed"
    assert step == "stopped"
    assert "rejected" in (error or "")
