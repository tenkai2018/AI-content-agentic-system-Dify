# Re-design Dify Frontend (Admin Dashboard)

Tài liệu này mô tả chi tiết chức năng, cấu trúc công nghệ và thiết kế giao diện (UI/UX) của ứng dụng Frontend Next.js sau quá trình đập đi xây lại sang cấu trúc Low-code (sử dụng Dify và n8n).

## 1. Mô tả Chức năng (Features)

Hệ thống Frontend không còn đóng vai trò xử lý logic AI trực tiếp mà chuyển sang vai trò **"Bảng điều khiển Trung tâm" (Admin Dashboard)**. Các chức năng cốt lõi bao gồm:

- **AI Agents (Dify):** Môi trường để tương tác và cấu hình các AI Agents. Nhúng trực tiếp giao diện WebApp của Dify.
- **Automations (n8n):** Môi trường tạo và giám sát các luồng tự động hoá (workflows). Nhúng trực tiếp giao diện của n8n.
- **Video Render (Remotion):** Môi trường để xem trước và tinh chỉnh template video bằng Remotion.
- **System Logs:** Khu vực theo dõi trạng thái hệ thống, hiển thị real-time các bản ghi hoạt động và cảnh báo lỗi từ Backend FastAPI.

## 2. Công nghệ sử dụng (Tech Stack)

- **Framework:** Next.js 16 (App Router)
- **Language:** TypeScript
- **Styling:** CSS Modules (với biến CSS tùy chỉnh)
- **Icons:** Lucide React
- **Animations:** Framer Motion (hiệu ứng mượt mà, chuyển trang)
- **Integration:** Iframe nhúng các dịch vụ (Dify, n8n, Remotion), Fetch API gọi Backend.

## 3. Thiết kế (UI/UX Design)

### Phong cách (Aesthetic)
- **Dark Mode Cao cấp:** Lấy cảm hứng từ giao diện Vercel, Linear, với nền màu đen/xanh thẫm (`#0A0F1C`).
- **Glassmorphism:** Sử dụng hiệu ứng kính mờ cho các thành phần nổi (Bảng điều khiển, thẻ số liệu) với viền mỏng (`1px solid rgba(255, 255, 255, 0.08)`).
- **Màu Nhấn (Accent):** Tím neon và Xanh lam để tạo cảm giác "AI" và hiện đại.

### Cấu trúc Trang (Layout)
1. **Sidebar (Trái - 260px):**
   - Chứa Logo dự án với chữ gradient.
   - Các nút điều hướng (Tabs) giữa các chức năng, sử dụng Icon Lucide. Nút đang kích hoạt có hiệu ứng sáng nền và thay đổi màu chữ.
2. **Main Content (Phải):**
   - **Header:** Tên của phân hệ đang mở (ví dụ: "AI Agents").
   - **Metrics Area (Nếu có):** Hiển thị số liệu tóm tắt (Tổng số log, Trạng thái API...).
   - **Iframe/Data Container:** Box rộng bo góc tròn (border-radius: 16px) chứa iframe Dify/n8n/Remotion hoặc Bảng Log. Bảng Log thiết kế gọn gàng, có màu sắc phân loại mức độ (INFO, WARNING, ERROR).

## 4. Cấu hình Môi trường (Environment)

- `NEXT_PUBLIC_API_URL`: URL của Backend FastAPI (Mặc định: http://localhost:8080)
- `NEXT_PUBLIC_DIFY_APP_URL`: URL của Dify Web (Mặc định: http://localhost)
- `NEXT_PUBLIC_N8N_URL`: URL của n8n (Mặc định: http://localhost:5678)
- `NEXT_PUBLIC_REMOTION_URL`: URL của Remotion (Mặc định: http://localhost:3001)
