import pandas as pd
import os

def doc_khach_hang(duong_dan='dataset/customers_raw.csv'):
    """Đọc dữ liệu khách hàng thô. Giữ nguyên định dạng số điện thoại."""
    if not os.path.exists(duong_dan):
        print(f"Lỗi: Không tìm thấy file {duong_dan}")
        return pd.DataFrame()
    return pd.read_csv(duong_dan, dtype={'so_dien_thoai': str})

def doc_don_hang(duong_dan='dataset/orders_2024_2026.csv'):
    """Đọc thông tin tổng quan đơn hàng."""
    if not os.path.exists(duong_dan):
        print(f"Lỗi: Không tìm thấy file {duong_dan}")
        return pd.DataFrame()
    return pd.read_csv(duong_dan, dtype={'so_dien_thoai': str, 'ma_don': str, 'ma_cua_hang': str})

def doc_chi_tiet_don_hang(duong_dan='dataset/order_items.csv'):
    """Đọc thông tin chi tiết từng dòng sản phẩm trong đơn."""
    if not os.path.exists(duong_dan):
        print(f"Lỗi: Không tìm thấy file {duong_dan}")
        return pd.DataFrame()
    return pd.read_csv(duong_dan, dtype={'order_id': str, 'product_id': str})

def doc_san_pham(duong_dan='dataset/products.csv'):
    """Đọc danh mục sản phẩm."""
    if not os.path.exists(duong_dan):
        print(f"Lỗi: Không tìm thấy file {duong_dan}")
        return pd.DataFrame()
    return pd.read_csv(duong_dan, dtype={'product_id': str, 'product_code': str})

def doc_cua_hang(duong_dan='dataset/stores.csv'):
    """Đọc danh mục cửa hàng."""
    if not os.path.exists(duong_dan):
        print(f"Lỗi: Không tìm thấy file {duong_dan}")
        return pd.DataFrame()
    return pd.read_csv(duong_dan, dtype={'store_id': str, 'store_code': str})