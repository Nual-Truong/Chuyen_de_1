-- Bảng staging: dữ liệu đã làm sạch, trước khi nạp vào dimension và fact.

CREATE TABLE IF NOT EXISTS staging_customers (
  batch_id       VARCHAR(40)  NOT NULL,
  record_id      BIGINT       NOT NULL,
  ho_ten         VARCHAR(160) NOT NULL,
  sdt_chuan      VARCHAR(10),
  email          VARCHAR(200),
  dia_chi        VARCHAR(300),
  tinh_thanh     VARCHAR(80),
  ngay_tao       DATE,
  khoa_hop_nhat  VARCHAR(220) NOT NULL,
  PRIMARY KEY (batch_id, record_id)
);
CREATE INDEX IF NOT EXISTS idx_stg_cus_khoa
  ON staging_customers(khoa_hop_nhat);

CREATE TABLE IF NOT EXISTS staging_orders (
  batch_id       VARCHAR(40)  NOT NULL,
  order_id       BIGINT       NOT NULL,
  ma_don         VARCHAR(40)  NOT NULL,
  ma_cua_hang    VARCHAR(20)  NOT NULL,
  ngay_chuan     DATE,
  ten_khach      VARCHAR(160),
  sdt_chuan      VARCHAR(10),
  thanh_tien     NUMERIC(14,2),
  khoa_hop_nhat  VARCHAR(220),
  PRIMARY KEY (batch_id, order_id)
);
CREATE INDEX IF NOT EXISTS idx_stg_ord_khoa
  ON staging_orders(ma_cua_hang, ma_don);