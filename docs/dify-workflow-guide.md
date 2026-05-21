# Hướng dẫn thiết lập chi tiết Multi-Agent Workflow trên Dify

Tài liệu này cung cấp hướng dẫn từng bước để thiết lập và cấu hình hệ thống Multi-Agent Workflow **Content-Machine-Brain** trên giao diện kéo thả trực quan của **Dify**, dựa theo cấu trúc tệp DSL [dify_agent_dsl.yml](file:///d:/HUYTQ/ProdXSolution/Projects/AI-content-agentic-system%20-%20Dify/dify_n8n/dify_agent_dsl.yml) của hệ thống.

---

## 🏗️ 1. Chọn loại ứng dụng và thiết lập ban đầu

1. **Truy cập Dify**: Đăng nhập vào trang quản trị Dify Studio cục bộ hoặc đám mây của bạn.
2. **Tạo ứng dụng mới**:
   - Nhấp vào **"Create from Blank"** (Tạo mới từ trang trắng).
   - Chọn **App Mode** (Chế độ ứng dụng) là **Workflow** (Luồng công việc). *Lưu ý: Không chọn Chatflow hay Agent vì Workflow giúp kiểm soát luồng dữ liệu chính xác theo dạng sơ đồ tuần tự.*
   - Đặt tên ứng dụng: `Content-Machine-Brain`.
   - Nhập mô tả: `Dify workflow template for Content Machine: Script -> Thumbnail Brief -> LinkedIn Repurpose`.
   - Chọn một icon đại diện và màu nền phù hợp, sau đó bấm **"Create"**.

---

## 📥 2. Bước 1: Cấu hình Node Khởi Đầu (Start Node)

Node này chịu trách nhiệm nhận các dữ liệu đầu vào được truyền từ n8n hoặc API Gateway.

1. Bấm vào Node **Start** mặc định trên khung vẽ.
2. Tại khu vực cấu hình Input Variables (Biến đầu vào), thêm 4 biến sau:

| Tên Biến (`Variable Name`) | Tên hiển thị (`Label`) | Loại (`Type`) | Trạng thái (`Required`) | Mô tả |
| :--- | :--- | :--- | :--- | :--- |
| `niche` | Niche | `text-input` (Dòng đơn) | **Bắt buộc** | Ngách nội dung (Ví dụ: "AI Automation") |
| `selected_title` | Selected Title | `text-input` (Dòng đơn) | **Bắt buộc** | Tiêu đề hoặc góc tiếp cận đã được duyệt |
| `language` | Language | `text-input` (Dòng đơn) | Không bắt buộc | Ngôn ngữ viết kịch bản (mặc định: `en` hoặc `vi`) |
| `reference_thumbnail_url` | Reference Thumbnail URL | `text-input` (Dòng đơn) | Không bắt buộc | Đường dẫn ảnh thu nhỏ của video gốc để phân tích |

---

## ✍️ 3. Bước 2: Thiết lập Scriptwriter Agent (LLM Node)

Node này đóng vai trò là Agent biên kịch, chuyển đổi chủ đề thành một kịch bản hấp dẫn dạng cấu trúc dọc.

1. Rê chuột vào cổng đầu ra của Node **Start**, kéo ra và chọn thêm Node **LLM**.
2. Đổi tên Node LLM này thành `Scriptwriter Agent`.
3. **Cấu hình Model**:
   - **Provider**: Chọn nhà cung cấp mô hình mong muốn (ví dụ: `OpenAI` hoặc `Anthropic`).
   - **Model Name**: Chọn mô hình mạnh về viết lách và tối ưu chi phí (Khuyên dùng: `gpt-4o-mini` hoặc `claude-3-5-sonnet` nếu cần văn phong xuất sắc).
   - **Temperature**: Thiết lập ở mức `0.6` (đảm bảo sự cân bằng giữa tính sáng tạo và việc tuân thủ cấu trúc).
   - **Max Tokens**: `2500` (đủ dung lượng cho một kịch bản chi tiết).
4. **Cấu hình Prompt hệ thống (System Prompt)**:
   Copy đoạn Prompt chuẩn hóa định dạng JSON sau vào khung **SYSTEM**:

```text
You are the Scriptwriter Agent for short-form vertical video.
Create a script with this required hook structure:
1) Identify pain
2) Missed opportunity
3) Outcome
4) Visual preview

Return strict JSON only:
{
  "agent": "scriptwriter",
  "step": "script_writing",
  "topic": "{{selected_title}}",
  "estimated_duration_seconds": 60,
  "script": {
    "hook": {
      "identify": "...",
      "missed_opportunity": "...",
      "outcome": "...",
      "visual_preview": "[VISUAL: ...]"
    },
    "credibility": "...",
    "main_content": [
      {
        "point_number": 1,
        "title": "...",
        "explanation": "...",
        "example": "...",
        "takeaway": "..."
      }
    ],
    "cta": "...",
    "full_script_text": "..."
  }
}
```

5. **Cấu hình nội dung người dùng (User Prompt)**:
   Thiết lập các biến tham chiếu từ Node **Start** bằng cách dùng cú pháp `{{biến}}` trong khung **USER**:
```text
Niche: {{sys.query.niche}}
Title: {{sys.query.selected_title}}
Language: {{sys.query.language}}
```
*(Trong Dify trực quan, bạn chỉ cần gõ `{{` hệ thống sẽ hiển thị danh sách biến từ Node Start để bạn bấm chọn).*

---

## 🎨 4. Bước 3: Thiết lập Visual Director Agent (LLM Node)

Agent này đảm nhận phân tích kịch bản và đưa ra chỉ thị thiết kế ảnh thu nhỏ (Thumbnail Brief).

1. Kéo từ cổng đầu ra của Node `Scriptwriter Agent`, chọn thêm Node **LLM**.
2. Đổi tên Node thành `Visual Director Agent`.
3. **Cấu hình Model**:
   - **Model Name**: Khuyên dùng mô hình mạnh về suy luận hình ảnh trực quan như `gpt-4o`.
   - **Temperature**: `0.4` (cần độ chính xác cao, hạn chế LLM tự suy diễn xa rời kịch bản).
   - **Max Tokens**: `1800`.
4. **Cấu hình SYSTEM Prompt**:
   Copy đoạn cấu hình định hình phong cách trực quan sau:

```text
You are the Visual Director Agent.
Produce a non-copycat thumbnail brief from the script.
Text overlay must be <= 5 words.

Return strict JSON only:
{
  "agent": "visual_director",
  "step": "thumbnail_brief",
  "pattern_summary": "...",
  "brief": {
    "concept": "...",
    "background": {"type": "...", "color_hex": "#..."},
    "color_palette": {"primary": "#...", "accent": "#...", "text": "#..."},
    "text_overlay": {"main_text": "...", "placement": "..."},
    "person": {"include": true, "expression": "...", "gesture": "..."},
    "emotion_target": "...",
    "avoid": ["...", "..."]
  }
}
```

5. **Cấu hình USER Prompt**:
   Tham chiếu kịch bản đã tạo ở bước trước:
```text
Script JSON:
{{scriptwriter.text}}

Reference thumbnail URL:
{{sys.query.reference_thumbnail_url}}
```

---

## 🔄 5. Bước 4: Thiết lập Repurposer Agent (LLM Node)

Agent này tự động chuyển đổi kịch bản video thành các bài viết sâu sắc cho mạng xã hội LinkedIn.

1. Kéo từ cổng đầu ra của Node `Visual Director Agent`, chọn thêm Node **LLM**.
2. Đổi tên Node thành `Repurposer Agent`.
3. **Cấu hình Model**:
   - **Model Name**: `gpt-4o-mini`.
   - **Temperature**: `0.7` (khuyến khích lối viết tự nhiên, phong phú).
   - **Max Tokens**: `2500`.
4. **Cấu hình SYSTEM Prompt**:
   Đảm bảo LLM phân tách bài đăng thành 6 định dạng bài viết chuẩn mực trên LinkedIn:

```text
You are the Repurposer Agent.
Convert the source script into 6 LinkedIn post formats.

Return strict JSON only:
{
  "agent": "repurposer",
  "step": "linkedin_repurposing",
  "source_topic": "...",
  "posts": {
    "personal_story": "...",
    "strong_opinion": "...",
    "step_by_step": "...",
    "question_hook": "...",
    "data_insight": "...",
    "failure_lesson": "..."
  }
}
```

5. **Cấu hình USER Prompt**:
```text
Script JSON:
{{scriptwriter.text}}
```

---

## 📤 6. Bước 5: Cấu hình Node Kết Thúc (End Node)

Node này đóng gói tất cả các tài liệu đã tạo để gửi trả lại cho n8n và Backend API Gateway.

1. Kéo từ cổng đầu ra của `Repurposer Agent`, thêm Node **End** (Kết thúc).
2. Tại danh sách biến đầu ra (Outputs), tạo 3 biến đầu ra tương ứng:

| Tên Biến Đầu Ra | Nguồn Biến (Variable Selector) |
| :--- | :--- |
| `script_result` | Chọn đầu ra `text` từ Node `Scriptwriter Agent` |
| `thumbnail_brief` | Chọn đầu ra `text` từ Node `Visual Director Agent` |
| `linkedin_posts` | Chọn đầu ra `text` từ Node `Repurposer Agent` |

---

## 💡 7. Các lưu ý quan trọng khi vận hành trên Dify

### 7.1 Đảm bảo đầu ra là JSON sạch
Vì các Node LLM trên được yêu cầu trả về định dạng `strict JSON only`, đôi khi các mô hình có thể vô tình kẹp thêm thẻ markdown ```json ... ``` làm hỏng việc phân tích cú pháp ở Backend.
*   **Giải pháp**: Trong cài đặt nâng cao của từng Node LLM trên Dify, hãy kích hoạt tùy chọn **JSON Mode** nếu mô hình của bạn hỗ trợ (như GPT-4o). Điều này bắt buộc mô hình phải trả ra JSON hợp lệ.

### 7.2 Cách nhập trực tiếp qua tệp DSL (Cách nhanh nhất)
Nếu bạn không muốn kéo thả thủ công từng Node, Dify cho phép nhập trực tiếp cấu trúc luồng bằng mã DSL:
1. Trên giao diện Dify Studio, tạo một ứng dụng Workflow mới trống.
2. Tìm nút góc trên bên phải (thường là biểu tượng ba dấu chấm `...` hoặc menu cấu hình) và chọn **"Import DSL"** (Nhập DSL).
3. Tải lên hoặc dán nội dung tệp [dify_agent_dsl.yml](file:///d:/HUYTQ/ProdXSolution/Projects/AI-content-agentic-system%20-%20Dify/dify_n8n/dify_agent_dsl.yml). Toàn bộ sơ đồ luồng sẽ tự động xuất hiện hoàn chỉnh với tất cả các thông số cấu hình đã định sẵn.
