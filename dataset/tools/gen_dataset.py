# -*- coding: utf-8 -*-
"""Sinh bo du lieu mau Mekong Mobile cho Chuyen de tot nghiep 1."""
import csv, random, os, unicodedata
from datetime import date, datetime, timedelta

random.seed(20260901)
OUT = '/tmp/course/dataset'
os.makedirs(OUT, exist_ok=True)

def w(name, header, rows):
    p = os.path.join(OUT, name)
    with open(p, 'w', newline='', encoding='utf-8') as f:
        cw = csv.writer(f); cw.writerow(header); cw.writerows(rows)
    print(f'  {name:28} {len(rows):>7} dong')
    return len(rows)

HO = ['Nguyễn','Trần','Lê','Phạm','Hoàng','Huỳnh','Phan','Vũ','Võ','Đặng','Bùi','Đỗ','Hồ','Ngô','Dương','Lý']
DEM = ['Văn','Thị','Hữu','Đức','Minh','Ngọc','Thanh','Quang','Hoài','Xuân','Tuấn','Kim','Bảo','Gia','Anh']
TEN = ['An','Bình','Cường','Dung','Đạt','Giang','Hà','Hải','Hạnh','Hiếu','Hoa','Huy','Khoa','Lan','Linh',
       'Long','Mai','Nam','Nga','Ngân','Nhung','Phong','Phúc','Quân','Quyên','Sơn','Tâm','Thảo','Thắng',
       'Thu','Trang','Trung','Tú','Tuyết','Vy','Yến','Duy','Khánh','Lâm','Mỹ','Như','Oanh','Phương','Vinh']

def no_dau(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return s.replace('đ','d').replace('Đ','D')

def ten_kh():
    return f'{random.choice(HO)} {random.choice(DEM)} {random.choice(TEN)}'

DAU_SO = ['090','091','093','094','096','097','098','032','033','034','035','036','037','038','039',
          '070','076','077','078','079','081','082','083','084','085','086','088','089']
def sdt():
    return random.choice(DAU_SO) + ''.join(random.choice('0123456789') for _ in range(7))

print('== SINH BO DU LIEU MEKONG MOBILE ==')

# ---------------------------------------------------------------- stores
TP = [('TP. Hồ Chí Minh', 14), ('Cần Thơ', 6), ('Hà Nội', 4)]
QUAN = {'TP. Hồ Chí Minh': ['Quận 1','Quận 3','Quận 5','Quận 7','Quận 10','Quận 11','Quận Bình Thạnh',
                            'Quận Gò Vấp','Quận Tân Bình','Quận Tân Phú','Quận Phú Nhuận','TP. Thủ Đức',
                            'Quận 12','Quận Bình Tân'],
        'Cần Thơ': ['Ninh Kiều','Bình Thủy','Cái Răng','Ô Môn','Thốt Nốt','Phong Điền'],
        'Hà Nội': ['Hoàn Kiếm','Cầu Giấy','Đống Đa','Hai Bà Trưng']}
stores = []; sid = 0
for tp, n in TP:
    for i in range(n):
        sid += 1
        q = QUAN[tp][i]
        stores.append([sid, f'MM{sid:03d}', f'Mekong Mobile {q}', tp, q,
                       (date(2015,3,1) + timedelta(days=random.randint(0, 3200))).isoformat()])
w('stores.csv', ['store_id','store_code','store_name','thanh_pho','quan_huyen','ngay_khai_truong'], stores)

# ---------------------------------------------------------------- service centers
CENTERS = [(1,'TTBH Quận 10','TP. Hồ Chí Minh'), (2,'TTBH Quận Tân Bình','TP. Hồ Chí Minh'),
           (3,'TTBH TP. Thủ Đức','TP. Hồ Chí Minh'), (4,'TTBH Ninh Kiều','Cần Thơ'),
           (5,'TTBH Cái Răng','Cần Thơ'), (6,'TTBH Cầu Giấy','Hà Nội')]
w('service_centers.csv', ['center_id','center_code','center_name','thanh_pho'],
  [[c[0], f'TT{c[0]:02d}', c[1], c[2]] for c in CENTERS])

# ---------------------------------------------------------------- products
BRANDS = [('Samsung', 'SS'), ('Xiaomi','XM'), ('OPPO','OP'), ('realme','RM'), ('vivo','VV'),
          ('Apple','AP'), ('Nokia','NK'), ('TECNO','TC')]
NHOM = ['Điện thoại phổ thông','Điện thoại tầm trung','Điện thoại cao cấp','Máy tính bảng','Phụ kiện']
products = []; pid = 0
for brand, bc in BRANDS:
    for k in range(40):
        pid += 1
        nhom = random.choices(NHOM, weights=[18,32,20,12,18])[0]
        if nhom == 'Phụ kiện':
            name = f'{brand} {random.choice(["Tai nghe","Sạc nhanh","Ốp lưng","Cáp Type-C","Pin dự phòng"])} {random.choice(["A","B","Pro","Lite"])}{random.randint(1,9)}'
            gia = random.choice([120000, 190000, 250000, 320000, 450000, 590000, 750000])
            bh = 6
        elif nhom == 'Máy tính bảng':
            name = f'{brand} Tab {random.choice(["S","M","A"])}{random.randint(5,12)}'
            gia = random.choice([4590000, 5990000, 7490000, 9990000, 12990000]); bh = 12
        elif nhom == 'Điện thoại cao cấp':
            name = f'{brand} {random.choice(["Ultra","Pro Max","Pro+"])} {random.randint(11,16)}'
            gia = random.choice([18990000, 22990000, 27990000, 31990000, 36990000]); bh = 12
        elif nhom == 'Điện thoại tầm trung':
            name = f'{brand} {random.choice(["Note","Neo","Plus","S"])} {random.randint(8,14)}'
            gia = random.choice([4990000, 6490000, 7990000, 9490000, 11990000]); bh = 12
        else:
            name = f'{brand} {random.choice(["Lite","Go","C","Y"])}{random.randint(2,9)}'
            gia = random.choice([1890000, 2490000, 2990000, 3490000, 3990000]); bh = 12
        products.append([pid, f'{bc}{pid:04d}', name, brand, nhom, gia, bh])
w('products.csv', ['product_id','product_code','product_name','thuong_hieu','nhom_san_pham','gia_niem_yet','warranty_months'], products)
PROD = {p[0]: p for p in products}

# ---------------------------------------------------------------- customers (raw, ban)
N_CUST = 54000
cust_clean = []       # ban ghi "that" de sinh don hang
for i in range(1, N_CUST + 1):
    cust_clean.append({'id': i, 'ten': ten_kh(), 'sdt': sdt(),
                       'ngay_tao': date(2024,1,1) + timedelta(days=random.randint(0, 970))})
# tao ban ghi raw co loi chat luong
raw = []
rid = 0
for c in cust_clean:
    n_ban = 1
    r = random.random()
    if r < 0.18: n_ban = 2          # ~18% trung lap
    elif r < 0.21: n_ban = 3
    for k in range(n_ban):
        rid += 1
        ten = c['ten']; s = c['sdt']; email = ''
        # bien the ten
        v = random.random()
        if k > 0:
            if v < 0.30: ten = no_dau(ten)
            elif v < 0.50: ten = ten.upper()
            elif v < 0.65: ten = ten.lower()
            elif v < 0.75: ten = '  ' + ten + ' '
        # bien the so dien thoai
        v = random.random()
        if v < 0.10: s = '84' + s[1:]
        elif v < 0.18: s = '+84' + s[1:]
        elif v < 0.26: s = f'{s[:4]} {s[4:7]} {s[7:]}'
        elif v < 0.30: s = f'{s[:4]}.{s[4:7]}.{s[7:]}'
        if random.random() < 0.062: s = ''          # ~6.2% thieu sdt
        if random.random() < 0.55:
            email = no_dau(ten.strip().split()[-1]).lower() + str(random.randint(1,999)) + random.choice(['@gmail.com','@yahoo.com','@outlook.com'])
        dc = f'{random.randint(1,300)} {random.choice(["Nguyễn Trãi","Lê Lợi","Trần Hưng Đạo","Cách Mạng Tháng 8","Điện Biên Phủ","3 Tháng 2","Hai Bà Trưng"])}, {random.choice(QUAN["TP. Hồ Chí Minh"] + QUAN["Cần Thơ"] + QUAN["Hà Nội"])}'
        if random.random() < 0.09: dc = ''
        raw.append([rid, ten, s, email, dc, c['ngay_tao'].isoformat()])
random.shuffle(raw)
for i, r in enumerate(raw, start=1): r[0] = i
w('customers_raw.csv', ['record_id','ho_ten','so_dien_thoai','email','dia_chi','ngay_tao'], raw)

# ---------------------------------------------------------------- orders + order_items
D0 = date(2024, 7, 1); D1 = date(2026, 8, 31)
NDAYS = (D1 - D0).days
def fmt_ngay(d):
    v = random.random()
    if v < 0.62: return d.strftime('%d/%m/%Y')
    elif v < 0.86: return f'{d.day}-{d.month}-{d.strftime("%y")}'
    else: return d.strftime('%Y.%m.%d')

NV = [f'{random.choice(["Anh","Chị"])} {random.choice(TEN)}' for _ in range(90)]
orders = []; items = []
oid = 0
# khach mua nhieu lan
buyers = random.sample(range(1, N_CUST + 1), 26000)
ma_don_pool = {}
for b_i, cid in enumerate(buyers):
    n_don = random.choices([1,2,3,4], weights=[62,24,10,4])[0]
    for k in range(n_don):
        oid += 1
        if oid > 26000: break
        d = D0 + timedelta(days=random.randint(0, NDAYS))
        st = random.choice(stores)
        # ma don do cua hang tu dat -> co trung giua cac cua hang
        seq = ma_don_pool.get(st[0], 0) + 1; ma_don_pool[st[0]] = seq
        ma_don = f'HD{seq:05d}' if random.random() < 0.6 else f'{st[1]}-{seq:04d}'
        c = cust_clean[cid - 1]
        s = c['sdt']
        v = random.random()
        if v < 0.12: s = '84' + s[1:]
        elif v < 0.20: s = f'{s[:4]} {s[4:7]} {s[7:]}'
        if random.random() < 0.058: s = ''
        n_item = random.choices([1,2,3], weights=[70,23,7])[0]
        tong = 0
        for _ in range(n_item):
            p = random.choice(products)
            sl = random.choices([1,2,3], weights=[88,9,3])[0]
            dg = int(p[5] * random.choice([1.0, 1.0, 1.0, 0.95, 0.9]))
            tt = sl * dg
            # ~1.5% dong thanh_tien sai
            tt_ghi = tt if random.random() > 0.015 else int(tt * random.choice([0.9, 1.1]))
            tong += tt_ghi
            items.append([oid, p[0], sl, dg, tt_ghi])
        tong_ghi = str(tong)
        if random.random() < 0.0085: tong_ghi = f'{tong:,}'.replace(',', '.') + 'đ'
        if random.random() < 0.011: tong_ghi = ''
        ten_ghi = c['ten']
        v = random.random()
        if v < 0.15: ten_ghi = no_dau(ten_ghi)
        elif v < 0.22: ten_ghi = ten_ghi.upper()
        nv = random.choice(NV) if random.random() > 0.038 else ''
        ngay = fmt_ngay(d) if random.random() > 0.004 else ''
        orders.append([oid, ma_don, st[1], ngay, ten_ghi, s, tong_ghi, nv,
                       random.choice(['', '', '', 'Khách hẹn lấy sau', 'Đã xuất hóa đơn VAT', 'Trả góp 0%'])])
    if oid > 26000: break
w('orders_2024_2026.csv',
  ['order_id','ma_don','ma_cua_hang','ngay','ten_khach','so_dien_thoai','thanh_tien','nhan_vien','ghi_chu'], orders)
w('order_items.csv', ['order_id','product_id','so_luong','don_gia','thanh_tien'], items)

# ---------------------------------------------------------------- technicians
LEVELS = ['SO_CAP','TRUNG_CAP','CAO_CAP']
CATS = [(1,'MAN_HINH','CAO'), (2,'PIN','TRUNG_BINH'), (3,'SAC','TRUNG_BINH'),
        (4,'PHAN_MEM','THAP'), (5,'NUOC_VAO','CAO'), (6,'KHAC','TRUNG_BINH')]
w('issue_categories.csv', ['category_id','category_name','default_priority','is_active'],
  [[c[0], c[1], c[2], 'true'] for c in CATS])

techs = []; skills = []
for t in range(1, 39):
    ctr = random.choice(CENTERS)[0]
    lv = random.choices(LEVELS, weights=[35,45,20])[0]
    techs.append([t, f'KT{t:03d}', ten_kh(), ctr, lv, 'true' if random.random() > 0.05 else 'false'])
    n_sk = random.randint(3, 5)
    for cat in random.sample([c[0] for c in CATS], n_sk):
        skills.append([t, cat, random.randint(2, 5)])
w('technicians.csv', ['technician_id','technician_code','ho_ten','center_id','level','is_active'], techs)
w('technician_skills.csv', ['technician_id','category_id','proficiency'], skills)

# ---------------------------------------------------------------- issue descriptions (co nhan)
TPL = {
 'MAN_HINH': ['màn hình bị sọc dọc', 'màn hình đen không lên', 'màn hình bị ám vàng một góc',
   'cảm ứng loạn không bấm được', 'màn hình nứt sau khi rơi', 'màn hình chớp tắt liên tục',
   'điểm chết trên màn hình', 'màn hình bị hở sáng viền dưới', 'cảm ứng chỗ được chỗ không',
   'màn hình xuất hiện vệt mực loang'],
 'PIN': ['pin tụt rất nhanh dùng 2 tiếng đã hết', 'máy phồng pin cấn màn hình', 'sạc đầy nhưng dùng 30 phút là sập nguồn',
   'pin chai chỉ còn dùng được nửa ngày', 'máy tự tắt khi còn 30% pin', 'pin nóng bất thường khi dùng',
   'báo pin sai phần trăm nhảy loạn', 'máy không giữ được pin qua đêm', 'pin sụt 20% chỉ sau vài phút'],
 'SAC': ['cắm sạc không vào điện', 'chân sạc lỏng phải giữ mới sạc được', 'sạc rất chậm mất cả đêm',
   'cắm sạc báo lỗi phụ kiện', 'cổng sạc bị gãy chân', 'sạc vào nhưng không nhận cáp',
   'cắm sạc máy nóng bất thường', 'cổng sạc bám bụi không tiếp xúc'],
 'PHAN_MEM': ['máy treo logo không vào được hệ điều hành', 'ứng dụng tự thoát liên tục',
   'máy chạy chậm giật lag sau khi cập nhật', 'quên mật khẩu không mở được máy',
   'máy tự khởi động lại nhiều lần trong ngày', 'không cài được ứng dụng báo lỗi',
   'wifi không kết nối được sau cập nhật', 'camera mở lên bị đen màn'],
 'NUOC_VAO': ['máy rơi vào nước không lên nguồn', 'điện thoại dính nước mưa loa bị rè',
   'máy bị đổ nước ngọt vào không sạc được', 'rơi bồn rửa máy chập chờn',
   'máy vào nước màn hình loang ố', 'dính nước biển máy nóng và tắt'],
 'KHAC': ['loa ngoài rè không nghe rõ', 'camera sau bị mờ như có sương',
   'máy rung liên tục không dừng', 'không nhận sim', 'nút nguồn bị kẹt',
   'máy có tiếng kêu lạ bên trong', 'mic gọi điện đối phương không nghe được'],
}
PREF = ['', 'khách báo ', 'kh nói ', 'khách hàng phản ánh ', 'may bi ', 'tình trạng: ']
SUF  = ['', ' đã thử khởi động lại không được', ' mới bị 2 ngày nay', ' bị từ tuần trước',
        ' xảy ra sau khi rơi', ' khách chưa từng sửa ở đâu', ' máy còn bảo hành']
target = {'MAN_HINH':1310, 'PIN':980, 'SAC':640, 'PHAN_MEM':520, 'NUOC_VAO':330, 'KHAC':220}
desc_rows = []; k = 0
for cat, n in target.items():
    for _ in range(n):
        k += 1
        t = random.choice(PREF) + random.choice(TPL[cat]) + random.choice(SUF)
        if random.random() < 0.16: t = no_dau(t)
        if random.random() < 0.08: t = t.upper()
        desc_rows.append([k, t.strip(), cat])
random.shuffle(desc_rows)
for i, r in enumerate(desc_rows, start=1): r[0] = i
w('issue_descriptions.csv', ['desc_id','issue_desc','issue_category'], desc_rows)

# ---------------------------------------------------------------- tickets + status log
STATUS = ['MOI','DA_PHAN_CONG','DANG_XU_LY','CHO_LINH_KIEN','HOAN_TAT','DA_DONG']
SLA_H = {'CAO':24, 'TRUNG_BINH':72, 'THAP':120}
CATID = {c[1]: c[0] for c in CATS}
tickets = []; logs = []; lid = 0
buyers_pool = buyers[:20000]
for t in range(1, 7801):
    cid = random.choice(buyers_pool)
    p = random.choice(products)
    d = D0 + timedelta(days=random.randint(60, NDAYS))
    hh = random.randint(8, 17); mm = random.choice([0,15,30,45])
    recv = datetime(d.year, d.month, d.day, hh, mm)
    dr = random.choice(desc_rows)
    cat = dr[2]; pr = dict((c[1], c[2]) for c in CATS)[cat]
    if random.random() < 0.18: pr = random.choice(['CAO','TRUNG_BINH','THAP'])
    due = recv + timedelta(hours=SLA_H[pr])
    ctr = random.choice(CENTERS)[0]
    # vong doi: chon duong di, co ca phieu dang o CHO_LINH_KIEN va HOAN_TAT
    r = random.random()
    if   r < 0.62: path = ['MOI','DA_PHAN_CONG','DANG_XU_LY','HOAN_TAT','DA_DONG']
    elif r < 0.82: path = ['MOI','DA_PHAN_CONG','DANG_XU_LY','CHO_LINH_KIEN','HOAN_TAT','DA_DONG']
    elif r < 0.88: path = ['MOI','DA_PHAN_CONG','DANG_XU_LY']
    elif r < 0.93: path = ['MOI','DA_PHAN_CONG','DANG_XU_LY','CHO_LINH_KIEN']
    elif r < 0.97: path = ['MOI','DA_PHAN_CONG','DANG_XU_LY','HOAN_TAT']
    else:          path = ['MOI','DA_PHAN_CONG']
    tech = random.choice([x for x in techs if x[3] == ctr] or techs)[0] if len(path) > 1 else ''
    # tong thoi gian xu ly: ~15% vuot han cam ket (khop van de V2 cua case study)
    if random.random() < 0.15:
        factor = random.uniform(1.05, 2.6)
    else:
        factor = random.uniform(0.25, 0.92)
    total_h = SLA_H[pr] * factor
    n_step = max(1, len(path) - 1)
    weights = [random.uniform(0.5, 1.5) for _ in range(n_step)]
    ws = sum(weights)
    steps = [total_h * x / ws for x in weights]
    cur = recv; closed = ''
    for i, st in enumerate(path):
        lid += 1
        if i > 0:
            cur = cur + timedelta(hours=steps[i-1])
        logs.append([lid, t, path[i-1] if i > 0 else '', st,
                     cur.isoformat(sep=' ', timespec='minutes'), random.randint(1, 60), ''])
        if st == 'DA_DONG': closed = cur.isoformat(sep=' ', timespec='minutes')
    status = path[-1]
    is_wr = 'true' if random.random() < 0.74 else 'false'
    tickets.append([t, f'BH-{t:06d}/{d.year}', cid, f'SN{random.randint(10**11, 10**12-1)}', p[0], ctr,
                    dr[1], CATID[cat], pr, status, tech, recv.isoformat(sep=' ', timespec='minutes'),
                    due.isoformat(sep=' ', timespec='minutes'), closed, is_wr])
w('tickets_history.csv',
  ['ticket_id','ticket_code','customer_id','serial_no','product_id','center_id','issue_desc',
   'category_id','priority','status','technician_id','received_at','due_date','closed_at','is_warranty'], tickets)
w('ticket_status_log.csv',
  ['log_id','ticket_id','from_status','to_status','changed_at','changed_by','note'], logs)

# ---------------------------------------------------------------- parts + transactions
PART_TPL = [('Màn hình', 'MH'), ('Pin', 'PIN'), ('Cổng sạc', 'CS'), ('Camera sau', 'CAM'),
            ('Loa ngoài', 'LOA'), ('Mic', 'MIC'), ('Nút nguồn', 'NN'), ('Cáp màn hình', 'CMH'),
            ('Khay sim', 'KS'), ('Keo dán màn', 'KD')]
parts = []; k = 0
for nm, pc in PART_TPL:
    for brand, bc in BRANDS[:6]:
        for v in range(3):
            k += 1
            parts.append([k, f'{pc}-{bc}-{v+1:02d}', f'{nm} {brand} loại {v+1}',
                          random.choice([150000, 280000, 420000, 650000, 980000, 1450000, 2200000])])
parts = parts[:180]
w('parts.csv', ['part_id','part_code','part_name','unit_price'], parts)
ptx = []; tx = 0
stock = {}
for c in CENTERS:
    for p in parts:
        if random.random() < 0.55:
            q = random.randint(2, 40); stock[(c[0], p[0])] = q
            tx += 1
            ptx.append([tx, c[0], p[0], 'NHAP', q,
                        (D0 + timedelta(days=random.randint(0, 120))).isoformat(), ''])
for t in tickets:
    if t[9] in ('HOAN_TAT','DA_DONG') and random.random() < 0.62:
        cand = [k2 for k2 in stock if k2[0] == t[5] and stock[k2] > 0]
        if not cand: continue
        key = random.choice(cand); q = min(stock[key], random.choices([1,2], weights=[92,8])[0])
        stock[key] -= q; tx += 1
        ptx.append([tx, key[0], key[1], 'XUAT', q, t[11][:10], t[1]])
    if random.random() < 0.04:
        c2 = random.choice(CENTERS)[0]; p2 = random.choice(parts)[0]
        q = random.randint(5, 30); stock[(c2, p2)] = stock.get((c2, p2), 0) + q; tx += 1
        ptx.append([tx, c2, p2, 'NHAP', q, (D0 + timedelta(days=random.randint(120, NDAYS))).isoformat(), ''])
ptx.sort(key=lambda r: r[5])
for i, r in enumerate(ptx, start=1): r[0] = i
w('part_transactions.csv', ['transaction_id','center_id','part_id','loai','so_luong','ngay','ticket_code'], ptx)
w('part_stock.csv', ['center_id','part_id','quantity','min_threshold'],
  [[k2[0], k2[1], v, random.choice([3,5,8])] for k2, v in sorted(stock.items())])

# ---------------------------------------------------------------- survey responses
CMT = {5: ['Nhân viên nhiệt tình, sửa nhanh', 'Rất hài lòng, máy chạy tốt lại', 'Dịch vụ tốt sẽ quay lại',
           'Kỹ thuật viên giải thích rõ ràng', 'Trả máy đúng hẹn'],
       4: ['Ổn, chỉ hơi lâu một chút', 'Hài lòng nhưng chỗ ngồi chờ hơi chật', 'Sửa được nhưng phải chờ linh kiện',
           'Tốt, giá hơi cao'],
       3: ['Bình thường', 'Máy sửa xong nhưng vẫn hơi nóng', 'Chờ hơi lâu', 'Tạm được'],
       2: ['Trả máy trễ hẹn 3 ngày', 'Gọi điện không ai nghe máy', 'Phải quay lại lần 2 mới xong',
           'Nhân viên trả lời không rõ ràng'],
       1: ['Sửa xong vẫn bị lỗi cũ', 'Trễ hẹn cả tuần không ai báo', 'Thái độ nhân viên không tốt',
           'Mất phụ kiện kèm theo máy']}
srv = []; k = 0
closed_t = [t for t in tickets if t[9] == 'DA_DONG']
for t in random.sample(closed_t, min(2600, len(closed_t))):
    k += 1
    sc = random.choices([5,4,3,2,1], weights=[42,28,15,9,6])[0]
    cm = random.choice(CMT[sc]) if random.random() < 0.72 else ''
    dt = datetime.fromisoformat(t[13]) + timedelta(days=random.randint(1, 5))
    srv.append([k, t[0], sc, cm, dt.isoformat(sep=' ', timespec='minutes')])
w('survey_responses.csv', ['response_id','ticket_id','score','comment','responded_at'], srv)

print('\nHoan tat. Thu muc:', OUT)
