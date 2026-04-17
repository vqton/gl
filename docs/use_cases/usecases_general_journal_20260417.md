<!-- 
📁 FILE NAME: usecases_general_journal_20260417.md
🕐 Ngày trích xuất: 2026-04-17
🔗 URL gốc: https://ketoanthienung.net/mau-so-nhat-ky-chung-theo-thong-tu-99-va-cach-lap.htm
📦 Độ sâu duyệt: 1 cấp
-->

# 📋 Use Cases Sổ Nhật Ký Chung (TT99)
*Based on Thông tư 99/2025/TT-BTC*

---

## 🗂️ Mục lục nguồn đã duyệt
| Cấp | URL | Trạng thái |
|-----|-----|------------|
| 1 | https://ketoanthienung.net/mau-so-nhat-ky-chung-theo-thong-tu-99-va-cach-lap.htm | ✅ |

---

## 📦 Use Cases

### 📌 [NKC-01] Ghi chép nghiệp vụ phát sinh vào Sổ Nhật ký chung
🔗 Nguồn: [Cấp 1]

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán / `Secondary:` Thủ quỹ |
| **Mục tiêu** | Ghi nhận mọi nghiệp vụ kinh tế tài chính phát sinh theo trình tự thời gian |
| **Tiên quyết** | Có chứng từ gốc hợp lệ |
| **Kích hoạt** | Phát sinh nghiệp vụ kinh tế |

#### 🔄 Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Xác định ngày ghi sổ |
| 2 | Kế toán | Ghi số hiệu và ngày tháng chứng từ |
| 3 | Kế toán | Ghi diễn giải nội dung nghiệp vụ |
| 4 | Kế toán | Ghi tài khoản Nợ (trước), tài khoản Có (sau) |
| 5 | Kế toán | Ghi số tiền phát sinh Nợ và Có |
| 6 | Hệ thống | Kiểm tra tổng Nợ = Tổng Có |

✅ **Hậu kiểm:** Bút toán cân bằng, đã ghi vào Sổ Nhật ký

---

### 📌 [NKC-02] Chuyển trang và cộng số phát sinh lũy kế
🔗 Nguồn: [Cấp 1] | Mẫu S03a-DN

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán |
| **Mục tiêu** | Chuyển số liệu sang trang mới và tính cộng lũy kế |

#### 🔄 Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Hệ thống | Tính tổng phát sinh Nợ từ đầu kỳ đến trang này |
| 2 | Hệ thống | Tính tổng phát sinh Có từ đầu kỳ đến trang này |
| 3 | Hệ thống | Ghi "Cộng chuyển sang trang sau" |
| 4 | Hệ thống | Đầu trang mới ghi "Số trang trước chuyển sang" |

✅ **Hậu kiểm:** Tổng Nợ = Tổng Có (cửa sổ)

---

### 📌 [NKC-03] Mở và sử dụng Sổ Nhật ký đặc biệt
🔗 Nguồn: [Cấp 1]

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán |
| **Mục tiêu** | Giảm khối lượng ghi chép khi có nhiều giao dịch cùng loại |

#### 🔄 Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | KT trưởng | Quyết định mở NK đặc biệt (thu tiền, chi tiền, mua, bán) |
| 2 | Kế toán | Ghi các nghiệp vụ vào NK đặc biệt |
| 3 | Hệ thống | Đánh dấu đã ghi NK đặc biệt (ko lặp vào NKC) |
| 4 | Hệ thống | Dùng NK đặc biệt để ghi Sổ Cái |

#### ⚠️ Luồng thay thế/Ngoại lệ
| Bước gốc | Điều kiện | Xử lý |
|----------|-----------|-------|
| [1] | DN lớn, nhiều phát sinh | Mở Sổ Nhật ký thu tiền (S03a1-DN) |
| [1] | DN thương mại | Mở Sổ Nhật ký mua hàng (S03a3-DN) |
| [1] | DN sản xuất | Mở Sổ Nhật ký mua hàng + bán hàng |

✅ **Hậu kiểm:** Không trùng lặp với NKChung

---

### 📌 [NKC-04] Kiểm tra và đối chiếu sổ Nhật ký chung
🔗 Nguồn: [Cấp 1]

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán / `Secondary:` Kế toán trưởng |
| **Mục tiêu** | Đảm bảo tính chính xác trước khi ghi Sổ Cái |

#### 🔄 Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Kiểm tra tổng Nợ = Tổng Có mỗi bút toán |
| 2 | Kế toán | Đánh dấu "Đã ghi Sổ Cái" (cột E) |
| 3 | Kế toán | Đối chiếu với chứng từ gốc |
| 4 | KT trưởng | Xác nhận và ký duyệt |

✅ **Hậu kiểm:** Tất cả bút toán đã đối chiếu

---

### 📌 [NKC-05] Khóa sổ Nhật ký chung cuối kỳ
🔗 Nguồn: [Cấp 1]

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán / `Secondary:` Kế toán trưởng |
| **Mục tiêu** | Cộng tổng phát sinh và chuyển sang kỳ sau |

#### 🔄 Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Tính cộng tổng phát sinh Nợ lũy kế trong kỳ |
| 2 | Kế toán | Tính cộng tổng phát sinh Có lũy kế trong kỳ |
| 3 | Kế toán | Ghi số trang, ngày mở sổ |
| 4 | KT trưởng | Ký xác nhận, đóng dấu |

#### ⚠️ Luồng thay thế
| Bước gốc | Điều kiện | Xử lý |
|----------|-----------|-------|
| [2] | Tổng Nợ ≠ Tổng Có | Báo lỗi, tìm nguyên nhân sai sót |

✅ **Hậu kiểm:** Sổ khóa, số liệu sang Sổ Cái

---

### 📌 [NKC-06] Định khoản kế toán (Account Codes)
🔗 Nguồn: [Cấp 1]

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán |
| **Mục tiêu** | Xác định đúng tài khoản Nợ/Có theo chuẩn TT99 |

#### 🔄 Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Xác định đối tượng (KH, NCC, hàng hóa...) |
| 2 | Kế toán | Chọn TK ghi Nợ trước (cột 1) |
| 3 | Kế toán | Chọn TK ghi Có sau (cột 2) |
| 4 | Kế toán | Mỗi TK một dòng riêng |

✅ **Hậu kiểm:** Định khoản đúng theo Thông tư 99

---

## Mẫu Sổ Nhật Ký Chung (S03a-DN)

```
| A      | B, C    | D       | E    | G  | H      | 1     | 2     |
|--------|---------|---------|------|----|--------|-------|-------|
|Ngày... | Số CT...| Diễn giải|Đã ghi|STT | TK Nợ/Có| Nợ    | Có    |
```

**Cột:**
- A: Ngày, tháng ghi sổ
- B, C: Số hiệu + ngày tháng chứng từ
- D: Diễn giải nội dung
- E: Đánh dấu đã ghi Sổ Cái
- G: Số thứ tự dòng
- H: Số hiệu tài khoản đối ứng
- 1: Phát sinh Nợ
- 2: Phát sinh Có

---

## Special Journals (Nhật ký đặc biệt)

| Mã mẫu | Tên sổ | Mục đích |
|--------|--------|----------|
| S03a1-DN | Nhật ký thu tiền | Theo dõi thu hàng ngày |
| S03a2-DN | Nhật ký chi tiền | Theo dõi chi hàng ngày |
| S03a3-DN | Nhật ký mua hàng | Theo dõi mua hàng NK |
| S03a4-DN | Nhật ký bán hàng | Theo dõi bán hàng NK |

---

## QUY TẮC THEO TT99

1. **Nguyên tắc:** Mọi nghiệp vụ KT phát sinh phải ghi vào Sổ Nhật ký chung
2. **Định khoản:** Tài khoản ghi Nợ trước, Tài khoản ghi Có sau
3. **Cân bằng:** Tổng Nợ = Tổng Có mỗi bút toán
4. **Cá nhân hóa:** DN được sửa đổi mẫu nhưng phải đáp ứng Điều 24 Luật Kế toán

---

*Nguồn: ketoanthienung.net / Thông tư 99/2025/TT-BTC*