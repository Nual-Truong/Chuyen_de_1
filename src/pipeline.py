import argparse
import datetime
import pandas as pd
from sqlalchemy import create_engine

# Import từ các module đã tách lớp
from src.extract.read_sources import doc_khach_hang
from src.transform.clean_customers import lam_sach_khach_hang # Đã import hàm tách rời
from src.quality import checks
from src.load.load_staging import ghi_lo, ghi_reject, ghi_bao_cao

def main():
    batch_id = 'khach-hang-' + datetime.date.today().isoformat()
    print(f"=== Bắt đầu chạy lô: {batch_id} ===")
    
    engine = create_engine('sqlite:///data/mekong_dw.db')
    
    # 1. EXTRACT: Đọc dữ liệu thô (Đường dẫn gốc)
    duong_dan_csv = 'dataset/customers_raw.csv'
    tho = doc_khach_hang(duong_dan_csv)
    
    if tho.empty:
        print("Không có dữ liệu, dừng pipeline.")
        return
        
    # 2. TRANSFORM: Làm sạch và tách reject qua file chuyên biệt
    sach, reject = lam_sach_khach_hang(tho)
    
    # 3. QUALITY: Đo lường chất lượng
    ket_qua = [checks.cl1_dien_thoai_hop_le(sach)]
    
    # 4. LOAD: Ghi staging, ghi reject và xuất báo cáo
    ghi_lo(sach, batch_id, engine)
    ghi_reject(reject, batch_id, engine)
    ghi_bao_cao(ket_qua, batch_id, so_dong_vao=len(tho), so_reject=len(reject))
    
    print(f"Hoàn thành lô {batch_id}: Đã nạp {len(sach)} dòng sạch, đẩy sang bảng reject {len(reject)} dòng lỗi.")
    print("Xem báo cáo chi tiết tại thư mục reports/")

if __name__ == '__main__':
    main()