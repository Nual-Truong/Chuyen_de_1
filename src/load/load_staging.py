import json
from datetime import datetime
from sqlalchemy import text, inspect

def ghi_lo(df_sach, batch_id, engine, table_name='staging_customers'):
    """Ghi dữ liệu sạch vào bảng staging. Đảm bảo chạy lại không nhân đôi."""
    if df_sach.empty:
        return

    df_sach = df_sach.copy()
    df_sach['batch_id'] = batch_id
    
    # ÉP PANDAS XÓA BẢNG CŨ VÀ TẠO LẠI (Sửa if_exists='append' thành 'replace')
    with engine.begin() as conn:
        df_sach.to_sql(table_name, conn, if_exists='replace', index=False)

def ghi_reject(df_reject, batch_id, engine, table_name='reject_rows'):
    """Ghi các dòng dữ liệu không xử lý được vào bảng reject kèm lý do."""
    if df_reject.empty:
        return
        
    df_reject = df_reject.copy()
    df_reject['batch_id'] = batch_id
    
    # Với bảng Reject cũng ép tạo lại để test cho mượt
    with engine.begin() as conn:
        df_reject.to_sql(table_name, conn, if_exists='replace', index=False)

def ghi_bao_cao(ket_qua_kiem, batch_id, so_dong_vao, so_reject):
    """Tự động sinh báo cáo chất lượng ra file JSON lưu vào thư mục reports/"""
    report = {
        "batch_id": batch_id,
        "thoi_gian": datetime.now().isoformat(),
        "tong_so_dong_vao": so_dong_vao,
        "so_dong_sach": so_dong_vao - so_reject,
        "so_dong_reject": so_reject,
        "chi_tiet_kiem_tra": [
            {
                "ma": kq.ma,
                "ten": kq.ten,
                "so_dong_kiem": kq.so_dong_kiem,
                "so_dong_loi": kq.so_dong_loi,
                "ti_le_loi": round(kq.ti_le_loi * 100, 2),
                "nguong_cho_phep": kq.nguong_cho_phep * 100,
                "ket_luan": "ĐẠT" if kq.dat else "KHÔNG ĐẠT"
            } for kq in ket_qua_kiem
        ]
    }
    
    file_name = f"reports/chat-luong-{batch_id}.json"
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=4)
    return file_name