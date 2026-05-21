# Kiến trúc & Kế hoạch Refactor - Con đường 2: Tối ưu Low-code (Sử dụng Dify.ai)

Tài liệu này mô tả chi tiết việc chuyển đổi kiến trúc hệ thống sang hướng **Low-code**, tận dụng sức mạnh của nền tảng **Dify.ai** để đóng vai trò "Não bộ" (AI Logic, RAG, Prompt Management) kết hợp với **n8n** để làm "Chân tay" (Tự động hóa workflow ngoại vi). 

Đây là con đường được khuyến nghị cao nhất cho một **One-Man-Business** vì nó giúp giảm thiểu đến 80% lượng code phải bảo trì.

## 1. Tổng quan Kiến trúc Tech Stack Mới

- **Frontend:** Next.js (Chỉ đóng vai trò làm UI, hiển thị kết quả hoặc Dashboard).
- **AI Backend / Orchestration (Lõi thay đổi):** **Dify.ai**. Đảm nhận toàn bộ phần Prompt Engineering, Agent logic, RAG (Retrieval-Augmented Generation), và Vector Search.
- **Database (Cho Dify & n8n):** PostgreSQL.
- **Vector Database:** PostgreSQL (pgvector) hoặc Weaviate/Milvus (tích hợp sẵn trong Dify).
- **Workflow Automation:** n8n (Xử lý HTTP requests, Cron jobs, đẩy bài lên MXH).
- **Backend API (Tùy chọn):** FastAPI (Chỉ giữ lại nếu bạn có những logic xử lý dữ liệu phức tạp không thể làm trên Dify/n8n. Đa số trường hợp có thể **xóa bỏ hoàn toàn** phần này).

---

## 2. Các thay đổi cực lớn đối với Source Code

Kiến trúc này đòi hỏi bạn phải "mạnh tay" gỡ bỏ mã nguồn cũ và chuyển logic lên nền tảng mới.

### 2.1. Cập nhật Infrastructure (`docker-compose.yml`)

Bạn cần thêm các service của Dify vào Docker Compose và cấu hình lại.

```diff
# Gỡ bỏ các service không còn cần thiết
- chromadb:
-   image: chromadb/chroma:latest
-   ...

# Thêm Dify.ai services (Dify thường có file docker-compose riêng khá lớn)
# Bạn có thể merge nó với file hiện tại hoặc chạy song song 2 cụm docker.
+ api:
+   image: langgenius/dify-api:latest
+ web:
+   image: langgenius/dify-web:latest
+ weaviate: (hoặc pgvector)
+ redis:
```

> [!TIP]
> Dify.ai cung cấp sẵn một kho lưu trữ `docker-compose`. Cách tốt nhất là clone repo của Dify, cấu hình chạy Dify trên port 80, và để n8n chạy trên port 5678 trong cùng một mạng lưới (Docker Network) để chúng dễ dàng gọi API của nhau.

### 2.2. "Khai tử" (hoặc thu nhỏ) Backend FastAPI

Với kiến trúc cũ, `backend/` chứa toàn bộ logic LangGraph. Với Dify, bạn sẽ chuyển các luồng này lên giao diện trực quan.

**Thay đổi:**
- **Prompt & Agent Logic:** Thay vì viết code Python khai báo LLM, khai báo System Prompt, bạn sẽ vào giao diện Dify, tạo một `Chat App` hoặc `Agent App` và gõ Prompt trực tiếp trên đó.
- **RAG (Knowledge Base):** Thay vì tự code chức năng cắt text (chunking), nhúng (embedding), và đưa vào ChromaDB bằng Python, bạn chỉ cần nộp file PDF/TXT/URL lên giao diện Knowledge của Dify. Dify sẽ tự động vectorize và quản lý chúng.
- **Custom Tools:** Nếu Agent cần một tool đặc biệt (ví dụ: cào dữ liệu báo chí), bạn viết tool đó bằng Python trong Dify, hoặc dùng n8n tạo Webhook và cho Agent trên Dify gọi Webhook của n8n.

Hành động trên mã nguồn: **Có thể xóa bỏ toàn bộ thư mục `backend/` nếu không còn logic nghiệp vụ đặc thù nào khác.**

### 2.3. Tái cấu trúc Frontend (Next.js)

Giao diện Next.js của bạn giờ đây không còn gọi API vào `http://localhost:8000` (FastAPI) nữa, mà sẽ gọi trực tiếp vào API của Dify.

**Ví dụ logic gọi API mới trên Frontend:**
```javascript
// frontend/src/services/aiService.ts
export const generateContent = async (topic: string) => {
  const response = await fetch('http://dify-api:5001/v1/chat-messages', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.DIFY_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      inputs: { topic: topic },
      query: "Hãy viết bài cho tôi",
      user: "user-123"
    }),
  });
  return response.json();
};
```

---

## 3. Chiến lược Đóng gói thành Template (Siêu tốc độ)

Con đường số 2 biến việc nhân bản (white-labeling) cho khách hàng/nghiệp vụ khác trở nên cực kỳ dễ dàng, thậm chí không cần chạm vào code:

1. **Nhân bản "Não bộ" AI:**
   Trong Dify.ai, mỗi Agent hoặc Workflow đều có tính năng **Export DSL**. Hệ thống sẽ xuất ra một file định dạng `.yml`.
   - **Tạo Template:** Bạn có 1 file `real_estate_agent.yml` cho ngành Bất động sản, `marketing_agent.yml` cho ngành Marketing.
   - **Triển khai:** Chỉ cần Import file `.yml` này vào Dify của khách hàng mới là họ có ngay cấu hình Agent chuẩn xác mà bạn đã thiết kế.

2. **Nhân bản "Chân tay" n8n:**
   Tương tự Dify, n8n cũng hỗ trợ Export toàn bộ Workflow ra file `JSON`.
   - Để triển khai, bạn chỉ cần import `workflow.json` và yêu cầu khách hàng kết nối lại các thông tin xác thực (Ví dụ: Đăng nhập lại tài khoản Facebook, WordPress của họ).

3. **Giao diện (Frontend):**
   Bạn thậm chí có thể **không cần Frontend Next.js**. Dify.ai cung cấp tính năng **WebApp**. Dify sẽ tự sinh ra một trang web giao diện chat/tạo form cực kỳ đẹp mắt, cho phép đổi Logo, đổi màu sắc thương hiệu.
   - Nếu khách hàng chỉ cần dùng nội bộ: Đưa họ dùng WebApp tích hợp sẵn của Dify.
   - Nếu cần tích hợp vào website có sẵn của khách hàng: Dify cung cấp đoạn mã `<iframe>` hoặc Script để nhúng thẳng cửa sổ Chat/Agent vào trang web WordPress/React bất kỳ.

> [!IMPORTANT]
> **Tổng kết:** Việc chọn Con đường 2 đòi hỏi bạn phải từ bỏ thói quen tự code mọi thứ. Đổi lại, bạn có một hệ thống cực kỳ dễ nâng cấp, bảo trì bằng giao diện, và tốc độ tạo ra Template để bán/triển khai cho nghiệp vụ mới sẽ giảm từ **vài tuần xuống chỉ còn vài giờ**.
