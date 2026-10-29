---
model: "gpt-oss-120b-medium"
genre: "academic"
kind: "academic"
lang: "vi"
prompt: "Viết một bài giải thích khoảng 300 chữ cho sinh viên năm nhất về thuật toán sắp xếp nổi bọt."
generated_at: "2026-10-29"
label: "ai"
---

**Thuật toán sắp xếp nổi bọt (Bubble Sort)**  

Thuật toán bắt đầu bằng việc duyệt lần lượt các phần tử trong mảng từ đầu tới cuối. Ở mỗi bước, nó so sánh cặp phần tử liền kề; nếu phần tử bên trái lớn hơn phần tử bên phải, hai phần tử sẽ được hoán đổi vị trí. Nhờ đó, "bong bóng" (phần tử lớn nhất) sẽ “nổi” lên cuối mảng sau mỗi lượt duyệt.  

Quá trình này được lặp lại bao nhiêu lần tùy vào độ dài mảng: sau mỗi lượt, phần tử cuối cùng đã được sắp xếp, nên lượt tiếp theo chỉ cần xét đến phần tử trước đó. Thuật toán dừng khi một lượt duyệt không thực hiện bất kỳ hoán đổi nào, nghĩa là mảng đã ở trạng thái sắp xếp.  

Độ phức tạp thời gian của Bubble Sort là O(n²) trong trường hợp tệ nhất (khi mảng được sắp xếp ngược) và O(n) trong trường hợp tốt nhất (mảng đã sắp xếp). Vì vậy, mặc dù dễ hiểu và triển khai, Bubble Sort thường không được dùng cho các bộ dữ liệu lớn; các thuật toán nhanh hơn như Quick Sort hay Merge Sort thường được ưu tiên.
