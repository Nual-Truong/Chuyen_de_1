-- Bảng sự kiện (Fact sales).
-- GRAIN: Một dòng fact = MỘT SẢN PHẨM trong MỘT ĐƠN HÀNG tại MỘT CỬA HÀNG vào MỘT NGÀY.

CREATE TABLE IF NOT EXISTS fact_sales (
  order_key     VARCHAR(60) NOT NULL,
  product_key   INTEGER     NOT NULL,
  date_key      INTEGER     NOT NULL REFERENCES dim_ngay(date_key),
  store_key     INTEGER     NOT NULL REFERENCES dim_store(store_key),
  customer_key  INTEGER     REFERENCES dim_customer(customer_sk),
  so_luong      INTEGER     NOT NULL DEFAULT 1,
  don_gia       NUMERIC(14,2) NOT NULL,
  thanh_tien    NUMERIC(14,2) NOT NULL,
  PRIMARY KEY (order_key, product_key)
);
CREATE INDEX IF NOT EXISTS idx_fact_date ON fact_sales(date_key);
CREATE INDEX IF NOT EXISTS idx_fact_store ON fact_sales(store_key);
CREATE INDEX IF NOT EXISTS idx_fact_customer ON fact_sales(customer_key);