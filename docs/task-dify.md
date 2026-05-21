# Danh sách Task: Chuyển đổi Kiến trúc Low-code (Dify.ai + n8n)

- [ ] **Giai đoạn 1: Chuẩn bị Infrastructure**
  - [ ] Sao lưu (Backup) project hiện tại trước khi refactor.
  - [ ] Chỉnh sửa `docker-compose.yml`: Xóa ChromaDB và các service AI cũ.
  - [ ] Thêm Dify docker-compose (`dify-api`, `dify-web`, `weaviate`, `redis`) vào mạng lưới với n8n và BE.
  - [ ] Khởi chạy và kiểm tra truy cập vào Dify, n8n.

- [x] **Giai đoạn 2: Tái cấu trúc Backend & Đẩy Logic AI lên Dify**
  - [x] Tạo Chat/Agent App và Weaviate Knowledge Base trên Dify.
  - [x] Xây dựng Custom Tools (Python/n8n Webhook) nếu cần.
  - [x] Tái cấu trúc thư mục `backend/` FastAPI: Xóa bỏ các file logic AI/RAG/Prompt cũ.
  - [x] Bổ sung / Củng cố các API lưu trữ Log và hoạt động của hệ thống (System Activities) trên Backend FastAPI.

- [x] **Giai đoạn 3: Tái thiết kế Frontend Next.js (Admin Dashboard)**
  - [x] Refactor layout hiện tại thành cấu trúc Admin Dashboard chuẩn.
  - [x] Cấu hình biến môi trường (`DIFY_API_KEY`, url...).
  - [x] Thiết kế trang và tích hợp Dify WebApp vào Dashboard (thông qua iframe / script embedded).
  - [x] Gắn các API calls để lưu Log và giám sát hoạt động trả về cho FastAPI Backend.

- [x] **Giai đoạn 3.1: Hoàn thiện Premium UI (Mockup Approved)**
  - [x] Tạo file mô tả kiến trúc thiết kế `re-design-dify-fe.md`.
  - [x] Cài đặt các thư viện hỗ trợ (lucide-react, framer-motion).
  - [x] Code giao diện Premium Dark Mode với CSS Modules cho Admin Dashboard.
  - [x] Thêm hiệu ứng chuyển động và làm đẹp UI.

- [ ] **Giai đoạn 4: Đóng gói (Templateization)**
  - [ ] Export cấu hình Agent/Workflow từ Dify ra DSL (`.yml`).
  - [ ] Export các luồng automation từ n8n ra `workflow.json`.
