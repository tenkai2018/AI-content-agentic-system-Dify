# Hướng dẫn Triển khai & Cấu hình Dify và n8n Templates

Thư mục này chứa các file cấu hình mẫu giúp đóng gói toàn bộ logic xử lý AI và tự động hóa ngoại vi cho hệ thống **AI Content Agentic System**. Bằng cách import các file mẫu này, bạn có thể thiết lập nhanh chóng môi trường production hoặc white-label cho khách hàng mới mà không cần code lại.

---

## 📂 Danh sách Files

1. **`dify_agent_dsl.yml`**: File định nghĩa cấu hình ứng dụng AI (DSL) của Dify. Chứa toàn bộ prompt system, các tác nhân (Scriptwriter, Visual Director, Repurposer, SEO, Newsletter, Analyst) và schema đầu ra chuẩn hóa.
2. **`n8n_workflow.json`**: File chứa toàn bộ quy trình tự động hóa của n8n, bao gồm quét YouTube API, tính Outlier Score, gọi log FastAPI Backend và trigger Dify.

---

## 🤖 1. Hướng dẫn Import & Cấu hình Dify (Brain)

### Bước 1: Import DSL
1. Truy cập vào giao diện quản trị Dify (Mặc định chạy ở cổng `80` hoặc `http://localhost` qua Docker Compose).
2. Tại màn hình **Studio**, nhấn nút **Create from DSL file** (Tạo từ file DSL) ở góc trên bên phải.
3. Chọn file [dify_agent_dsl.yml](file:///d:/HUYTQ/ProdXSolution/Projects/AI-content-agentic-system%20-%20Dify/dify_n8n/dify_agent_dsl.yml) từ thiết bị của bạn.
4. Đặt tên ứng dụng (ví dụ: `AI Content Machine Brain`) và hoàn tất import.

### Bước 2: Cấu hình Model & API Key
1. Đi tới góc phải màn hình, chọn **Settings** -> **Model Provider**.
2. Thiết lập API Key cho các nhà cung cấp mô hình tương ứng:
   - **OpenAI**: Để sử dụng mô hình `gpt-4o` (cho Visual Director) và `gpt-4o-mini` (cho các tác nhân phụ).
   - **Anthropic (Tùy chọn)**: Để sử dụng mô hình `claude-3-5-sonnet` cho chất lượng bài viết tự nhiên nhất.
3. Lưu cấu hình.

### Bước 3: Lấy API Key của Workflow
1. Trong giao diện Workflow Dify vừa import, click vào mục **API Access** ở menu sidebar bên trái.
2. Nhấn **API Key** -> **Generate New API Key**.
3. Copy API Key này để điền vào cấu hình n8n ở phần tiếp theo.

---

## ⚡ 2. Hướng dẫn Import & Cấu hình n8n (Execution)

### Bước 1: Import Workflow
1. Truy cập vào n8n WebUI (Mặc định chạy ở cổng `5678` hoặc `http://localhost:5678`).
2. Vào mục **Workflows** -> Chọn **Add Workflow** (hoặc tạo một workflow trống mới).
3. Click vào dấu ba chấm `...` ở góc trên bên phải màn hình -> Chọn **Import từ File** (Import from File).
4. Chọn file [n8n_workflow.json](file:///d:/HUYTQ/ProdXSolution/Projects/AI-content-agentic-system%20-%20Dify/dify_n8n/n8n_workflow.json).

### Bước 2: Thiết lập thông tin xác thực (Credentials)
Workflow n8n cần kết nối đến YouTube API và Dify API:

1. **YouTube API Key**:
   - Mở node **YouTube Search** hoặc cấu hình biến môi trường toàn cục trong Docker của n8n với key `YOUTUBE_API_KEY`.
   - Hoặc bạn có thể điền trực tiếp key API YouTube (tạo trên Google Cloud Console) vào trường dữ liệu `key` ở mục Query Parameters của node **YouTube Search** và **Get Video Details**.

2. **Dify API Token**:
   - Double-click vào node **Trigger Dify Workflow**.
   - Tại mục **Credential for HTTP Header Auth**, nhấn **Create New Credential**.
   - Thiết lập header:
     - **Name**: `Authorization`
     - **Value**: `Bearer <YOUR_DIFY_WORKFLOW_API_KEY>` (Thay thế bằng key bạn lấy ở Bước 3 phần Dify).

### Bước 3: Kích hoạt Workflow
1. Nhấn nút **Save** ở góc trên bên phải.
2. Bật công tắc **Active** (ở góc phải) để workflow bắt đầu lắng nghe các sự kiện Webhook từ Dashboard Frontend hoặc chạy theo chu kỳ.

---

## ⚙️ 3. Kiểm tra tích hợp (Integration Verification)

Để đảm bảo hệ thống low-code của bạn hoạt động chính xác:
1. Đảm bảo FastAPI Backend đang hoạt động tại cổng `8080` (để nhận Logs).
2. Gửi một request POST thử nghiệm tới Webhook n8n (lấy URL webhook ở node Webhook Trigger, ví dụ: `http://localhost:5678/webhook/content-pipeline`):
   ```bash
   curl -X POST http://localhost:5678/webhook/content-pipeline \
     -H "Content-Type: application/json" \
     -d '{"niche": "AI Agent", "keywords": "low-code"}'
   ```
3. Xem tab **Monitoring (System Logs)** trên giao diện Admin Dashboard (Next.js) để xem các log sự kiện từ n8n và Dify được cập nhật thời gian thực qua FastAPI `/api/logs`.
