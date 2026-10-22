-- Các bảng chiều (Dimension). Khóa nghiệp vụ dùng để nạp lại được.

CREATE TABLE IF NOT EXISTS dim_customer (
  customer_sk    INTEGER PRIMARY KEY AUTOINCREMENT,
  business_key   VARCHAR(220) NOT NULL UNIQUE,   -- khóa hợp nhất
  ho_ten         VARCHAR(160) NOT NULL,
  sdt_chuan      VARCHAR(10),
  tinh_thanh     VARCHAR(80),
  so_ban_ghi_goc INTEGER      NOT NULL DEFAULT 1,
  ngay_tao_dau   DATE,
  cap_nhat_luc   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_store (
  store_sk       INTEGER PRIMARY KEY AUTOINCREMENT,
  business_key   VARCHAR(20) NOT NULL UNIQUE,    -- ma_cua_hang
  ten_cua_hang   VARCHAR(160),
  thanh_pho      VARCHAR(80),
  quan_huyen     VARCHAR(80),
  ngay_khai_truong DATE,
  cap_nhat_luc   DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_ngay (
  ngay_key   INTEGER PRIMARY KEY,        -- định dạng 20260909
  ngay_day_du DATE NOT NULL,
  tuan_iso   INTEGER NOT NULL,
  thang      INTEGER NOT NULL,
  quy        INTEGER NOT NULL,
  nam        INTEGER NOT NULL
);