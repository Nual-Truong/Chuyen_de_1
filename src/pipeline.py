import argparse
import datetime
import yaml
import pandas as pd
from sqlalchemy import create_engine

# Import từ các module đã tách lớp (ĐẢM BẢO BẠN ĐÃ CÓ CÁC HÀM NÀY)
# Nếu bạn chưa code file extract, tạm thời chúng ta dùng DataFrame giả lập để test
# from src.extract.read_sources import doc_khach_hang
# from src.transform.clean_customers import lam_sach_khach_hang
from src.quality import checks
from src.load.load_staging import ghi_lo, ghi_reject, ghi_bao_cao

def main():
    batch_id = 'khach-hang-' + datetime.date.today().isoformat()
    print(f"=== Bắt đầu chạy lô: {batch_id} ===")
    
    # Kết nối CSDL (SQLite)
    engine = create_engine('sqlite:///data/mekong_dw.db')
    
    # ---- PHẦN NÀY LÀ MÔ PHỎNG DỮ LIỆU VÌ CHƯA CÓ FILE EXTRACT ----
    # Tạo một DataFrame mẫu để test pipeline
    data_tho = {
        'ma_cua_hang': ['CH01', 'CH02', 'CH01'],
        'ma_don': ['DH001', 'DH002', 'DH001'], # Lỗi trùng mã đơn
        'so_dien_thoai': ['0763247885', '090 123 4567', ''],
        'sdt_chuan': ['0763247885', '0901234567', None],
        'ngay': ['17/08/2025', '17-8-25', '2025.08.17'],
        'ngay_chuan': [datetime.date(2025, 8, 17), datetime.date(2025, 8, 17), datetime.date(2025, 8, 17)],
        'so_luong': [1, 2, 1],
        'don_gia': [5000, 3000, 5000],
        'thanh_tien': [5000, 6000, 4000] # Lỗi tiền không khớp ở dòng 3
    }
    df_sach = pd.DataFrame(data_tho)
    df_reject = pd.DataFrame([{'loi': 'test reject'}])
    # ---------------------------------------------------------------
    
    # 3. QUALITY
    ket_qua = [
        checks.cl1_dien_thoai_hop_le(df_sach),
        checks.cl2_ngay_hop_le(df_sach),
        checks.cl3_tien_khop(df_sach),
        checks.cl4_khoa_khong_trung(df_sach)
    ]
    
    # 4. LOAD
    ghi_lo(df_sach, batch_id, engine)
    ghi_reject(df_reject, batch_id, engine)
    ghi_bao_cao(ket_qua, batch_id, so_dong_vao=len(df_sach), so_reject=len(df_reject))
    
    print(f"Hoàn thành lô {batch_id}. Xem báo cáo tại thư mục reports/")

if __name__ == '__main__':
    main()