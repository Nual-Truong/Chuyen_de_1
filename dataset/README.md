# Bộ dữ liệu mẫu — Case study Smart CRM · Mekong Mobile

Chuyên đề tốt nghiệp 1 · Khoa Công nghệ Thông tin · Trường Đại học Văn Lang · HK1 2026–2027  
Biên soạn: TS. Nguyễn Trí Hải · Bộ môn Công nghệ Phần mềm & Công nghệ Dữ liệu

---

## 1. Đây là gì

Bộ dữ liệu **sinh mô phỏng** cho doanh nghiệp giả định Mekong Mobile, dùng chung cho toàn bộ học phần.
Sinh bằng `gen_dataset.py` với `seed = 20260901` — chạy lại cùng seed sẽ ra đúng bộ dữ liệu này.

> **Mekong Mobile là doanh nghiệp MÔ PHỎNG.** Mọi số liệu, tên người và tên cửa hàng đều là giả định,
> được dựng riêng cho mục đích học tập. Không phản ánh bất kỳ tổ chức hay cá nhân có thật nào.

## 2. Danh mục tệp

| Tệp | Số dòng | Số cột | Dung lượng | Nội dung và luồng nghiệp vụ liên quan |
|---|---:|---:|---:|---|
| `customers_raw.csv` | 67.037 | 6 | 5835 KB | Hồ sơ khách hàng thô. CÓ LỖI CỐ Ý: ~20% khách bị trùng hồ sơ. số điện thoại 4 định dạng lẫn lộn. 6% thiếu số điện thoại. 9% thiếu địa chỉ. tên viết hoa/thường/không dấu lẫn lộn.  → L1. L7. L9 |
| `orders_2024_2026.csv` | 26.000 | 9 | 2258 KB | Đơn hàng 26 tháng của 24 cửa hàng. CÓ LỖI CỐ Ý: 3 định dạng ngày lẫn lộn. mã đơn trùng giữa các cửa hàng. thành tiền đôi khi lưu dạng văn bản kèm "đ". một số ô trống.  → L3. L6. L9 |
| `order_items.csv` | 35.697 | 5 | 997 KB | Dòng hàng của các đơn. CÓ LỖI CỐ Ý: ~1.5% dòng có thanh_tien ≠ so_luong × don_gia.  → L6 |
| `products.csv` | 320 | 7 | 21 KB | Danh mục sản phẩm kèm giá niêm yết và số tháng bảo hành.  → L6. L10 |
| `stores.csv` | 24 | 6 | 2 KB | Danh sách 24 cửa hàng kèm thành phố. quận/huyện và ngày khai trương.  → L6 |
| `service_centers.csv` | 6 | 4 | 0 KB | Danh sách 6 trung tâm bảo hành.  → L2. L4. L5 |
| `issue_categories.csv` | 6 | 4 | 0 KB | Danh mục 6 nhóm sự cố kèm mức ưu tiên mặc định.  → L2. L10 |
| `technicians.csv` | 38 | 6 | 2 KB | Kỹ thuật viên kèm bậc tay nghề và trung tâm làm việc.  → L4 |
| `technician_skills.csv` | 159 | 3 | 1 KB | Tay nghề của kỹ thuật viên theo từng nhóm sự cố (proficiency 1–5).  → L4 |
| `tickets_history.csv` | 7.800 | 15 | 1481 KB | Phiếu bảo hành lịch sử 26 tháng. đã gán nhóm sự cố. ~14.6% phiếu đã đóng bị quá hạn cam kết (khớp vấn đề V2).  → L2. L4. L8. L10 |
| `ticket_status_log.csv` | 38.112 | 7 | 1839 KB | Lịch sử chuyển trạng thái của các phiếu. mỗi dòng có thời điểm và người thực hiện.  → L2. L4. L8 |
| `issue_descriptions.csv` | 4.000 | 3 | 333 KB | Mô tả lỗi bằng văn bản tự do tiếng Việt. ĐÃ GÁN NHÃN nhóm sự cố. Nhãn có nhiễu và mất cân bằng lớp.  → L10 |
| `parts.csv` | 180 | 4 | 8 KB | Danh mục linh kiện kèm đơn giá.  → L5 |
| `part_transactions.csv` | 4.954 | 7 | 202 KB | Nhập – xuất linh kiện theo trung tâm. gắn với mã phiếu bảo hành.  → L5 |
| `part_stock.csv` | 717 | 4 | 8 KB | Tồn kho linh kiện hiện tại theo trung tâm kèm ngưỡng cảnh báo.  → L5 |
| `survey_responses.csv` | 2.600 | 5 | 140 KB | Phản hồi khảo sát hài lòng sau khi phiếu được đóng (điểm 1–5 kèm nhận xét).  → L8 |

**Tổng cộng:** 16 tệp. 187.650 dòng, 12.8 MB.
## 3. Lỗi chất lượng dữ liệu — CỐ Ý, không phải sai sót

Các lỗi dưới đây được chèn có chủ đích để track DA có bài toán làm sạch thật. **Đừng xin bộ dữ liệu
sạch** — phát hiện, đo lường và xử lý chúng chính là nhiệm vụ của em.

| Tệp | Vấn đề | Mức đo được |
|---|---|---:|
| `customers_raw.csv` | Hồ sơ trùng (nhiều bản ghi cho cùng một số điện thoại) | ~20% số khách |
| `customers_raw.csv` | Thiếu số điện thoại | ~6,1% |
| `customers_raw.csv` | Thiếu địa chỉ | ~9,0% |
| `customers_raw.csv` | Số điện thoại có 4 dạng: `0xxx`, `84xxx`, `+84xxx`, có dấu cách/dấu chấm | ~20% bản ghi |
| `customers_raw.csv` | Tên viết hoa / thường / không dấu / thừa khoảng trắng | ~ lẫn lộn |
| `orders_2024_2026.csv` | Ba định dạng ngày lẫn lộn: `dd/mm/yyyy`, `d-m-yy`, `yyyy.mm.dd` | 62% / 24% / 14% |
| `orders_2024_2026.csv` | Ngày để trống | ~0,5% |
| `orders_2024_2026.csv` | `thanh_tien` lưu dạng văn bản kèm `đ` và dấu chấm phân cách | ~0,9% |
| `orders_2024_2026.csv` | `thanh_tien` để trống | ~1,1% |
| `orders_2024_2026.csv` | `nhan_vien` để trống, ghi tên gọi thân mật không có mã | ~3,8% |
| `orders_2024_2026.csv` | Mã đơn trùng giữa các cửa hàng (khóa nghiệp vụ phải là cặp mã cửa hàng + mã đơn) | ~1.100 mã |
| `order_items.csv` | `thanh_tien` ≠ `so_luong` × `don_gia` | ~1,5% |
| `issue_descriptions.csv` | Nhãn do người gán nên có nhiễu; mất cân bằng lớp | lớp nhỏ nhất 5,5% |

## 4. Lưu ý cho từng track

**Track SE** — Dùng `service_centers.csv`, `technicians.csv`, `technician_skills.csv`,
`issue_categories.csv`, `parts.csv`, `part_stock.csv` làm dữ liệu danh mục để nạp vào cơ sở dữ liệu
của em. `tickets_history.csv` dùng để có dữ liệu thử nghiệm thật khi kiểm thử.

**Track DA** — Nguồn chính là `orders_2024_2026.csv`, `order_items.csv`, `customers_raw.csv`.
Mọi con số về chất lượng dữ liệu trong tài liệu của em phải được **ĐO** trên các tệp này, không được
đoán. Bảng ở mục 3 là để em tự đối chiếu sau khi đo, không phải để chép lại.

**Track AI** — `issue_descriptions.csv` đã có nhãn, dùng cho luồng L10. Với luồng L9 (dự báo khách
rời bỏ), nhãn **không có sẵn** — em phải tự sinh từ quy tắc QT-11 dựa trên `orders_2024_2026.csv`,
và phải tránh rò rỉ dữ liệu khi tạo đặc trưng.

## 5. Giới hạn đã biết của bộ dữ liệu

Ghi rõ ở đây để em không mất thời gian đi tìm nguyên nhân:

- `due_date` trong `tickets_history.csv` được tính bằng **giờ lịch đơn giản** (24h / 72h / 120h theo
  mức ưu tiên), **chưa áp dụng** quy tắc "chỉ tính ngày làm việc thứ Hai đến thứ Bảy" của QT-04.
  Hiện thực đúng quy tắc QT-04 là một phần việc của em.
- `serial_no` trong `tickets_history.csv` được sinh ngẫu nhiên, không liên kết với một bảng `device`
  riêng. Nếu luồng của em cần bảng `device`, hãy tự dựng từ cặp (`customer_id`, `product_id`, `serial_no`).
- Dữ liệu không có yếu tố mùa vụ hay xu hướng rõ rệt theo thời gian. Nếu bài toán của em cần điều đó,
  hãy nêu rõ giới hạn này trong phần đánh giá.
- Tên khách hàng được sinh ngẫu nhiên từ danh sách họ và tên phổ biến, nên có nhiều người trùng tên.
  Đây là điều đúng với thực tế và là lý do **không được dùng tên làm khóa** để khử trùng.

## 6. Sinh dữ liệu bổ sung

Nếu luồng của em cần dữ liệu không có trong bộ mẫu, dùng `tools/gen_sample.py`:

```bash
# Luồng L3 — cơ hội bán hàng
python tools/gen_sample.py --entity opportunity --rows 500 --seed 42 --out opportunities.csv

# Luồng L4 — lịch hẹn, gắn với phiếu có sẵn
python tools/gen_sample.py --entity appointment --rows 1200 --seed 42 \
       --link tickets_history.csv --out appointments.csv

# Luồng L1 — lượt tương tác chiến dịch marketing
python tools/gen_sample.py --entity campaign_touch --rows 3000 --seed 42 \
       --link customers_raw.csv --out campaign_touches.csv
```

**Bắt buộc:** luôn đặt `--seed` và **ghi lại giá trị seed trong README của em**. Đây là điều kiện của
nguyên tắc *tái lập được* — người khác chạy lại với cùng seed phải ra đúng bộ dữ liệu của em.

## 7. Quy định sử dụng

- **KHÔNG commit** các tệp lớn (`customers_raw.csv`, `orders_2024_2026.csv`, `ticket_status_log.csv`,
  `tickets_history.csv`) vào Git repo. Chỉ commit một mẫu nhỏ vài trăm dòng trong `data/sample/`
  và ghi trong README cách tải bộ đầy đủ.
- Thêm vào `.gitignore` của em: `data/raw/`, `*.csv` (rồi dùng `!data/sample/*.csv` để giữ mẫu nhỏ).
- Bộ dữ liệu này chỉ dùng cho mục đích học tập trong học phần Chuyên đề tốt nghiệp 1.
