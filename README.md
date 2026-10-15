# Chuyen_de_1

Lựa chọn luồng giải pháp theo yêu cầu qua bài mô phỏng

# 1. Trên GitHub: New repository

# Tên repo: cdtn1-phamtruongluan-l6

# [x] Add a README file Visibility: Public

# 2. Clone về máy

git clone https://github.com/Nual-Truong/Chuyen_de_1.git

# 3. Dùng cấu trúc thư mục chuẩn (xem slide buổi 1)

mkdir -p docs src tests data
touch docs/srs.md docs/ai-disclosure.md .env.example

# 4. Tạo .gitignore — LẤY MẪU THEO TRACK Ở SLIDE SAU

# Kiểm tra ngay: git status -> không được thấy node_modules/ hay venv/

# 5. Cấu hình danh tính

git config user.name "Nguyen Van An"
git config user.email "an.nguyenvan@vlu.edu.vn"

# 6. Commit đầu tiên — đúng quy ước Conventional Commits

git add .
git commit -m "chore(init): khoi tao cau truc thu muc, gitignore va env.example"
git push origin main

# 7. Kiểm chứng: mở repo trên GitHub, phải thấy đủ 4 thư mục và 3 file cấu hình

## 8. Yêu cầu môi trường

- Python 3.10 trở lên.
- Quản lý gói: `pip`.
- Các thư viện bắt buộc (liệt kê trong `requirements.txt`): `pandas`, `sqlalchemy`, `pytest`, `pyyaml`.
- Cơ sở dữ liệu: `SQLite` (Tích hợp sẵn, file `.db` sẽ được tự động tạo trong thư mục `data/` khi chạy).

## 9. Lệnh chạy toàn bộ dự án (One-click Run)

Để cài đặt môi trường, chạy kiểm thử logic và thực thi Pipeline từ A-Z, bạn chỉ cần mở Terminal tại thư mục gốc của dự án và chạy **1 chuỗi lệnh duy nhất** sau:

**Đối với Windows (Command Prompt / PowerShell):**

```bash
pip install -r requirements.txt && pytest -q && python -m src.pipeline
```
