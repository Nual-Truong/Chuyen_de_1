#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_sample.py - Sinh du lieu mo phong bo sung cho case study Smart CRM - Mekong Mobile.
Chuyen de tot nghiep 1 - Khoa CNTT - Truong Dai hoc Van Lang.

Dung khi luong nghiep vu cua em can du lieu khong co san trong bo mau
(vi du luong L3 - co hoi ban hang, hoac luong L4 - lich hen ky thuat vien).

VI DU:
  # 500 co hoi ban hang cho luong L3
  python gen_sample.py --entity opportunity --rows 500 --seed 42 --out opportunities.csv

  # 1200 lich hen, gan voi cac phieu co san trong tickets_history.csv
  python gen_sample.py --entity appointment --rows 1200 --seed 42 \
                       --link ../tickets_history.csv --out appointments.csv

  # 3000 luot tuong tac chien dich marketing cho luong L1
  python gen_sample.py --entity campaign_touch --rows 3000 --seed 42 \
                       --link ../customers_raw.csv --out campaign_touches.csv

LUU Y QUAN TRONG:
  LUON dat --seed va GHI LAI gia tri seed trong README cua em.
  Day la dieu kien cua nguyen tac "tai lap duoc" ma hoc phan yeu cau:
  nguoi khac chay lai voi cung seed phai ra dung bo du lieu cua em.
"""
import argparse, csv, random, sys, os
from datetime import date, datetime, timedelta

D0 = date(2024, 7, 1)
D1 = date(2026, 8, 31)
NDAYS = (D1 - D0).days

HO = ['Nguyễn','Trần','Lê','Phạm','Hoàng','Huỳnh','Phan','Vũ','Võ','Đặng','Bùi','Đỗ','Ngô','Dương']
DEM = ['Văn','Thị','Hữu','Đức','Minh','Ngọc','Thanh','Quang','Xuân','Tuấn','Kim','Bảo','Gia']
TEN = ['An','Bình','Cường','Dung','Đạt','Giang','Hà','Hải','Hạnh','Hiếu','Huy','Khoa','Lan','Linh',
       'Long','Mai','Nam','Nga','Phong','Phúc','Quân','Sơn','Tâm','Thảo','Thu','Trang','Trung','Vy']

def ten_nguoi(rnd):
    return f'{rnd.choice(HO)} {rnd.choice(DEM)} {rnd.choice(TEN)}'

def read_ids(path, col):
    if not path or not os.path.exists(path):
        return []
    with open(path, encoding='utf-8') as f:
        r = csv.DictReader(f)
        if col not in (r.fieldnames or []):
            return []
        return [row[col] for row in r if row.get(col)]

# ---------------------------------------------------------------- opportunity (L3)
STAGES = ['TIEP_CAN', 'TU_VAN', 'BAO_GIA', 'CHOT', 'THAT_BAI']
NGUON  = ['Khach den cua hang', 'Goi dien den', 'Zalo', 'Facebook', 'Gioi thieu', 'Website']
LY_DO_THAT_BAI = ['Gia cao hon doi thu', 'Khach chua co nhu cau ngay', 'Het hang mau khach muon',
                  'Khach mua noi khac', 'Khong lien lac duoc']

def gen_opportunity(rnd, n, links):
    cust = links or [str(i) for i in range(1, 54001)]
    head = ['opportunity_id','customer_id','store_code','nguon','san_pham_quan_tam',
            'gia_tri_du_kien','stage','xac_suat','ngay_tao','ngay_cap_nhat','ly_do_that_bai','nhan_vien']
    rows = []
    for i in range(1, n + 1):
        created = D0 + timedelta(days=rnd.randint(0, NDAYS))
        r = rnd.random()
        if   r < 0.20: stage = 'TIEP_CAN'
        elif r < 0.42: stage = 'TU_VAN'
        elif r < 0.58: stage = 'BAO_GIA'
        elif r < 0.82: stage = 'CHOT'
        else:          stage = 'THAT_BAI'
        prob = {'TIEP_CAN':10, 'TU_VAN':30, 'BAO_GIA':60, 'CHOT':100, 'THAT_BAI':0}[stage]
        updated = created + timedelta(days=rnd.randint(0, 45))
        if updated > D1: updated = D1
        rows.append([i, rnd.choice(cust), f'MM{rnd.randint(1,24):03d}', rnd.choice(NGUON),
                     rnd.choice(['Điện thoại tầm trung','Điện thoại cao cấp','Máy tính bảng','Phụ kiện']),
                     rnd.choice([2490000, 4990000, 7990000, 11990000, 18990000, 27990000]),
                     stage, prob, created.isoformat(), updated.isoformat(),
                     rnd.choice(LY_DO_THAT_BAI) if stage == 'THAT_BAI' else '',
                     ten_nguoi(rnd)])
    return head, rows

# ---------------------------------------------------------------- appointment (L4)
KHUNG = [('08:00','10:00'), ('10:00','12:00'), ('13:30','15:30'), ('15:30','17:30')]
TRANG_THAI_LH = ['DA_DAT','DA_XAC_NHAN','HOAN_TAT','KHACH_HUY','KHACH_KHONG_DEN']

def gen_appointment(rnd, n, links):
    tickets = links or [str(i) for i in range(1, 7801)]
    head = ['appointment_id','ticket_id','technician_id','center_id','ngay_hen',
            'gio_bat_dau','gio_ket_thuc','loai','trang_thai','ghi_chu']
    rows = []
    for i in range(1, n + 1):
        d = D0 + timedelta(days=rnd.randint(30, NDAYS))
        k = rnd.choice(KHUNG)
        r = rnd.random()
        if   r < 0.62: st = 'HOAN_TAT'
        elif r < 0.78: st = 'DA_XAC_NHAN'
        elif r < 0.88: st = 'DA_DAT'
        elif r < 0.95: st = 'KHACH_HUY'
        else:          st = 'KHACH_KHONG_DEN'
        rows.append([i, rnd.choice(tickets), rnd.randint(1, 38), rnd.randint(1, 6),
                     d.isoformat(), k[0], k[1],
                     rnd.choice(['GIAO_MAY','NHAN_MAY','KIEM_TRA_TAI_CHO']), st,
                     rnd.choice(['', '', '', 'Khách hẹn lại lần 2', 'Khách đến sớm hơn giờ hẹn'])])
    return head, rows

# ---------------------------------------------------------------- campaign touch (L1)
KENH = ['SMS','ZALO','EMAIL','GOI_DIEN']
CHIEN_DICH = [('CD001','Uu dai sinh nhat'), ('CD002','Back to school'),
              ('CD003','Tri an khach hang VIP'), ('CD004','Giam gia phu kien'),
              ('CD005','Doi may cu lay may moi')]

def gen_campaign_touch(rnd, n, links):
    cust = links or [str(i) for i in range(1, 54001)]
    head = ['touch_id','campaign_code','campaign_name','customer_id','kenh',
            'ngay_gui','da_mo','da_click','da_mua_sau_30_ngay']
    rows = []
    for i in range(1, n + 1):
        cd = rnd.choice(CHIEN_DICH)
        kenh = rnd.choice(KENH)
        opened = rnd.random() < {'SMS':0.42,'ZALO':0.55,'EMAIL':0.18,'GOI_DIEN':0.70}[kenh]
        clicked = opened and rnd.random() < 0.22
        bought = clicked and rnd.random() < 0.14
        rows.append([i, cd[0], cd[1], rnd.choice(cust), kenh,
                     (D0 + timedelta(days=rnd.randint(0, NDAYS))).isoformat(),
                     'true' if opened else 'false',
                     'true' if clicked else 'false',
                     'true' if bought else 'false'])
    return head, rows

GEN = {'opportunity': (gen_opportunity, 'customer_id'),
       'appointment': (gen_appointment, 'ticket_id'),
       'campaign_touch': (gen_campaign_touch, 'record_id')}

def main():
    ap = argparse.ArgumentParser(description='Sinh du lieu mo phong bo sung cho case study Smart CRM.')
    ap.add_argument('--entity', required=True, choices=sorted(GEN), help='Loai thuc the can sinh')
    ap.add_argument('--rows', type=int, required=True, help='So dong can sinh')
    ap.add_argument('--seed', type=int, required=True, help='Seed ngau nhien - BAT BUOC de tai lap duoc')
    ap.add_argument('--out', required=True, help='Duong dan tep CSV dau ra')
    ap.add_argument('--link', help='Tep CSV de lay khoa ngoai co that (tuy chon)')
    a = ap.parse_args()

    if a.rows < 1:
        sys.exit('Loi: --rows phai lon hon 0')
    rnd = random.Random(a.seed)
    fn, link_col = GEN[a.entity]
    links = read_ids(a.link, link_col) if a.link else []
    if a.link and not links:
        print(f'Canh bao: khong doc duoc cot "{link_col}" tu {a.link}; se sinh khoa ngoai gia dinh.',
              file=sys.stderr)
    head, rows = fn(rnd, a.rows, links)
    with open(a.out, 'w', newline='', encoding='utf-8') as f:
        cw = csv.writer(f); cw.writerow(head); cw.writerows(rows)
    print(f'Da sinh {len(rows)} dong -> {a.out}  (entity={a.entity}, seed={a.seed})')
    print(f'GHI LAI trong README:  python gen_sample.py --entity {a.entity} '
          f'--rows {a.rows} --seed {a.seed} --out {os.path.basename(a.out)}')

if __name__ == '__main__':
    main()
