# Kế hoạch triển khai (Implementation Plan) - Extended Phase

## Mục tiêu
Hoàn thiện 3 bước cuối của pipeline (SEO, Newsletter, Analyst) và nâng cấp giao diện Frontend Dashboard để hiển thị trực quan các đầu ra, tạo thành một hệ thống 9 bước hoàn chỉnh.

## Trạng thái hiện tại (Phân tích từ Code Review)
- Các node `seo_node`, `newsletter_node`, `analyst_node` đã được định nghĩa trong `backend/app/agents/orchestrator.py` và kết nối thành công vào chuỗi LangGraph.
- **Vấn đề Backend**: Thiếu các cột lưu trữ 3 kết quả này trong Database (`models.py`) và chưa trả về qua API `/api/status`.
- **Vấn đề Frontend**: Các bước này chưa hiển thị trên thanh tiến trình (Stepper). Kết quả đang hiển thị dưới dạng JSON thô `<pre>` thay vì giao diện media thân thiện.

## Tác vụ phát triển (Development Tasks)

### 1. Database & API Backend
- **Cập nhật Database Model**: Thêm các cột JSONB `seo_result`, `newsletter_result`, `analyst_result` vào bảng `content_tasks` trong `backend/app/db/models.py`.
- **Cập nhật Repository**: Ánh xạ dữ liệu từ LangGraph state vào 3 cột mới trong hàm `update_task_from_state` của `backend/app/db/repository.py`.
- **Cập nhật API Status**: Đưa dữ liệu 3 cột này vào payload trả về của `GET /api/status/{task_id}` (`backend/app/api/routes.py`).

### 2. Frontend UI/UX
Sử dụng CSS Modules và thẻ HTML/React thuần hiện tại để đồng bộ (không cài thêm shadcn/ui hay FluxUI).
- **Mở rộng Stepper**: Bổ sung các bước SEO, Newsletter, Analyst vào hằng số `STEPS` và cập nhật kiểu `PipelineStatus`.
- **Thiết kế lại Output View**:
  - **Script**: Hiển thị đoạn văn có cấu trúc.
  - **Assets**: Render danh sách các cảnh (Scenes) dưới dạng lưới (Grid), mỗi cảnh kèm thẻ `<img>` và `<audio controls>`.
  - **Video**: Nhúng trình phát `<video controls>` cho file MP4.
  - **Các bước báo cáo (LinkedIn, SEO, Newsletter, Analyst)**: Hiển thị dạng thẻ (Cards) dễ đọc.

## Kế hoạch kiểm thử (Test Plan)
- Chạy lệnh `pytest` cho repository mapping để đảm bảo DB lưu thành công các cột mới.
- Chạy E2E quy trình từ tạo chủ đề, đi qua toàn bộ 9 bước (bao gồm 4 mốc kiểm duyệt) và quan sát giao diện cập nhật thời gian thực.
- Kiểm thử các thẻ media (audio, video) có hoạt động chính xác theo đường dẫn tĩnh (static paths) hay không.
