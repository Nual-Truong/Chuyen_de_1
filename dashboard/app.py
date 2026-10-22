import os
import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine, text

# Cấu hình trang
st.set_page_config(page_title='Mekong Mobile - Dashboard', layout='wide')
st.title('📊 Dashboard Phân Tích Dữ Liệu Mekong Mobile')

# Kết nối CSDL SQLite
@st.cache_resource
def lay_engine():
    return create_engine('sqlite:///data/mekong_dw.db', pool_pre_ping=True)

@st.cache_data(ttl=300)
def doc_du_lieu(sql: str, tham: dict = None):
    with lay_engine().connect() as conn:
        return pd.read_sql(text(sql), conn, params=tham or {})

# Bộ lọc thời gian
st.markdown('### 📅 Bộ lọc thời gian')
c1, c2 = st.columns(2)
tu_ngay = c1.date_input('Từ ngày', pd.Timestamp('2024-01-01'))
den_ngay = c2.date_input('Đến ngày', pd.Timestamp('2026-12-31'))

# ==========================================
# TRẠNG THÁI 1: ĐANG TẢI (LOADING)
# ==========================================
with st.spinner('Đang truy vấn kho dữ liệu...'):
    try:
        # Khung 1: Tổng doanh thu theo cửa hàng (US1)
        sql_doanh_thu = """
            SELECT ds.ten_cua_hang, SUM(f.thanh_tien) AS tong_doanh_thu
            FROM fact_sales f
            JOIN dim_store ds ON f.store_key = ds.store_key
            JOIN dim_date dn ON f.date_key = dn.date_key
            WHERE dn.full_date BETWEEN :tu AND :den
            GROUP BY ds.ten_cua_hang
            ORDER BY tong_doanh_thu DESC
        """
        df_doanh_thu = doc_du_lieu(sql_doanh_thu, {'tu': tu_ngay.strftime('%Y-%m-%d'), 'den': den_ngay.strftime('%Y-%m-%d')})
        
        # Khung 2: Doanh thu theo nhóm sản phẩm (US4)
        sql_san_pham = """
            SELECT dp.nhom_san_pham, SUM(f.thanh_tien) AS tong_doanh_thu
            FROM fact_sales f
            JOIN dim_product dp ON f.product_key = dp.product_key
            JOIN dim_date dn ON f.date_key = dn.date_key
            WHERE dn.full_date BETWEEN :tu AND :den
            GROUP BY dp.nhom_san_pham
            ORDER BY tong_doanh_thu DESC
        """
        df_san_pham = doc_du_lieu(sql_san_pham, {'tu': tu_ngay.strftime('%Y-%m-%d'), 'den': den_ngay.strftime('%Y-%m-%d')})

        # Khung 3: Tỉ lệ khách hàng quay lại mua hàng (US3 - Retention)
        sql_retention = """
            SELECT 
                CASE WHEN so_don >= 2 THEN 'Khách quay lại (>=2 đơn)' 
                     ELSE 'Khách mua 1 lần' END AS nhom_khach,
                COUNT(customer_key) as so_luong
            FROM (
                SELECT customer_key, COUNT(DISTINCT order_key) as so_don
                FROM fact_sales
                WHERE customer_key != -1
                GROUP BY customer_key
            ) t
            GROUP BY nhom_khach
        """
        df_retention = doc_du_lieu(sql_retention)

    except Exception as e:
        # ==========================================
        # TRẠNG THÁI 3: LỖI (ERROR)
        # ==========================================
        st.error('Không đọc được dữ liệu từ kho dữ liệu. Kiểm tra kết nối rồi thử lại.')
        st.caption(f'Chi tiết kỹ thuật: {type(e).__name__}')
        st.stop()

# ==========================================
# TRẠNG THÁI 2: RỖNG (EMPTY)
# ==========================================
if df_doanh_thu.empty:
    st.info('Không có đơn hàng nào trong khoảng thời gian đã chọn. Thử mở rộng khoảng ngày, hoặc kiểm tra lại pipeline nạp dữ liệu.')
    st.stop()

# ==========================================
# HIỂN THỊ 3 KHUNG DASHBOARD (WIREFRAME 3 MÀN HÌNH)
# ==========================================
st.markdown('---')

col1, col2 = st.columns(2)

with col1:
    # --- Khung 1: Bar Chart Doanh Thu ---
    st.subheader('1. Tổng doanh thu theo cửa hàng')
    tb_doanh_thu = df_doanh_thu['tong_doanh_thu'].mean()
    fig1 = px.bar(
        df_doanh_thu.sort_values('tong_doanh_thu'), 
        x='tong_doanh_thu', y='ten_cua_hang', orientation='h',
        labels={'tong_doanh_thu': 'Doanh thu (VNĐ)', 'ten_cua_hang': ''}
    )
    fig1.add_vline(x=tb_doanh_thu, line_dash='dash', line_color='red',
                   annotation_text=f'Trung bình: {tb_doanh_thu:,.0f} VNĐ')
    st.plotly_chart(fig1, use_container_width=True)
    st.caption(f'Nguồn: fact_sales · {len(df_doanh_thu)} cửa hàng · Từ {tu_ngay.strftime("%d/%m/%Y")} đến {den_ngay.strftime("%d/%m/%Y")}')

with col2:
    # --- Khung 2: Bar Chart Nhóm Sản Phẩm ---
    st.subheader('2. Doanh thu theo nhóm sản phẩm')
    tb_sp = df_san_pham['tong_doanh_thu'].mean()
    fig2 = px.bar(
        df_san_pham.sort_values('tong_doanh_thu'), 
        x='tong_doanh_thu', y='nhom_san_pham', orientation='h',
        labels={'tong_doanh_thu': 'Doanh thu (VNĐ)', 'nhom_san_pham': ''},
        color_discrete_sequence=['#17becf']
    )
    fig2.add_vline(x=tb_sp, line_dash='dot', line_color='orange',
                   annotation_text=f'Trung bình: {tb_sp:,.0f} VNĐ')
    st.plotly_chart(fig2, use_container_width=True)
    st.caption(f'Nguồn: fact_sales và dim_product · Khoảng thời gian đã chọn')

st.markdown('---')

# --- Khung 3: Pie Chart Tỉ Lệ Khách Quay Lại (Retention Rate - US3) ---
st.subheader('3. Tỉ lệ khách hàng quay lại mua hàng (Retention Rate)')
if not df_retention.empty:
    fig3 = px.pie(
        df_retention, 
        names='nhom_khach', values='so_luong', 
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.caption('Nguồn: fact_sales (Đếm phân biệt đơn hàng nhóm theo định danh khách hàng đã che bảo mật)')
else:
    st.warning('Chưa có đủ dữ liệu để tính tỉ lệ khách quay lại.')