from datetime import date
import pytest
from src.transform import rules

# Test 1: Luồng đúng (Đưa SĐT bị dính dấu chấm, mã vùng về chuẩn 10 số)
@pytest.mark.parametrize('tho, mong_doi', [
    ('0763247885', '0763247885'),
    ('0760.833.592', '0760833592'),
    ('076 083 3592', '0760833592'),
    ('+84760833592', '0760833592')
])
def test_TR01_chuan_hoa_dien_thoai(tho, mong_doi):
    assert rules.chuan_hoa_dien_thoai(tho) == mong_doi

# Test 2: Xử lý 3 định dạng ngày (Luồng đúng)
@pytest.mark.parametrize('tho, mong_doi', [
    ('17/08/2025', date(2025, 8, 17)), 
    ('17-8-25', date(2025, 8, 17)), 
    ('2025.08.17', date(2025, 8, 17))
])
def test_TR02_doc_ba_khuon_ngay(tho, mong_doi):
    assert rules.doc_ngay(tho) == mong_doi

# Test 3: Giá trị biên (Chỉ 10 chữ số mới đạt, 9 số hoặc 11 số phải báo None)
@pytest.mark.parametrize('tho', ['076083359', '07608335921'])
def test_TR03_bien_do_dai_sdt(tho):
    assert rules.chuan_hoa_dien_thoai(tho) is None

# Test 4: Dữ liệu sai (Dữ liệu bị rỗng hoặc chuỗi rác)
@pytest.mark.parametrize('tho', [None, '', '   ', 'abc'])
def test_TR04_du_lieu_rac(tho):
    assert rules.chuan_hoa_dien_thoai(tho) is None
    assert rules.doc_ngay(tho) is None