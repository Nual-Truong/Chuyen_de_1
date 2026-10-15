# Nhật ký thay đổi thiết kế
## Sau phản hồi Bài tập 1

### TD-01 Bổ sung bảng chú thích ký hiệu cho các sơ đồ
- **Phản hồi của GV:** Sơ đồ Use Case, kiến trúc và star schema đều thiếu chú thích ký hiệu.
- **Quyết định:** SỬA.
- **Lý do:** Khắc phục thiếu sót trong quá trình xuất sơ đồ để đảm bảo nguyên tắc "đọc được độc lập mà không cần giải thích thêm".
- **Ảnh hưởng:** Cập nhật lại toàn bộ file `usecase.drawio`, `architecture.drawio` và `erd.drawio` để chèn thêm Legend (Bảng chú thích).

### TD-02 Đồng bộ mã Use Case và Bảng truy vết
- **Phản hồi của GV:** Mã UC trên sơ đồ không khớp SRS. UC2 không có trên sơ đồ. Bảng truy vết thiếu US6, US7.
- **Quyết định:** SỬA.
- **Lý do:** Lỗi bất nhất do chỉnh sửa file văn bản ở phút chót nhưng chưa cập nhật lại file vẽ và bảng truy vết.
- **Ảnh hưởng:** Vẽ lại `usecase.drawio` cho khớp với danh sách UC trong `srs.md`. Bổ sung US6, US7 vào Bảng truy vết.

### TD-03 Bổ sung dim_customer và mô tả cột vào mô hình dữ liệu
- **Phản hồi của GV:** Star schema thiếu mô tả từng cột. Thiếu bảng `dim_customer` trên lược đồ và `customer_key` trong `fact_sales` dẫn đến không tính được Retention.
- **Quyết định:** SỬA.
- **Lý do:** Bảng `dim_customer` là thành phần bắt buộc để gom nhóm dữ liệu khách hàng phục vụ US3 (Phân tích khách quay lại). Cần có mô tả cột để đóng vai trò như Data Dictionary cho Data Engineer.
- **Ảnh hưởng:** Cập nhật lại file `erd.drawio`, bổ sung bảng `dim_customer`, thêm khóa ngoại vào bảng Fact và ghi chú ý nghĩa từng cột.

### TD-04 Chỉnh sửa lỗi trình bày trong SRS
- **Phản hồi của GV:** Luồng chính UC2 chưa đánh số; NFR03 ghi che 4 số cuối nhưng ví dụ che 3 số giữa.
- **Quyết định:** SỬA.
- **Lý do:** Sửa lỗi đánh máy và định dạng văn bản để đảm bảo tính logic.
- **Ảnh hưởng:** Chỉnh sửa trực tiếp tại mục 2 và mục 4 của file `srs.md`.
