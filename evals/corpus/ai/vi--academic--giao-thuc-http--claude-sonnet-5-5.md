---
model: "claude-sonnet-5-5"
genre: "academic"
kind: "academic"
lang: "vi"
prompt: "Viết một bài giải thích khoảng 300 chữ cho sinh viên năm nhất về cách hoạt động của giao thức HTTP."
generated_at: "2026-10-28"
label: "ai"
---

# Cách hoạt động của giao thức HTTP

HTTP (HyperText Transfer Protocol) là giao thức nền tảng của World Wide Web, quy định cách trình duyệt và máy chủ web trao đổi dữ liệu với nhau. Mỗi khi bạn truy cập một trang web, HTTP đứng sau việc đưa nội dung từ máy chủ về thiết bị của bạn.

## Mô hình yêu cầu và phản hồi

HTTP hoạt động theo mô hình client-server. Trình duyệt (client) gửi một yêu cầu (request) đến máy chủ (server), và máy chủ trả về một phản hồi (response). Quá trình này gồm các bước chính sau:

1. **Phân giải tên miền:** Trình duyệt chuyển tên miền như example.com thành địa chỉ IP thông qua hệ thống DNS.
2. **Thiết lập kết nối:** Trình duyệt mở kết nối TCP đến máy chủ, thường qua cổng 80 (HTTP) hoặc 443 (HTTPS).
3. **Gửi yêu cầu:** Trình duyệt gửi thông điệp HTTP gồm phương thức, đường dẫn và các tiêu đề (header).
4. **Nhận phản hồi:** Máy chủ xử lý và trả về mã trạng thái cùng nội dung như HTML, hình ảnh hoặc dữ liệu JSON.

## Các thành phần quan trọng

Phương thức HTTP cho biết hành động mong muốn. GET dùng để lấy dữ liệu, POST dùng để gửi dữ liệu lên máy chủ, PUT để cập nhật và DELETE để xóa. Mã trạng thái cho biết kết quả: 200 nghĩa là thành công, 404 nghĩa là không tìm thấy tài nguyên, và 500 báo lỗi từ phía máy chủ.

## Đặc điểm cần lưu ý

HTTP là giao thức phi trạng thái (stateless), tức mỗi yêu cầu được xử lý độc lập và máy chủ không tự nhớ các yêu cầu trước đó. Để duy trì phiên đăng nhập, các website sử dụng cookie hoặc token. Ngoài ra, HTTP gửi dữ liệu dưới dạng văn bản thuần, vì vậy phiên bản bảo mật HTTPS được sử dụng rộng rãi để mã hóa thông tin trên đường truyền.

## Kết luận

Nắm vững cách HTTP hoạt động là bước đầu tiên để hiểu về lập trình web và mạng máy tính.
