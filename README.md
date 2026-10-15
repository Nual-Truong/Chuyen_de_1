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
