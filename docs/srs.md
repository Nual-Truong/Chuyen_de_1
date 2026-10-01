# BẢN ĐẶC TẢ YÊU CẦU (SRS) RÚT GỌN

## 1. Giới thiệu và phạm vi
* **Bối cảnh:** Mekong Mobile cần một kho dữ liệu tập trung để phân tích doanh thu từ 24 cửa hàng, thay thế việc tổng hợp thủ công từ các file Excel rời rạc.
* **Phạm vi:** Tập trung xây dựng pipeline làm sạch dữ liệu đơn hàng và xây dựng các báo cáo/dashboard phân tích doanh thu, khách hàng, sản phẩm.
* **Ngoài phạm vi (WON'T):** Không xây dựng tính năng dự báo doanh thu bằng Machine Learning; không phân quyền truy cập chi tiết đến từng nhân viên cấp dưới (chỉ cấp quyền xem cho cấp quản lý).
* **Bảng thuật ngữ:**
  * **Kho dữ liệu (Data Warehouse):** Hệ thống lưu trữ dữ liệu đã làm sạch từ các cửa hàng.
  * **Khách hàng quay lại (Retention):** Khách hàng có >= 2 đơn hàng thành công trong các tháng khác nhau.
  * **Doanh thu thuần:** Tổng `thanh_tien` của các đơn hàng hợp lệ, không tính đơn bị hủy.

## 2. Các bên liên quan và vai trò

| Vai trò | Quyền hạn và nghiệp vụ chính |
| :--- | :--- |
| **Giám đốc (Ông Minh)** | Xem toàn bộ báo cáo doanh thu tổng hợp, dashboard so sánh các cửa hàng. |
| **Trưởng phòng Marketing** | Xem báo cáo phân tích hành vi khách hàng, tỉ lệ khách quay lại. |
| **Quản lý sản phẩm** | Xem báo cáo doanh thu theo từng nhóm sản phẩm. |
| **Data Engineer** | Cấu hình pipeline nạp dữ liệu (ETL), theo dõi log lỗi dữ liệu. |

## 3. Yêu cầu chức năng (FR) & User Story
* **US1 (MUST):** Là Giám đốc, tôi muốn xem tổng doanh thu từng cửa hàng theo tháng để đánh giá hiệu quả kinh doanh.
  * *AC1.1:* GIVEN dữ liệu đơn hàng hợp lệ, WHEN Giám đốc chọn bộ lọc tháng/năm, THEN hệ thống hiển thị biểu đồ doanh thu của 24 cửa hàng.
  * *AC1.2 (Ngoại lệ):* GIVEN tháng được chọn chưa có dữ liệu nạp vào kho, WHEN Giám đốc bấm Lọc, THEN hệ thống báo "Chưa có dữ liệu cho kỳ báo cáo này".
* **US2 (MUST):** Là Giám đốc, tôi muốn xác định các cửa hàng có doanh thu giảm 3 tháng liên tiếp để có biện pháp xử lý.
  * *AC2.1:* GIVEN dữ liệu đã cập nhật, WHEN xem dashboard cảnh báo, THEN hệ thống highlight màu đỏ các cửa hàng có doanh thu Tháng(N) < Tháng(N-1) < Tháng(N-2).
* **US3 (MUST):** Là Trưởng phòng Marketing, tôi muốn tính tỉ lệ khách quay lại mua lần hai để đánh giá mức độ trung thành.
  * *AC3.1:* GIVEN tập khách hàng, WHEN xem báo cáo Retention, THEN hiển thị biểu đồ tròn biểu diễn % khách có >= 2 đơn hàng.
* **US4 (SHOULD):** Là Quản lý sản phẩm, tôi muốn phân tích doanh thu theo nhóm sản phẩm để tối ưu danh mục nhập hàng.
* **US5 (SHOULD):** Là Data Engineer, tôi muốn xem danh sách các dòng dữ liệu bị loại (reject) khi nạp vào kho để xử lý lỗi đầu vào.
* **US6 (COULD):** Là Giám đốc, tôi muốn lọc báo cáo doanh thu theo khu vực địa lý (Quận/Huyện).
* **US7 (COULD):** Là Trưởng phòng Marketing, tôi muốn xuất dữ liệu khách hàng quay lại ra file Excel.
* **US8 (WON'T):** Là Giám đốc, tôi muốn dự báo doanh thu tháng tới bằng mô hình AI.

## 4. Yêu cầu phi chức năng (NFR)
* **NFR1 (Hiệu năng):** Dashboard báo cáo doanh thu năm phải tải xong và hiển thị hoàn chỉnh trong dưới 3 giây khi truy vấn trên 100.000 dòng fact sales.
* **NFR2 (Tính sẵn sàng):** Thời gian gián đoạn của kho dữ liệu để chạy ETL cập nhật hàng tháng không được vượt quá 2 giờ (chạy từ 00:00 đến 02:00 sáng ngày mùng 1 hàng tháng).
* **NFR3 (Bảo mật):** 100% số điện thoại khách hàng hiển thị trên dashboard của Quản lý sản phẩm phải được che 4 số cuối (định dạng `0901xxx567`).

## 5. Ràng buộc và quy tắc nghiệp vụ
* **QT_DA_01:** Thành tiền của một dòng đơn hàng bắt buộc phải bằng số lượng nhân với đơn giá (sai lệch cho phép tối đa <= 1 VND).
* **QT_DA_02:** Mã đơn hàng không có tính duy nhất trên toàn hệ thống, khóa định danh duy nhất bắt buộc phải là cụm `(ma_cua_hang + ma_don)`.
* **QT_DA_03:** Các đơn hàng không chuyển đổi được định dạng ngày chuẩn ISO sẽ bị đẩy vào bảng `reject_log`, tuyệt đối không đưa vào báo cáo phân tích.

## 6. Bảng truy vết yêu cầu (Traceability Matrix)

| Mã FR | Yêu cầu chức năng | User Story | Use Case | MoSCoW | Test Case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| FR1 | Hệ thống tổng hợp và trực quan hóa doanh thu từng cửa hàng theo tháng. | US1 | UC2 | MUST | TC01, TC02 |
| FR2 | Hệ thống tự động phát hiện và cảnh báo các cửa hàng giảm doanh thu 3 tháng liên tiếp. | US2 | UC3 | MUST | TC03 |
| FR3 | Hệ thống tính toán tỉ lệ phần trăm khách hàng có mua lại trên hệ thống. | US3 | UC4 | MUST | TC04 |
| FR4 | Phân cụm và tính tổng doanh thu cho từng nhóm sản phẩm theo thời gian. | US4 | UC5 | SHOULD | TC05 |
| FR5 | Ghi log và hiển thị các bản ghi vi phạm quy tắc làm sạch dữ liệu. | US5 | UC1 | SHOULD | TC06 |

---

## 7. Đặc tả Use Case

**Danh sách Use Case**
* **Actor:** Giám đốc (Primary), Data Engineer (Primary), Trưởng phòng Marketing (Primary).
* `UC1`: Nạp và chuẩn hóa dữ liệu bán hàng thô (Data Engineer).
* `UC2`: Tra cứu doanh thu cửa hàng theo kỳ (Giám đốc).
* `UC3`: Theo dõi cảnh báo cửa hàng giảm doanh thu (Giám đốc).
* `UC4`: Phân tích tỉ lệ khách hàng quay lại (Trưởng phòng Marketing).
* `UC5`: Xuất báo cáo dữ liệu phân tích ra Excel (Giám đốc, Marketing).

**Đặc tả Use Case chính: UC2 - TRA CỨU DOANH THU CỬA HÀNG THEO KỲ**
* **Actor chính:** Giám đốc
* **Mục tiêu:** Xem báo cáo tổng hợp doanh thu của toàn bộ 24 cửa hàng trong một tháng/quý cụ thể.
* **Điều kiện trước:** Giám đốc đã đăng nhập; dữ liệu tháng cần xem đã được Data Engineer nạp vào Data Warehouse thành công.
* **Điều kiện sau:** Hiển thị biểu đồ cột so sánh doanh thu và bảng số liệu chi tiết.
* **Luồng chính (Happy Path):**
  1. Giám đốc truy cập vào màn hình "Dashboard Doanh Thu".
  2. Hệ thống hiển thị giao diện báo cáo với các bộ lọc mặc định là tháng hiện tại.
  3. Giám đốc chọn một "Tháng" và "Năm" trong bộ lọc và bấm "Xem báo cáo".
  4. Hệ thống truy vấn dữ liệu từ bảng Fact Sales, nhóm theo `ma_cua_hang`.
  5. Hệ thống render biểu đồ cột so sánh và hiển thị tổng doanh thu.
* **Luồng ngoại lệ:**
  * **3a. Dữ liệu tháng được chọn chưa có trong kho:**
    * Hệ thống kiểm tra thấy truy vấn trả về 0 dòng.
    * Hệ thống hiển thị popup cảnh báo: "Dữ liệu của tháng [X] chưa được cập nhật. Vui lòng liên hệ Data Engineer".
    * Hệ thống giữ nguyên biểu đồ của kỳ báo cáo trước đó.
