# BẢN ĐẶC TẢ YÊU CẦU PHẦN MỀM (SRS) - RÚT GỌN
**Học phần:** Chuyên đề tốt nghiệp 1
**Dự án:** Smart CRM - Mekong Mobile 
**Track:** Data Analytics (DA) - Luồng phân tích dữ liệu bán hàng
**Sinh viên thực hiện:** Phạm Trường Luân (MSSV: 2374802010296)

---

## 1. Giới thiệu và phạm vi
* **Bối cảnh:** Mekong Mobile là chuỗi bán lẻ thiết bị di động với 24 cửa hàng. Hiện tại, dữ liệu bán hàng đang bị phân mảnh ở nhiều file CSV, khiến Ban Giám đốc gặp khó khăn trong việc theo dõi doanh thu tổng thể và đánh giá độ trung thành của khách hàng.
* **Luồng nghiệp vụ lựa chọn:** Xây dựng Kho dữ liệu (Data Warehouse) bán hàng và thiết kế Dashboard phân tích doanh thu, tập trung vào việc tính toán tổng doanh thu, cảnh báo suy giảm và phân tích tỉ lệ khách quay lại (Retention).
* **Ngoài phạm vi (WON'T):** 
  * Dự báo doanh thu bằng mô hình AI.
  * Cập nhật dữ liệu theo thời gian thực (Real-time streaming).
* **Bảng thuật ngữ:**
  * **Cửa hàng:** Chi nhánh bán lẻ vật lý của Mekong Mobile.
  * **Sản phẩm:** Điện thoại, máy tính bảng hoặc phụ kiện bán tại cửa hàng.
  * **Thành tiền:** Doanh thu thực tế của một dòng sản phẩm trong đơn hàng (đã trừ khuyến mãi nếu có).
  * **Khách hàng:** Người mua hàng, được định danh duy nhất thông qua số điện thoại.

## 2. Các bên liên quan và vai trò
* **Giám đốc:** Người dùng cuối (End-user) quan trọng nhất. Sử dụng Dashboard để xem tổng doanh thu, theo dõi tình hình kinh doanh của các cửa hàng và xem các cảnh báo giảm doanh thu. Không có quyền can thiệp vào quy trình nạp dữ liệu.
* **Trưởng phòng Marketing:** Người dùng khai thác dữ liệu để phân tích độ trung thành của khách hàng (Retention) và hiệu quả của các nhóm sản phẩm. 
* **Data Engineer:** Quản trị viên hệ thống. Chịu trách nhiệm thiết kế luồng ETL, theo dõi quá trình nạp dữ liệu (batch) hàng ngày và xử lý các dòng dữ liệu bị loại (reject log).

## 3. Yêu cầu chức năng (FR) & User Story
* **FR01:** Hệ thống phải cung cấp báo cáo tổng doanh thu theo từng cửa hàng lọc theo tháng/năm.
* **FR02:** Hệ thống phải tự động highlight cảnh báo các cửa hàng có doanh thu giảm liên tiếp trong 3 tháng.
* **FR03:** Hệ thống phải tính toán và hiển thị tỉ lệ phần trăm khách hàng mua từ 2 đơn hàng trở lên (Retention rate).
* **FR04:** Hệ thống phải cho phép phân tích doanh thu chi tiết theo từng nhóm sản phẩm.
* **FR05:** Hệ thống phải ghi nhận và báo cáo các dòng dữ liệu bị lỗi định dạng trong quá trình ETL (reject log).

**Danh sách User Story:**
* **US1 (MUST):** Là Giám đốc, tôi muốn xem tổng doanh thu từng cửa hàng theo tháng để đánh giá hiệu quả kinh doanh.
  * *AC1.1:* GIVEN dữ liệu đơn hàng hợp lệ, WHEN Giám đốc chọn bộ lọc tháng/năm, THEN hệ thống hiển thị biểu đồ doanh thu của 24 cửa hàng.
  * *AC1.2 (Ngoại lệ):* GIVEN tháng được chọn chưa có dữ liệu nạp vào kho, WHEN Giám đốc bấm Lọc, THEN hệ thống báo "Chưa có dữ liệu cho kỳ báo cáo này".
* **US2 (MUST):** Là Giám đốc, tôi muốn xác định các cửa hàng có doanh thu giảm 3 tháng liên tiếp để có biện pháp xử lý.
  * *AC2.1:* GIVEN dữ liệu đã cập nhật, WHEN xem dashboard cảnh báo, THEN hệ thống highlight màu đỏ các cửa hàng có doanh thu Tháng(N) < Tháng(N-1) < Tháng(N-2).
  * *AC2.2 (Ngoại lệ):* GIVEN cửa hàng mới mở chưa đủ 3 tháng dữ liệu, WHEN xem dashboard cảnh báo, THEN hệ thống ẩn cửa hàng này khỏi danh sách cảnh báo.
* **US3 (MUST):** Là Trưởng phòng Marketing, tôi muốn tính tỉ lệ khách quay lại mua lần hai để đánh giá mức độ trung thành.
  * *AC3.1:* GIVEN tập khách hàng hợp lệ, WHEN xem báo cáo Retention, THEN hiển thị biểu đồ tròn biểu diễn % khách có >= 2 đơn hàng.
  * *AC3.2 (Ngoại lệ):* GIVEN các đơn hàng không thu thập được số điện thoại chuẩn, WHEN hệ thống tính toán, THEN hệ thống tự động loại bỏ các đơn này khỏi mẫu số chung để đảm bảo tỉ lệ chính xác.
* **US4 (SHOULD):** Là Trưởng phòng Marketing, tôi muốn phân tích doanh thu theo nhóm sản phẩm để tối ưu danh mục nhập hàng.
* **US5 (SHOULD):** Là Data Engineer, tôi muốn xem danh sách các dòng dữ liệu bị loại (reject) khi nạp vào kho để xử lý lỗi đầu vào.
* **US6 (COULD):** Là Giám đốc, tôi muốn lọc báo cáo doanh thu theo khu vực địa lý (Quận/Huyện).
* **US7 (COULD):** Là Trưởng phòng Marketing, tôi muốn xuất dữ liệu khách hàng quay lại ra file Excel.
* **US8 (WON'T):** Là Giám đốc, tôi muốn dự báo doanh thu tháng tới bằng mô hình AI.

## 4. Yêu cầu phi chức năng (NFR)
* **NFR01 (Hiệu năng):** Với khối lượng 100.000 dòng dữ liệu trong kho, Dashboard báo cáo phải tải xong và hiển thị hoàn chỉnh trong dưới **3 giây**.
* **NFR02 (Sẵn sàng/Bảo trì):** Quá trình ETL nạp dữ liệu từ các file CSV vào Kho dữ liệu (chạy batch ban đêm) phải hoàn thành trong thời gian tối đa là **2 giờ** đồng hồ.
* **NFR03 (Bảo mật):** Nhằm bảo mật thông tin, hệ thống tự động che giấu **4 số cuối** điện thoại của khách hàng (Data Masking) ngay tại tầng ETL trước khi đưa lên báo cáo phân tích (Ví dụ: 0901***567).

## 5. Ràng buộc và quy tắc nghiệp vụ
* **QT-01:** Một đơn hàng hợp lệ được ghi nhận doanh thu bắt buộc phải có đầy đủ mã cửa hàng, mã sản phẩm và ngày giao dịch.
* **QT-02:** Doanh thu của sản phẩm (thành tiền) được tính bằng `so_luong` nhân với `don_gia` tại thời điểm bán.
* **QT-03:** Các dòng dữ liệu bị lỗi định dạng trong file CSV nguồn sẽ bị đẩy vào `reject_log` thay vì làm sập toàn bộ tiến trình nạp (ETL).

## 6. Bảng truy vết yêu cầu (Traceability Matrix)

| Yêu cầu chức năng (FR) | User Story (US) | Use Case (UC) | Mức ưu tiên (MoSCoW) |
| :--- | :--- | :--- | :--- |
| FR01: Báo cáo tổng doanh thu | US1 | UC1: Xem báo cáo doanh thu | MUST |
| FR02: Cảnh báo giảm doanh thu | US2 | UC2: Xem cảnh báo doanh thu | MUST |
| FR03: Phân tích khách quay lại | US3 | UC3: Phân tích Retention | MUST |
| FR04: Doanh thu theo nhóm SP | US4 | UC4: Phân tích theo sản phẩm | SHOULD |
| FR05: Ghi nhận lỗi ETL | US5 | UC5: Xem log lỗi nạp dữ liệu | SHOULD |

---

## 7. Phụ lục: Mô tả các thiết kế kỹ thuật

### 7.1. Kiến trúc luồng dữ liệu (Data Pipeline)
Sơ đồ `architecture.drawio` thể hiện luồng dữ liệu của hệ thống, đi từ khâu tiếp nhận CSV đến khâu trực quan hóa (BI Dashboard).
* **Lập luận thiết kế 1:** Vì NFR01 yêu cầu dashboard tải dưới 3 giây, tôi chọn kiến trúc Kho dữ liệu dạng Star Schema (Lược đồ hình sao) để tối ưu hóa tốc độ truy vấn gộp (aggregation), đánh đổi là tốn thêm dung lượng lưu trữ cho dữ liệu dư thừa ở các chiều.
* **Lập luận thiết kế 2:** Vì NFR02 yêu cầu giới hạn thời gian nạp không quá 2 giờ, tôi chọn luồng xử lý Batch Processing định kỳ ban đêm thay vì Real-time Streaming, đánh đổi là dữ liệu trên báo cáo có độ trễ 1 ngày.
* **Lập luận thiết kế 3:** Vì NFR03 yêu cầu bảo mật che 4 số cuối điện thoại, tôi chọn thực hiện Data Masking ngay tại tầng ETL trước khi nạp vào kho, đánh đổi là Data Engineer tốn thêm thời gian phát triển logic xử lý chuỗi.

### 7.2. Mô hình dữ liệu (Star Schema)
Sơ đồ `erd.drawio` được thiết kế theo Lược đồ hình sao (Star Schema) chủ ý phi chuẩn hóa để tối ưu hóa tốc độ đọc thay vì chuẩn hóa 3NF.
* **Mức chi tiết (Grain):** Một dòng trong bảng `fact_sales` đại diện cho MỘT SẢN PHẨM nằm trong MỘT ĐƠN HÀNG được bán tại MỘT CỬA HÀNG vào MỘT NGÀY.
* **Bản ghi Unknown:** Các bảng Dimension chừa sẵn một bản ghi Unknown (`key = -1`) để chứa các fact có dữ liệu nguồn không khớp.
* **Dimension thay đổi theo thời gian (SCD):** Quyết định chọn SCD Loại 2 cho bảng `dim_customer` để phục vụ US3. Lý do: Cần tính tỷ lệ khách quay lại dựa trên thông tin chính xác TẠI THỜI ĐIỂM mua hàng chứ không ghi đè mất lịch sử. Đánh đổi: tốn dung lượng và truy vấn phức tạp hơn.

### 7.3. Thiết kế giao diện (Wireframe)
File `wireframe.png` cung cấp thiết kế cấu trúc cho 3 vùng báo cáo cốt lõi phục vụ Track DA:
1. **Khung 1 (Phục vụ US1):** Dashboard Tổng Doanh Thu sử dụng biểu đồ cột.
2. **Khung 2 (Phục vụ US2):** Bảng Cảnh Báo Giảm Doanh Thu.
3. **Khung 3 (Phục vụ US3):** Biểu đồ Tỉ Lệ Khách Quay Lại (Pie Chart).
Các chỉ số trên Wireframe đối chiếu trực tiếp với các trường trong bảng `fact_sales` của sơ đồ mô hình dữ liệu.
