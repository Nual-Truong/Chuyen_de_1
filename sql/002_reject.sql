-- Bảng reject: NƠI CHỨA MỌI DÒNG KHÔNG XỬ LÝ ĐƯỢC.
-- Nguyên tắc: KHÔNG bao giờ âm thầm bỏ một dòng dữ liệu.

CREATE TABLE IF NOT EXISTS reject_rows (
  reject_id    BIGSERIAL PRIMARY KEY,
  batch_id     VARCHAR(40) NOT NULL,
  nguon        VARCHAR(80) NOT NULL,   -- tên tệp nguồn
  so_dong      INT         NOT NULL,   -- dòng thứ mấy trong tệp nguồn
  ma_quy_tac   VARCHAR(16) NOT NULL,   -- CL1..CL7 - quy tắc nào loại nó
  ly_do        TEXT        NOT NULL,   -- viết cho NGƯỜI đọc, không phải cho máy
  du_lieu_goc  TEXT        NOT NULL,   -- toàn bộ dòng gốc dưới dạng chuỗi/JSON để truy vết
  tao_luc      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_reject_batch
  ON reject_rows(batch_id, ma_quy_tac);