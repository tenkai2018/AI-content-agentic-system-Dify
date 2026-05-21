import os
from pathlib import Path

# Đường dẫn gốc tới thư mục remotion_app
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
REMOTION_APP_DIR = BASE_DIR / "remotion_app"
GENERATED_ASSETS_DIR = REMOTION_APP_DIR / "public" / "assets" / "generated"

def get_generated_assets_dir(task_id: str) -> Path:
    """
    Tạo và trả về đường dẫn thư mục lưu trữ assets sinh tự động cho một task.
    Ví dụ: remotion_app/public/assets/generated/{task_id}
    """
    task_dir = GENERATED_ASSETS_DIR / task_id
    
    # Tạo thư mục nếu chưa tồn tại
    os.makedirs(task_dir, exist_ok=True)
    
    return task_dir

def get_manifest_path(task_id: str) -> Path:
    """
    Trả về đường dẫn tới file manifest.json của một task cụ thể.
    """
    # Ta lưu manifest thẳng vào thư mục của task đó luôn cho tiện quản lý
    task_dir = get_generated_assets_dir(task_id)
    return task_dir / "manifest.json"
