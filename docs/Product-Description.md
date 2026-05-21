# AI Content Agentic System — Product Description

Dự án **AI-content-agentic-system** là một hệ thống tự động hóa quy trình sản xuất nội dung đa nền tảng theo mô hình **Multi-Agent (Đa tác nhân AI)** phối hợp nâng cao, tích hợp chặt chẽ cơ chế kiểm duyệt của con người **Human-in-the-loop (HITL)** và hỗ trợ dựng video tự động (automated video rendering).

---

## 🏗️ 1. Kiến trúc hệ thống (System Architecture)

Hệ thống được thiết kế theo mô hình single-tenant (triển khai độc lập cho từng khách hàng), gồm 4 lớp cốt lõi:

### 1.1 Frontend Layer (Next.js + TypeScript + Framer Motion)
Nằm trong thư mục [frontend](file:///d:/HUYTQ/ProdXSolution/Projects/AI-content-agentic-system%20-%20Dify/frontend).
- **Admin Control Center ([page.tsx](file:///d:/HUYTQ/ProdXSolution/Projects/AI-content-agentic-system%20-%20Dify/frontend/src/app/page.tsx))**: Cung cấp trung tâm quản trị tập trung. Tích hợp trực tiếp các iframe hiển thị giao diện làm việc của Dify, n8n, Remotion Studio và bảng theo dõi System Logs theo thời gian thực.
- **Workflow Workspace ([dashboard/page.tsx](file:///d:/HUYTQ/ProdXSolution/Projects/AI-content-agentic-system%20-%20Dify/frontend/src/app/dashboard/page.tsx))**: Giao diện làm việc chuyên biệt dành cho quy trình sản xuất nội dung của dự án **Content Machine**. Hỗ trợ nhập Niche/Keywords, hiển thị tiến độ 6 bước dạng Stepper, xem dữ liệu đầu ra và thực hiện các thao tác duyệt/từ chối HITL.

### 1.2 Orchestration Layer (FastAPI API Gateway)
Nằm trong thư mục [backend](file:///d:/HUYTQ/ProdXSolution/Projects/AI-content-agentic-system%20-%20Dify/backend).
- Đóng vai trò là cổng kết nối API Gateway và trung tâm quản trị trạng thái (State Machine).
- Tiếp nhận yêu cầu khởi chạy workflow, xử lý các phản hồi duyệt/từ chối (approve/reject) và điều hướng luồng dữ liệu.
- Định nghĩa các mô hình cơ sở dữ liệu để ghi vết lịch sử hoạt động.

### 1.3 LLM & Automation Layer (Dify & n8n)
Nằm trong thư mục [dify_n8n](file:///d:/HUYTQ/ProdXSolution/Projects/AI-content-agentic-system%20-%20Dify/dify_n8n).
- **Dify Brain ([dify_agent_dsl.yml](file:///d:/HUYTQ/ProdXSolution/Projects/AI-content-agentic-system%20-%20Dify/dify_n8n/dify_agent_dsl.yml))**: Định nghĩa Multi-Agent Workflow gồm 3 Agent chuyên trách: `Scriptwriter Agent` (viết kịch bản Hook 4 bước), `Visual Director Agent` (thiết kế brief thumbnail), và `Repurposer Agent` (tái chế kịch bản thành 6 định dạng LinkedIn).
- **n8n Flow ([n8n_workflow.json](file:///d:/HUYTQ/ProdXSolution/Projects/AI-content-agentic-system%20-%20Dify/dify_n8n/n8n_workflow.json))**: Tự động hóa các tích hợp bên ngoài Dify (gọi YouTube Search API thu thập dữ liệu nghiên cứu ban đầu, chuẩn hóa dữ liệu, kích hoạt Dify Workflow và gửi logs tiến trình về FastAPI).

### 1.4 Storage & Video Production Layer (PostgreSQL + Remotion)
- **PostgreSQL**: Lưu trữ logs hệ thống (`system_logs`), phiên chạy (`workflow_runs`), và lịch sử các sự kiện (`workflow_events`) phục vụ kiểm toán (Audit Trail) thông qua SQLAlchemy tại [models.py](file:///d:/HUYTQ/ProdXSolution/Projects/AI-content-agentic-system%20-%20Dify/backend/app/db/models.py).
- **Remotion App ([remotion_app](file:///d:/HUYTQ/ProdXSolution/Projects/AI-content-agentic-system%20-%20Dify/remotion_app))**: Engine dựng video dọc tự động bằng React từ cấu trúc tài nguyên đầu vào (`manifestData.ts`/`videoManifest.ts`), cho phép xuất trực tiếp thành file `.mp4` chất lượng cao.

---

## 🔄 2. Quy trình hoạt động (Workflow) của Content Machine

Quy trình sản xuất nội dung của **Content Machine** được chia thành 6 bước tuần tự, tích hợp kiểm duyệt HITL ở các mốc quan trọng:

1. **Bước 1: Viral Detection (Researcher Agent)**
   - Quét tối thiểu 20 video mới trong ngách từ YouTube Data API.
   - Tính toán chỉ số **Outlier Score** ($\frac{\text{Lượt xem video}}{\text{Lượt xem trung bình của kênh}} \times 100$) để tìm ra các chủ đề bùng nổ thực tế (Score $\ge$ 200).
   - 🛑 *HITL Checkpoint*: Tạm dừng chờ người dùng duyệt chủ đề muốn thực hiện (`awaiting_topic_approval`).

2. **Bước 2: Script Writing (Scriptwriter Agent)**
   - Claude 3.5 / GPT-4o-mini viết kịch bản ngắn tuân thủ cấu trúc Hook 4 bước: *Identify (Nỗi đau) -> Missed Opportunity (Cơ hội bỏ lỡ) -> Outcome (Kết quả đạt được) -> Visual Preview (Mô tả phân cảnh mở đầu)*.
   - 🛑 *HITL Checkpoint*: Tạm dừng chờ người dùng duyệt/chỉnh sửa kịch bản (`awaiting_script_approval`).

3. **Bước 3: Thumbnail Briefing (Visual Director Agent)**
   - Nghiên cứu xu hướng thumbnail viral và lập Thumbnail Brief cụ thể (concept, text overlay $\le$ 5 từ, các yếu tố cần tránh sao chép).
   - 🛑 *HITL Checkpoint*: Tạm dừng chờ người dùng duyệt brief (`awaiting_thumbnail_approval`).

4. **Bước 4: Asset Generation (Asset Generator Node)**
   - Tự động chia nhỏ kịch bản theo slide phân cảnh, gọi API OpenAI TTS để tạo Voiceover và DALL-E để tạo ảnh minh họa, sau đó tạo file `manifest.json`.
   - 🛑 *HITL Checkpoint*: Tạm dừng chờ người dùng duyệt tài nguyên phân cảnh (`awaiting_assets_approval`).

5. **Bước 5: Video Production (Video Producer Node & Remotion)**
   - Backend thực thi Remotion CLI render video dọc (1080x1920), đồng bộ khớp timeline ảnh/audio voiceover và lồng nhạc nền BGM chéo timeline.

6. **Bước 6: LinkedIn Repurposing (Repurposer Agent)**
   - Tự động biến đổi kịch bản gốc thành 6 định dạng bài đăng LinkedIn độc đáo: *Personal Story, Strong Opinion, Step-by-step, Question Hook, Data & Insight, Failure & Lesson*.

---

## ✅ 3. Chức năng đã được triển khai (Implemented Features)

### 3.1 Về phía Backend & Hợp nhất Dữ liệu
- **Cơ chế HITL Resume thực tế**: Triển khai đầy đủ endpoint `/api/approve` xử lý tiến trình chuyển đổi trạng thái tiếp theo (`topic` -> `script` -> `thumbnail` -> `assets` -> `completed` hoặc `failed` nếu bị từ chối) và lưu vết sự kiện thay đổi vào DB.
- **API giám sát và truy xuất trạng thái**: Triển khai endpoint `/api/status/{task_id}` trả về đầy đủ tiến độ hiện tại, chi tiết lỗi nếu có, và toàn bộ dữ liệu đầu ra của các bước.
- **Hệ thống lưu trữ & Sự kiện Audit**: Thiết kế và hoàn thiện cấu trúc Database (`workflow_runs`, `workflow_events`, `system_logs`) để lưu vết mọi hành động của n8n, Dify và Frontend.
- **Bộ tích hợp YouTube API thực tế**: File [youtube_client.py](file:///d:/HUYTQ/ProdXSolution/Projects/AI-content-agentic-system%20-%20Dify/backend/app/core/youtube_client.py) triển khai đầy đủ khả năng tìm kiếm video theo ngách, thống kê lượt xem và tính toán lượng view trung bình kênh thực tế để lọc chỉ số Outlier.

### 3.2 Về phía Frontend UI
- **Giao diện Giám sát Admin**: Tích hợp các tab Iframe cho phép quản trị viên xem trực tiếp tiến trình n8n, Dify và Remotion Studio song song với bảng giám sát nhật ký lỗi (System Logs).
- **Giao diện Vận hành Workflow trực quan**:
  - Giao diện Dark mode hiện đại với hiệu ứng chuyển trang mượt mà (dùng Framer Motion).
  - Tích hợp tính năng Polling cập nhật trạng thái tự động mỗi 4 giây từ API `/api/status/{task_id}`.
  - Phân nhánh hiển thị các panel nút "Approve" / "Reject" khớp theo từng bước trạng thái của Pipeline.

### 3.3 Về phía Remotion (Video Rendering)
- Triển khai thành công cấu trúc slide động ([ScreenSlide.tsx](file:///d:/HUYTQ/ProdXSolution/Projects/AI-content-agentic-system%20-%20Dify/remotion_app/src/ScreenSlide.tsx)) và cơ chế render phân cảnh ([SceneRenderer.tsx](file:///d:/HUYTQ/ProdXSolution/Projects/AI-content-agentic-system%20-%20Dify/remotion_app/src/SceneRenderer.tsx)).
- Hỗ trợ tính toán thời lượng video tự động dựa trên tổng thời lượng của các file voiceover thô.
- Hỗ trợ phát song song nhạc nền (BGM track) xuyên suốt timeline video.
