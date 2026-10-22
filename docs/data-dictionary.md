# TỪ ĐIỂN DỮ LIỆU KHO DỮ LIỆU (DATA DICTIONARY)

## 1. Phát biểu Mức chi tiết (GRAIN) và Phát hiện dữ liệu thực tế

- **GRAIN của bảng sự kiện (`fact_sales`):** Một dòng trong bảng `fact_sales` đại diện cho **MỘT SẢN PHẨM** nằm trong **MỘT ĐƠN HÀNG** được bán tại **MỘT CỬA HÀNG** vào **MỘT NGÀY**.
- **Phát hiện khóa thực tế từ dữ liệu nguồn:** Trong tệp `orders_2024_2026.csv`, mã đơn hàng (`ma_don`, ví dụ `HD00001`) bị lặp lại giữa nhiều cửa hàng khác nhau. Do đó, khóa nghiệp vụ thực sự xác định duy nhất một đơn hàng là cặp **`(ma_cua_hang, ma_don)`** (được lưu thành `order_key`), không phải `ma_don` đứng một mình.
- **Quy ước Bản ghi Unknown:** Tất cả các bảng Dimension đều có bản ghi mặc định với khóa thay thế `key = -1` để hứng các giao dịch không khớp khóa ngoại, đảm bảo phép JOIN không làm mất dòng doanh thu nào.

## 2. Chi tiết các bảng trong Lược đồ Hình sao (Star Schema)

### 2.1. Bảng sự kiện: `fact_sales`

| Tên cột        | Kiểu dữ liệu | Ràng buộc | Mô tả ý nghĩa                                                      |
| :------------- | :----------- | :-------- | :----------------------------------------------------------------- |
| `order_key`    | VARCHAR(60)  | PK        | Khóa ghép đơn hàng (`ma_cua_hang` + `_` + `ma_don`)                |
| `product_key`  | INT          | PK, FK    | Khóa ngoại trỏ tới `dim_product(product_key)`                      |
| `date_key`     | INT          | FK        | Khóa ngoại trỏ tới `dim_date(date_key)` dạng YYYYMMDD              |
| `store_key`    | INT          | FK        | Khóa ngoại trỏ tới `dim_store(store_key)`                          |
| `customer_key` | INT          | FK        | Khóa ngoại trỏ tới `dim_customer(customer_key)`                    |
| `so_luong`     | INT          | NOT NULL  | Số lượng sản phẩm bán ra (Measure cộng dồn được)                   |
| `don_gia`      | INT          | NOT NULL  | Đơn giá bán tại thời điểm giao dịch (VNĐ)                          |
| `thanh_tien`   | INT          | NOT NULL  | Doanh thu dòng hàng = `so_luong * don_gia` (Measure cộng dồn được) |

### 2.2. Bảng chiều Khách hàng: `dim_customer` (Áp dụng SCD Type 2 & Data Masking)

| Tên cột               | Kiểu dữ liệu | Ràng buộc | Mô tả ý nghĩa                                                  |
| :-------------------- | :----------- | :-------- | :------------------------------------------------------------- |
| `customer_key`        | INT          | PK        | Khóa thay thế (Surrogate Key), `-1` là khách vãng lai/không rõ |
| `khoa_khach_hang`     | VARCHAR(220) | UNIQUE    | Khóa hợp nhất khách hàng (`sdt_chuan` + `_` + `ten_chuan`)     |
| `ho_ten`              | VARCHAR(160) | NOT NULL  | Họ và tên khách hàng                                           |
| `sdt`                 | VARCHAR(20)  | NOT NULL  | Số điện thoại đã che 4 số cuối theo NFR03 (VD: `090123****`)   |
| `phan_khuc`           | VARCHAR(40)  | NOT NULL  | Phân khúc khách hàng (theo dõi lịch sử bằng SCD Type 2)        |
| `hieu_luc_tu`         | DATE         | NOT NULL  | Ngày bắt đầu hiệu lực của bản ghi (SCD2)                       |
| `hieu_luc_den`        | DATE         | NOT NULL  | Ngày kết thúc hiệu lực của bản ghi (SCD2)                      |
| `la_ban_ghi_hien_tai` | BOOLEAN      | NOT NULL  | Cờ đánh dấu bản ghi hiện hành (`1` = hiện tại, `0` = lịch sử)  |

### 2.3. Bảng chiều Cửa hàng (`dim_store`), Sản phẩm (`dim_product`), Thời gian (`dim_date`)

- **`dim_store`:** `store_key` (INT, PK), `ma_cua_hang` (VARCHAR, Mã chi nhánh gốc), `ten_cua_hang` (VARCHAR, Tên chi nhánh), `thanh_pho` (VARCHAR), `quan_huyen` (VARCHAR), `ngay_khai_truong` (DATE).
- **`dim_product`:** `product_key` (INT, PK), `ma_san_pham` (VARCHAR, Mã SP gốc), `ten_san_pham` (VARCHAR, Tên SP), `nhom_san_pham` (VARCHAR, Nhóm hàng), `thuong_hieu` (VARCHAR, Hãng sản xuất).
- **`dim_date`:** `date_key` (INT, PK - dạng YYYYMMDD), `full_date` (DATE), `month` (INT), `quarter` (INT), `year` (INT).
