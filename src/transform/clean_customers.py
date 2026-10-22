import pandas as pd
from src.transform.rules import chuan_hoa_dien_thoai, chuan_hoa_ten, khoa_hop_nhat

def lam_sach_khach_hang(df_tho):
    """
    Nhận DataFrame khách hàng thô.
    Trả về 2 DataFrame: sach (dữ liệu hợp lệ) và reject (dữ liệu lỗi).
    Tuyệt đối không thao tác với CSDL ở đây.
    """
    if df_tho.empty:
        return pd.DataFrame(), pd.DataFrame()
        
    df = df_tho.copy()
    
    # 1. Áp dụng các quy tắc chuẩn hóa
    df['sdt_chuan'] = df['so_dien_thoai'].apply(chuan_hoa_dien_thoai)
    df['ten_chuan'] = df['ho_ten'].apply(chuan_hoa_ten)
    
    # 2. Tạo khóa tổng hợp để phát hiện trùng lặp (ví dụ: gộp Nguyễn Văn A và Nguyen Van A)
    # Cũ: 

    df['khoa_khach_hang'] = df.apply(lambda row: f"{khoa_hop_nhat(row['ho_ten'], row['so_dien_thoai'])[0]}_{khoa_hop_nhat(row['ho_ten'], row['so_dien_thoai'])[1]}", axis=1)
    
    # 3. Định nghĩa quy tắc lọc (CL1: Số điện thoại phải chuẩn hóa được)
    # Lỗi nếu SĐT gốc có chứa ký tự nhưng hàm chuẩn hóa trả về None
    reject_mask = df['sdt_chuan'].isna() & df['so_dien_thoai'].notna() & (df['so_dien_thoai'].astype(str).str.strip() != '')
    
    # Tách dữ liệu sạch
    df_sach = df[~reject_mask].copy()
    
    # 3. Tạo cấu trúc cho bảng Reject (chỉ lấy các dòng bị lỗi)
    df_reject = pd.DataFrame()
    if reject_mask.sum() > 0:
        df_reject = df[reject_mask].copy()
        df_reject['ma_quy_tac'] = 'CL1'
        df_reject['ly_do'] = 'Số điện thoại sai định dạng, không thể chuẩn hóa thành chuẩn 10 số.'
        # Lưu toàn bộ dòng gốc nguyên bản dưới dạng JSON để truy vết
        df_reject['du_lieu_goc'] = df_reject.apply(lambda row: row.to_json(force_ascii=False), axis=1)
        # Chỉ giữ lại các cột cần thiết cho bảng reject_rows trong CSDL
        df_reject = df_reject[['ma_quy_tac', 'ly_do', 'du_lieu_goc']]

    return df_sach, df_reject