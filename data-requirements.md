# ĐẶC TẢ YÊU CẦU DỮ LIỆU (TRACK DA)

## 1. Câu hỏi phân tích
* **CH1:** Doanh thu từng cửa hàng theo tháng là bao nhiêu? (Trỏ về US1)
* **CH2:** Cửa hàng nào có doanh thu giảm ba tháng liên tiếp? (Trỏ về US2)
* **CH3:** Tỉ lệ khách hàng quay lại mua lần thứ hai là bao nhiêu? (Trỏ về US3)

## 2. Nguồn dữ liệu

| Nguồn | Định dạng | Tần suất | Khối lượng | Vấn đề đã biết |
| :--- | :--- | :--- | :--- | :--- |
| `orders_2024_2026.csv` | CSV | Hằng tháng | ~26.000 dòng | 3 định dạng ngày lẫn lộn; mã đơn trùng giữa các cửa hàng. |
| `order_items.csv` | CSV | Hằng tháng | ~48.000 dòng | `thanh_tien` đôi khi không khớp `so_luong * don_gia`. |
| `products.csv` | CSV | Khi có thay đổi | 420 dòng | Cùng một sản phẩm có nhiều cách viết tên. |

## 3. Từ điển dữ liệu nguồn (Bảng Orders)

| Cột nguồn | Kiểu thực tế | Ý nghĩa | Giá trị hợp lệ | Tỉ lệ thiếu (Đo được) |
| :--- | :--- | :--- | :--- | :--- |
| `Ngay` | Văn bản | Ngày phát sinh đơn hàng | `dd/mm/yyyy`, `d-m-yy`, `yyyy.mm.dd` | 0,4% |
| `Ma_don` | Văn bản | Mã đơn hàng cửa hàng tự đặt | Bất kỳ (Có trùng lặp) | 0% |
| `SDT` | Văn bản | Số điện thoại khách | Bắt đầu bằng 0 hoặc 84, 10-11 số | 6,2% |
| `Thanh_tien` | Chuỗi/Số | Thành tiền đơn hàng | Số nguyên (có thể dính chữ "đ") | 1,1% |

## 4. Quy tắc chất lượng dữ liệu
* **CL1 (Completeness):** Sau khi làm sạch, tỉ lệ thiếu của cột `ngay_dat` và `thanh_tien` phải bằng 0%. (Kiểm chứng: Đếm số ô null trên bảng đích).
* **CL2 (Validity):** 100% giá trị `ngay_dat` quy về được định dạng chuẩn ISO 8601 (YYYY-MM-DD); dòng vi phạm đẩy vào `reject_log`.
* **CL3 (Uniqueness):** Khóa nghiệp vụ `(ma_cua_hang + ma_don)` là duy nhất trong bảng Fact. (Kiểm chứng: Đối chiếu `COUNT(*)` với `COUNT(DISTINCT)`).
* **CL4 (Accuracy):** `thanh_tien = so_luong x don_gia` với sai lệch tuyệt đối <= 1 VND cho >= 99.5% số dòng.

## 5. Mức chi tiết (Grain)
* **Phát biểu Grain:** "Một dòng trong bảng `fact_sales` đại diện cho **MỘT SẢN PHẨM** nằm trong **MỘT ĐƠN HÀNG** được bán tại **MỘT CỬA HÀNG** vào **MỘT NGÀY**."

## 6. Quy tắc biến đổi
* **Ngày tháng:** Thử parse qua 3 định dạng ưu tiên. Không thành công -> gán null và đẩy báo lỗi.
* **SĐT:** Strip mọi khoảng trắng, bỏ ký tự lạ. Nếu bắt đầu bằng `84` thì cắt và nối thêm `0` ở đầu. Ép cứng độ dài 10 chữ số.
* **Thành tiền:** Xóa cụm từ "đ", "vnd", bỏ dấu phẩy phân cách ngàn, ép kiểu về `Integer`.
