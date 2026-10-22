import argparse
import datetime
import logging
import os
import pandas as pd
from sqlalchemy import create_engine

from src.extract.read_sources import (
    doc_khach_hang, doc_don_hang, doc_chi_tiet_don_hang, doc_san_pham, doc_cua_hang
)
from src.transform.clean_customers import lam_sach_khach_hang
from src.transform.clean_orders import lam_sach_don_hang
from src.transform.rules import doc_ngay
from src.quality import checks
from src.load.load_staging import ghi_lo, ghi_reject, ghi_bao_cao
from src.load.load_warehouse import nap_kho_du_lieu

def parse_args():
    parser = argparse.ArgumentParser(description='Mekong Mobile ETL Pipeline')
    parser.add_argument('--tu-ngay', type=str, default=None, help='Ngày bắt đầu lọc (YYYY-MM-DD)')
    parser.add_argument('--den-ngay', type=str, default=None, help='Ngày kết thúc lọc (YYYY-MM-DD)')
    return parser.parse_args()

def main():
    args = parse_args()
    os.makedirs('reports', exist_ok=True)
    os.makedirs('data', exist_ok=True)

    # Sinh mã lô dựa theo phạm vi ngày để chạy lại cùng phạm vi không bị nhân đôi lô
    if args.tu_ngay and args.den_ngay:
        batch_id = f"lo-{args.tu_ngay}-{args.den_ngay}"
    else:
        batch_id = "lo-toan-bo"

    # Cấu hình ghi file log vào reports/
    log_file = f"reports/run_{batch_id}.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    logging.info(f"=== Bắt đầu chạy Pipeline ETL - Mã lô: {batch_id} ===")
    db_url = os.environ.get('DWH_URL', 'sqlite:///data/mekong_dw.db')
    engine = create_engine(db_url)

    # 1. EXTRACT
    data_dir = os.environ.get('DATA_DIR', 'dataset')
    df_cus_tho = doc_khach_hang(f'{data_dir}/customers_raw.csv')
    df_ord_tho = doc_don_hang(f'{data_dir}/orders_2024_2026.csv')
    df_itm_tho = doc_chi_tiet_don_hang(f'{data_dir}/order_items.csv')
    df_prd_tho = doc_san_pham(f'{data_dir}/products.csv')
    df_str_tho = doc_cua_hang(f'{data_dir}/stores.csv')

    if df_cus_tho.empty or df_ord_tho.empty:
        logging.error("Không tìm thấy dữ liệu nguồn, dừng pipeline.")
        return

    # 2. TRANSFORM
    df_cus_sach, df_rej_cus = lam_sach_khach_hang(df_cus_tho)
    df_ord_sach, df_itm_sach, df_rej_ord = lam_sach_don_hang(df_ord_tho, df_itm_tho)

    # Lọc theo tham số ngày nếu người dùng truyền vào
    if args.tu_ngay:
        df_ord_sach = df_ord_sach[df_ord_sach['ngay_chuan'].astype(str) >= args.tu_ngay]
    if args.den_ngay:
        df_ord_sach = df_ord_sach[df_ord_sach['ngay_chuan'].astype(str) <= args.den_ngay]

    df_reject_all = pd.concat([df_rej_cus, df_rej_ord], ignore_index=True)

    # 3. QUALITY
    df_ord_kiem = df_ord_tho.copy()
    df_ord_kiem['ngay_chuan'] = df_ord_kiem['ngay'].apply(doc_ngay)

    df_itm_kiem = df_itm_tho.copy()
    df_itm_kiem['so_luong'] = pd.to_numeric(df_itm_kiem['so_luong'], errors='coerce').fillna(0)
    df_itm_kiem['don_gia'] = pd.to_numeric(df_itm_kiem['don_gia'], errors='coerce').fillna(0)
    df_itm_kiem['thanh_tien'] = pd.to_numeric(df_itm_kiem['thanh_tien'], errors='coerce').fillna(0)

    ket_qua = [
        checks.cl1_dien_thoai_hop_le(df_cus_sach),
        checks.cl2_ngay_hop_le(df_ord_kiem),
        checks.cl3_tien_khop(df_itm_kiem),
        checks.cl4_khoa_khong_trung(df_ord_sach),
        checks.cl5_khoa_ngoai_ton_tai(df_itm_sach, df_ord_sach)
    ]

    # 4. LOAD STAGING & REJECT
    ghi_lo(df_cus_sach, batch_id, engine, table_name='staging_customers')
    ghi_lo(df_ord_sach, batch_id, engine, table_name='staging_orders')
    ghi_reject(df_reject_all, batch_id, engine, table_name='reject_rows')

    tong_vao = len(df_cus_tho) + len(df_ord_tho) + len(df_itm_tho)
    ghi_bao_cao(ket_qua, batch_id, so_dong_vao=tong_vao, so_reject=len(df_reject_all))

    # 5. LOAD DATA WAREHOUSE
    thong_ke_dwh = nap_kho_du_lieu(
        df_cus_sach, df_ord_sach, df_itm_sach, df_str_tho, df_prd_tho, engine
    )

    logging.info(f"Staging & Reject: Đã lưu {len(df_reject_all)} dòng lỗi vào reject_rows.")
    logging.info(f"Kho dữ liệu Star Schema đã nạp thành công: {thong_ke_dwh}")
    logging.info(f"=== Hoàn tất Pipeline! Báo cáo và log lưu tại thư mục reports/ ===")

if __name__ == '__main__':
    main()