"""Constants for Giá Thành (Product Costing) module."""

LOAI_DOI_TUONG = [
    ("san_pham", "Sản phẩm"),
    ("don_hang", "Đơn hàng"),
    ("phan_xuong", "Phân xưởng"),
]

LOAI_KHOAN_MUC = [
    ("nguyen_vat_lieu", "Nguyên vật liệu trực tiếp"),
    ("nhan_cong", "Nhân công trực tiếp"),
    ("san_xuat_chung", "Chi phí sản xuất chung"),
]

PHUONG_PHAP_PHAN_BO = [
    ("truc_tiep", "Trực tiếp"),
    ("he_so", "Hệ số"),
    ("ty_le", "Tỷ lệ"),
    ("dinh_muc", "Định mức"),
]

TIEU_THUC_PHAN_BO = [
    ("gio_cong", "Giờ công"),
    ("gio_may", "Giờ máy"),
    ("chi_phi_nvl", "Chi phí NLVL"),
    ("chi_phi_truc_tiep", "Chi phí trực tiếp"),
]

TRANG_THAI = [
    ("draft", "Nháp"),
    ("posted", "Đã ghi sổ"),
]
