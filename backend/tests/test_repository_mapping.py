from app.db.models import TaskStatus
from app.db.repository import _to_task_status


def test_state_to_status_mapping_includes_assets_and_rendering():
    assert _to_task_status("awaiting_assets_approval") == TaskStatus.AWAITING_ASSETS_APPROVAL
    assert _to_task_status("rendering_video") == TaskStatus.RENDERING_VIDEO
    assert _to_task_status("repurposing") == TaskStatus.REPURPOSING


def test_unknown_status_falls_back_to_pending():
    assert _to_task_status("unknown_value") == TaskStatus.PENDING
