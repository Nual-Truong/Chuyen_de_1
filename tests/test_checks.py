import pandas as pd
from src.transform.clean_customers import lam_sach_khach_hang
from src.transform.clean_orders import lam_sach_don_hang
from src.quality import checks

def test_TC05_hop_dong_du_lieu_clean_customers():
    """Test hợp đồng ở ranh giới Transform: Kiểm tra đầy đủ tên cột đầu ra và tách dòng lỗi."""
    df_mau = pd.DataFrame([
        {'record_id': '1', 'ho_ten': 'Nguyễn Văn A', 'so_dien_thoai': '0912345678', 'ngay_tao': '2025-01-01'},
        {'record_id': '2', 'ho_ten': 'Trần Thị B', 'so_dien_thoai': 'sdt_rac_123', 'ngay_tao': '2025-01-02'}
    ])
    df_sach, df_reject = lam_sach_khach_hang(df_mau)
    
    # Kiểm tra hình dạng (Shape) của hợp đồng dữ liệu
    for cot_bat_buoc in ['sdt_chuan', 'ten_chuan', 'khoa_khach_hang']:
        assert cot_bat_buoc in df_sach.columns
    assert len(df_sach) == 1
    assert len(df_reject) == 1
    assert df_reject.iloc[0]['ma_quy_tac'] == 'CL1'

def test_TC06_phat_hien_lech_thanh_tien_CL3():
    """Test quy tắc nghiệp vụ QT-02 / CL3: Phát hiện dòng có thanh_tien != so_luong * don_gia."""
    df_ord = pd.DataFrame([
        {'order_id': '1', 'ma_don': 'HD01', 'ma_cua_hang': 'MM001', 'ngay': '17/08/2025', 'ten_khach': 'A', 'so_dien_thoai': '0912345678', 'thanh_tien': '2000'}
    ])
    df_itm = pd.DataFrame([
        {'order_id': '1', 'product_id': '10', 'so_luong': '2', 'don_gia': '1000', 'thanh_tien': '2000'}, # Đúng
        {'order_id': '1', 'product_id': '11', 'so_luong': '2', 'don_gia': '1000', 'thanh_tien': '9999'}  # Sai tiền
    ])
    _, df_itm_sach, df_reject = lam_sach_don_hang(df_ord, df_itm)
    assert len(df_itm_sach) == 1
    assert len(df_reject) == 1
    assert df_reject.iloc[0]['ma_quy_tac'] == 'CL3'