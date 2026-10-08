# BẢN ĐẶC TẢ YÊU CẦU (SRS) RÚT GỌN

## 1. Giới thiệu và phạm vi
**Bối cảnh:** Mekong Mobile cần một kho dữ liệu tập trung để phân tích doanh thu từ 24 cửa hàng, thay thế việc tổng hợp thủ công từ các file Excel rời rạc.
**Phạm vi:** Tập trung xây dựng pipeline làm sạch dữ liệu đơn hàng và xây dựng các báo cáo/dashboard phân tích doanh thu, khách hàng, sản phẩm.
**Ngoài phạm vi (WON'T):** Không xây dựng tính năng dự báo doanh thu bằng Machine Learning; không phân quyền truy cập chi tiết đến từng nhân viên cấp dưới (chỉ cấp quyền xem cho cấp quản lý).
**Bảng thuật ngữ:**
 **Kho dữ liệu (Data Warehouse):** Hệ thống lưu trữ dữ liệu đã làm sạch từ các cửa hàng.
 **Khách hàng quay lại (Retention):** Khách hàng có >= 2 đơn hàng thành công trong các tháng khác nhau.
 **Doanh thu thuần:** Tổng `thanh_tien` của các đơn hàng hợp lệ, không tính đơn bị hủy.

## 2. Các bên liên quan và vai trò

| Vai trò | Quyền hạn và nghiệp vụ chính |
| :--- | :--- |
| **Giám đốc (Ông Minh)** | Xem toàn bộ báo cáo doanh thu tổng hợp, dashboard so sánh các cửa hàng. |
| **Trưởng phòng Marketing** | Xem báo cáo phân tích hành vi khách hàng, tỉ lệ khách quay lại. |
| **Quản lý sản phẩm** | Xem báo cáo doanh thu theo từng nhóm sản phẩm. |
| **Data Engineer** | Cấu hình pipeline nạp dữ liệu (ETL), theo dõi log lỗi dữ liệu. |

## 3. Yêu cầu chức năng (FR) & User Story
**US1 (MUST):** Là Giám đốc, tôi muốn xem tổng doanh thu từng cửa hàng theo tháng để đánh giá hiệu quả kinh doanh.
 *AC1.1:* GIVEN dữ liệu đơn hàng hợp lệ, WHEN Giám đốc chọn bộ lọc tháng/năm, THEN hệ thống hiển thị biểu đồ doanh thu của 24 cửa hàng.
 *AC1.2 (Ngoại lệ):* GIVEN tháng được chọn chưa có dữ liệu nạp vào kho, WHEN Giám đốc bấm Lọc, THEN hệ thống báo "Chưa có dữ liệu cho kỳ báo cáo này".
**US2 (MUST):** Là Giám đốc, tôi muốn xác định các cửa hàng có doanh thu giảm 3 tháng liên tiếp để có biện pháp xử lý.
 *AC2.1:* GIVEN dữ liệu đã cập nhật, WHEN xem dashboard cảnh báo, THEN hệ thống highlight màu đỏ các cửa hàng có doanh thu Tháng(N) < Tháng(N-1) < Tháng(N-2).
 *AC2.2 (Ngoại lệ):* GIVEN cửa hàng mới mở chưa đủ 3 tháng dữ liệu, WHEN xem dashboard cảnh báo, THEN hệ thống ẩn cửa hàng này khỏi danh sách cảnh báo.
**US3 (MUST):** Là Trưởng phòng Marketing, tôi muốn tính tỉ lệ khách quay lại mua lần hai để đánh giá mức độ trung thành.
 *AC3.1:* GIVEN tập khách hàng hợp lệ, WHEN xem báo cáo Retention, THEN hiển thị biểu đồ tròn biểu diễn % khách có >= 2 đơn hàng.
 *AC3.2 (Ngoại lệ):* GIVEN các đơn hàng không thu thập được số điện thoại chuẩn, WHEN hệ thống tính toán, THEN hệ thống tự động loại bỏ các đơn này khỏi mẫu số chung để đảm bảo tỉ lệ chính xác.
**US4 (SHOULD):** Là Quản lý sản phẩm, tôi muốn phân tích doanh thu theo nhóm sản phẩm để tối ưu danh mục nhập hàng.
**US5 (SHOULD):** Là Data Engineer, tôi muốn xem danh sách các dòng dữ liệu bị loại (reject) khi nạp vào kho để xử lý lỗi đầu vào.
**US6 (COULD):** Là Giám đốc, tôi muốn lọc báo cáo doanh thu theo khu vực địa lý (Quận/Huyện).
**US7 (COULD):** Là Trưởng phòng Marketing, tôi muốn xuất dữ liệu khách hàng quay lại ra file Excel.
**US8 (WON'T):** Là Giám đốc, tôi muốn dự báo doanh thu tháng tới bằng mô hình AI.

## 4. Yêu cầu phi chức năng (NFR)
 **NFR1 (Hiệu năng):** Dashboard báo cáo doanh thu năm phải tải xong và hiển thị hoàn chỉnh trong dưới 3 giây khi truy vấn trên 100.000 dòng fact sales.
 **NFR2 (Tính sẵn sàng):** Thời gian gián đoạn của kho dữ liệu để chạy ETL cập nhật hàng tháng không được vượt quá 2 giờ (chạy từ 00:00 đến 02:00 sáng ngày mùng 1 hàng tháng).
 **NFR3 (Bảo mật):** 100% số điện thoại khách hàng hiển thị trên dashboard của Quản lý sản phẩm phải được che 4 số cuối (định dạng `0901xxx567`).

## 5. Ràng buộc và quy tắc nghiệp vụ
 **QT_DA_01:** Thành tiền của một dòng đơn hàng bắt buộc phải bằng số lượng nhân với đơn giá (sai lệch cho phép tối đa <= 1 VND).
 **QT_DA_02:** Mã đơn hàng không có tính duy nhất trên toàn hệ thống, khóa định danh duy nhất bắt buộc phải là cụm `(ma_cua_hang + ma_don)`.
 **QT_DA_03:** Các đơn hàng không chuyển đổi được định dạng ngày chuẩn ISO sẽ bị đẩy vào bảng `reject_log`, tuyệt đối không đưa vào báo cáo phân tích.

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
**Actor:** Giám đốc (Primary), Data Engineer (Primary), Trưởng phòng Marketing (Primary).
 `UC1`: Nạp và chuẩn hóa dữ liệu bán hàng thô (Data Engineer).
 `UC2`: Tra cứu doanh thu cửa hàng theo kỳ (Giám đốc).
 `UC3`: Theo dõi cảnh báo cửa hàng giảm doanh thu (Giám đốc).
 `UC4`: Phân tích tỉ lệ khách hàng quay lại (Trưởng phòng Marketing).
 `UC5`: Xuất báo cáo dữ liệu phân tích ra Excel (Giám đốc, Marketing).

**Đặc tả Use Case chính: UC2 - TRA CỨU DOANH THU CỬA HÀNG THEO KỲ**
 **Actor chính:** Giám đốc
 **Mục tiêu:** Xem báo cáo tổng hợp doanh thu của toàn bộ 24 cửa hàng trong một tháng/quý cụ thể.
 **Điều kiện trước:** Giám đốc đã đăng nhập; dữ liệu tháng cần xem đã được Data Engineer nạp vào Data Warehouse thành công.
 **Điều kiện sau:** Hiển thị biểu đồ cột so sánh doanh thu và bảng số liệu chi tiết.
 **Luồng chính (Happy Path):**
  1. Giám đốc truy cập vào màn hình "Dashboard Doanh Thu".
  2. Hệ thống hiển thị giao diện báo cáo với các bộ lọc mặc định là tháng hiện tại.
  3. Giám đốc chọn một "Tháng" và "Năm" trong bộ lọc và bấm "Xem báo cáo".
  4. Hệ thống truy vấn dữ liệu từ bảng Fact Sales, nhóm theo `ma_cua_hang`.
  5. Hệ thống render biểu đồ cột so sánh và hiển thị tổng doanh thu.
 **Luồng ngoại lệ:**
  **a. Dữ liệu tháng được chọn chưa có trong kho:**
    Hệ thống kiểm tra thấy truy vấn trả về 0 dòng.
    Hệ thống hiển thị popup cảnh báo: "Dữ liệu của tháng [X] chưa được cập nhật. Vui lòng liên hệ Data Engineer".
    Hệ thống giữ nguyên biểu đồ của kỳ báo cáo trước đó.

## 8. Mô tả các thiết kế
### Mô tả Sơ đồ Kiến trúc (Data Flow/Pipeline)
Sơ đồ `architecture.drawio` thể hiện luồng dữ liệu (Data Pipeline) của hệ thống Kho dữ liệu Mekong Mobile, đi từ khâu tiếp nhận đến khâu trực quan hóa:
 **Hệ thống nguồn (Source):** Dữ liệu thô được trích xuất từ 3 file định dạng CSV (`orders`, `order_items`, `products`).
 **Tầng ETL (Extract - Transform - Load):** Dữ liệu đi qua các bước làm sạch (chuẩn hóa ngày tháng, xử lý lỗi SĐT) và biến đổi (tính toán lại thành tiền, kết nối các bảng) trước khi nạp. Các dòng lỗi định dạng không thể cứu vãn sẽ bị đẩy vào `reject_log`.
 **Tầng Lưu trữ (Data Warehouse):** Dữ liệu sạch được lưu trữ tập trung theo dạng Lược đồ hình sao (Star Schema) để tối ưu cho truy vấn phân tích.
 **Tầng Trực quan hóa (BI Dashboard):** Nơi Giám đốc và Trưởng phòng Marketing thao tác với các biểu đồ tổng hợp.

**3 Quyết định kiến trúc cốt lõi:**
1. Vì **NFR1** yêu cầu dashboard tải dưới 3 giây với khối lượng 100.000 dòng, chúng tôi chọn kiến trúc **Kho dữ liệu dạng Star Schema (Lược đồ hình sao)** để tối ưu hóa tốc độ truy vấn gộp (aggregation), đánh đổi là tốn thêm dung lượng lưu trữ cho dữ liệu dư thừa ở các chiều (dimensions).
2. Vì **NFR2** yêu cầu thời gian bảo trì nạp dữ liệu không vượt quá 2 giờ, chúng tôi chọn luồng xử lý **Batch Processing (Xử lý theo lô định kỳ ban đêm)** thay vì Real-time Streaming, đánh đổi là dữ liệu trên báo cáo có độ trễ 1 ngày.
3. Vì **NFR3** yêu cầu bảo mật che 4 số cuối điện thoại, chúng tôi chọn thực hiện **Data Masking (Che giấu dữ liệu) ngay tại tầng ETL** trước khi nạp vào kho, đánh đổi là Data Engineer tốn thêm thời gian phát triển logic xử lý chuỗi.

### Mô tả Mô hình Dữ liệu (Star Schema)
Sơ đồ `erd.drawio` mô tả cấu trúc cơ sở dữ liệu phân tích của hệ thống, được thiết kế theo Lược đồ hình sao (Star Schema) kinh điển trong Data Warehouse, bao gồm:
 **Bảng Sự kiện (Fact Table) - `fact_sales`:** Lưu trữ các chỉ số đo lường (measures) như `so_luong`, `don_gia`, `thanh_tien` và các khóa ngoại liên kết. Khóa chính của bảng là khóa ghép `(ma_cua_hang + ma_don)` do mã đơn nguyên thủy không có tính duy nhất.
 **Các Bảng Chiều (Dimension Tables):** 
 `dim_date`: Lưu trữ thông tin phân cấp thời gian (ngày, tháng, quý, năm) phục vụ bộ lọc thời gian.
 `dim_store`: Lưu trữ thông tin chi tiết về 24 cửa hàng bán lẻ.
 `dim_product`: Lưu trữ thông tin định danh và phân loại nhóm sản phẩm.

**Mức chi tiết (Grain):** 
Một dòng trong bảng `fact_sales` đại diện cho **MỘT SẢN PHẨM** nằm trong **MỘT ĐƠN HÀNG** được bán tại **MỘT CỬA HÀNG** vào **MỘT NGÀY**. Đây là mức chi tiết sâu nhất, cho phép hệ thống linh hoạt tổng hợp dữ liệu theo bất kỳ chiều (dimension) nào mà không bị mất mát thông tin.

### Mô tả Bản phác thảo Giao diện (Wireframe)
File `wireframe.png` cung cấp thiết kế cấu trúc (low-fidelity) cho 3 vùng báo cáo cốt lõi, tập trung vào việc bố trí luồng dữ liệu hơn là giao diện đồ họa chi tiết:
1. **Khung 1 - Dashboard Tổng Doanh Thu (Phục vụ US1):** Sử dụng biểu đồ cột (Bar Chart) để so sánh trực quan doanh thu giữa các cửa hàng trong một kỳ báo cáo cụ thể. Nguồn dữ liệu được tính toán dựa trên truy vấn `SUM(thanh_tien)` kết hợp giữa bảng Fact và bảng Dimension Cửa hàng.
2. **Khung 2 - Bảng Cảnh Báo Giảm Doanh Thu (Phục vụ US2):** Bố trí dưới dạng bảng ma trận (Table). Các dòng dữ liệu của cửa hàng có doanh thu giảm liên tục trong 3 tháng sẽ được hệ thống highlight (làm nổi bật) để Giám đốc nhận diện rủi ro tức thời.
3. **Khung 3 - Biểu đồ Tỉ Lệ Khách Quay Lại (Phục vụ US3):** Sử dụng biểu đồ tròn (Pie Chart) biểu diễn tỉ trọng tập khách hàng. Hệ thống đếm phân biệt các đơn hàng `COUNT(DISTINCT order_key)` nhóm theo định danh số điện thoại khách hàng (đã được che bảo mật) để tính ra tỉ lệ Retention.

### Mô tả Mô hình Dữ liệu (Star Schema)
Sơ đồ `erd.drawio` được thiết kế theo Lược đồ hình sao (Star Schema) chủ ý phi chuẩn hóa để tối ưu hóa tốc độ đọc và khả năng tổng hợp nhiều chiều thay vì chuẩn hóa 3NF.

 **Mức chi tiết (Grain):** Một dòng trong bảng `fact_sales` đại diện cho MỘT SẢN PHẨM nằm trong MỘT ĐƠN HÀNG được bán tại MỘT CỬA HÀNG vào MỘT NGÀY.
 **Xử lý bản ghi mồ côi:** Mọi bảng Dimension đều được thiết kế chừa sẵn một bản ghi Unknown (`key = -1`) để chứa các fact có dữ liệu nguồn không khớp (VD: mã cửa hàng bị sai trong file CSV không tìm thấy ở bảng chi nhánh).
 **Dimension thay đổi theo thời gian (SCD):** Quyết định chọn **SCD Loại 2** cho bảng `dim_customer` (bằng cách thêm cột `hieu_luc_tu`, `hieu_luc_den`, `la_ban_ghi_hien_tai`). Lý do: Cần tính chính xác tỉ lệ khách hàng quay lại (US3) dựa trên phân khúc/thông tin khách hàng đúng TẠI THỜI ĐIỂM mua hàng chứ không ghi đè mất lịch sử. Đánh đổi: Bảng `dim_customer` tốn nhiều dung lượng lưu trữ hơn và truy vấn phải kẹp thêm điều kiện lọc khoảng thời gian hiệu lực.
