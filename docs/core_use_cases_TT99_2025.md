# Core Use Cases Kế Toán theo Thông tư 99/2025/TT-BTC

> **Căn cứ pháp lý:** Thông tư 99/2025/TT-BTC — hiệu lực từ 01/01/2026  
> **Hệ thống TK:** 71 TK cấp 1 · 101 TK cấp 2 · 10 TK cấp 3 · 2 TK cấp 4  
> **Phạm vi:** Doanh nghiệp áp dụng chế độ kế toán đầy đủ (thay thế TT200/2014)

---

## Mục lục

1. [Phân tích cấu trúc COA](#1-phân-tích-cấu-trúc-coa)
2. [Danh sách đầy đủ Use Cases](#2-danh-sách-đầy-đủ-use-cases)
   - [Domain: Bán hàng & Doanh thu](#21-domain-bán-hàng--doanh-thu)
   - [Domain: Mua hàng & Nhập kho](#22-domain-mua-hàng--nhập-kho)
   - [Domain: Thanh toán & Tiền](#23-domain-thanh-toán--tiền)
   - [Domain: Thuế](#24-domain-thuế)
   - [Domain: Tài sản & Hàng tồn kho](#25-domain-tài-sản--hàng-tồn-kho)
   - [Domain: Lương & Bảo hiểm xã hội](#26-domain-lương--bảo-hiểm-xã-hội)
   - [Domain: Kết chuyển cuối kỳ & Điều chỉnh](#27-domain-kết-chuyển-cuối-kỳ--điều-chỉnh)
3. [Core Use Case Shortlist — 22 nghiệp vụ bắt buộc](#3-core-use-case-shortlist--22-nghiệp-vụ-bắt-buộc)
4. [Kiểm tra vòng kế toán](#4-kiểm-tra-vòng-kế-toán)

---

## 1. Phân tích cấu trúc COA

### Nhóm tài khoản theo chức năng

| Nhóm | Tài khoản | Chức năng | Báo cáo |
|------|-----------|-----------|---------|
| **Tiền & tương đương tiền** | 111, 112, 113 | Theo dõi luồng tiền vào/ra. Dư Nợ = tài sản thanh khoản cao nhất. Là đích đến/xuất phát của mọi giao dịch thanh toán. | BCĐKT A.I |
| **Phải thu** | 131, 133, 138, 141 | Quyền đòi tiền từ bên ngoài. 131 phát sinh khi bán chịu. 1331 ghi nhận VAT đầu vào được khấu trừ. 141 tạm ứng nội bộ. | BCĐKT A.II |
| **Hàng tồn kho** | 151, 152, 153, 154, 155, 156, 157 | Tài sản vật chất trong chu trình SXKD. Xuất kho → 632. Nhập từ mua → Nợ TK kho / Có 331 hoặc 112. | BCĐKT A.III |
| **Tài sản cố định** | 211, 212, 213, 214, 241, 242 | Tài sản dài hạn. 214 là TK điều chỉnh (Dư Có). KH hàng tháng: Nợ 627/641/642 / Có 214. | BCĐKT B.I |
| **Phải trả** | 331, 333, 334, 335, 338, 341 | Nghĩa vụ nợ. 331 mua chịu. 333 thuế. 334 lương. 341 vay dài/ngắn hạn. | BCĐKT C |
| **Doanh thu & giảm trừ** | 511, 515, 521 | 511 Dư Có trong kỳ, kết chuyển về 911. 521 là TK giảm trừ (Dư Nợ): chiết khấu, hàng trả lại, giảm giá. | BCKQHĐKD |
| **Chi phí SXKD** | 621, 622, 627, 632, 635, 641, 642 | 621/622/627 → 154 → 632. Chi phí kỳ (641/642/635) kết chuyển thẳng về 911. | BCKQHĐKD |
| **TN khác, CP khác & Kết quả** | 711, 811, 821, 911 | 711/811 hoạt động ngoài chính. 821 thuế TNDN (hiện hành + hoãn lại). 911 là TK trung gian xác định lãi/lỗ. | BCKQHĐKD |

---

## 2. Danh sách đầy đủ Use Cases

---

### 2.1 Domain: Bán hàng & Doanh thu

> **TK chủ lực:** 511, 515, 521, 131, 33311, 632, 155, 156

---

#### S01 ★ CORE — Bán hàng thu tiền ngay (có VAT)

**Mô tả:** Khách hàng thanh toán ngay khi nhận hàng/dịch vụ. Doanh thu và thuế GTGT đầu ra được ghi nhận đồng thời.

**Trigger:** Xuất hóa đơn GTGT, nhận tiền mặt hoặc chuyển khoản.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 111 / 112 | Tổng tiền thu (giá + VAT) |
| Có | 511 | Doanh thu chưa VAT |
| Có | 33311 | Thuế GTGT đầu ra |

**TK liên quan:** `111`, `112`, `511`, `33311`

**Edge cases:**
- Chiết khấu TM → Nợ 521 / Có 131
- Hàng trả lại → bút toán đảo
- Xuất ngoại tệ → xử lý chênh lệch tỷ giá 413

---

#### S02 ★ CORE — Bán hàng ghi công nợ (bán chịu)

**Mô tả:** Xuất hàng, ghi nhận phải thu khách hàng. Tiền về sau. Phổ biến nhất trong thực tế B2B.

**Trigger:** Xuất hóa đơn GTGT, chưa thu tiền.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 131 | Phải thu KH (gồm VAT) |
| Có | 511 | Doanh thu |
| Có | 33311 | Thuế GTGT đầu ra |

**TK liên quan:** `131`, `511`, `33311`

**Edge cases:**
- Khách nợ quá hạn → lập dự phòng 2293
- Chiết khấu thanh toán → Nợ 635 / Có 131

---

#### S03 ★ CORE — Xuất kho ghi nhận giá vốn

**Mô tả:** Song song với bút toán doanh thu, hệ thống ghi nhận giá vốn hàng bán để đủ chu trình doanh thu - chi phí.

**Trigger:** Xuất kho hàng hóa/thành phẩm giao khách.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 632 | Giá vốn hàng bán |
| Có | 156 / 155 | Hàng hóa / Thành phẩm xuất kho |

**TK liên quan:** `632`, `155`, `156`

**Edge cases:**
- Phương pháp tính giá xuất kho (FIFO/BQGQ) phải nhất quán
- Hàng bị trả lại → nhập kho ngược, đảo 632

---

#### S04 — Chiết khấu thương mại, giảm giá hàng bán

**Mô tả:** Giảm trừ doanh thu khi đã xuất hóa đơn. Ảnh hưởng đến doanh thu thuần trên P&L.

**Trigger:** Phát sinh chiết khấu TM hoặc giảm giá theo hợp đồng.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 521 | Khoản giảm trừ doanh thu |
| Có | 131 / 111 | Giảm công nợ hoặc trả tiền lại |

**TK liên quan:** `521`, `131`, `111`

**Edge cases:**
- Đã xuất VAT → cần xuất hóa đơn điều chỉnh, điều chỉnh 33311

---

#### S05 — Hàng bán bị trả lại

**Mô tả:** Khách hàng trả lại hàng, cần đảo doanh thu và nhập kho hàng trả về.

**Trigger:** Biên bản trả hàng + hóa đơn điều chỉnh.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 521 | Hàng bán bị trả lại |
| Nợ | 33311 | Thuế GTGT đầu ra điều chỉnh |
| Có | 131 | Giảm phải thu |
| Nợ | 156 | Nhập kho hàng trả |
| Có | 632 | Giảm giá vốn |

**TK liên quan:** `521`, `33311`, `131`, `156`, `632`

**Edge cases:**
- Hàng hỏng không nhập kho được → ghi 811
- Trả lại khác kỳ → cần điều chỉnh kỳ trước

---

#### S06 — Doanh thu tài chính (lãi tiền gửi, lãi cho vay)

**Mô tả:** Thu nhập từ hoạt động tài chính ngoài SXKD chính. Ghi 515, không phải 511.

**Trigger:** Ngân hàng báo lãi tiền gửi hoặc đối tác trả lãi vay.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 112 | Tiền về tài khoản |
| Có | 515 | Doanh thu tài chính |

**TK liên quan:** `112`, `515`

**Edge cases:**
- Lãi phát sinh nhưng chưa nhận → Nợ 138 / Có 515
- Cuối kỳ kết chuyển 515 về 911

---

### 2.2 Domain: Mua hàng & Nhập kho

> **TK chủ lực:** 331, 156, 152, 153, 1331, 111, 112

---

#### P01 ★ CORE — Mua hàng hóa nhập kho (mua chịu)

**Mô tả:** Nhận hàng từ nhà cung cấp, chưa thanh toán. Ghi nhận hàng tồn kho và công nợ phải trả.

**Trigger:** Nhận hàng + hóa đơn GTGT của NCC.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 156 | Giá trị hàng nhập kho |
| Nợ | 1331 | Thuế GTGT đầu vào được khấu trừ |
| Có | 331 | Phải trả NCC (tổng tiền hóa đơn) |

**TK liên quan:** `156`, `1331`, `331`

**Edge cases:**
- Hàng nhập khẩu → thêm thuế NK (3333), VAT NK (33312)
- Chi phí vận chuyển → cộng vào giá vốn 156

---

#### P02 ★ CORE — Mua nguyên vật liệu nhập kho

**Mô tả:** Mua NVL phục vụ sản xuất. Tương tự P01 nhưng TK kho là 152 thay vì 156.

**Trigger:** Hóa đơn mua NVL + phiếu nhập kho.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 152 | Giá trị NVL nhập kho |
| Nợ | 1331 | VAT đầu vào |
| Có | 331 / 112 | Phải trả hoặc thanh toán ngay |

**TK liên quan:** `152`, `1331`, `331`, `112`

**Edge cases:**
- NVL không đủ tiêu chuẩn → nhập kho chờ trả lại, ghi tạm 151

---

#### P03 — Mua công cụ dụng cụ

**Mô tả:** CCDC giá trị nhỏ, không đủ tiêu chuẩn TSCĐ. Nhập kho 153, xuất dùng phân bổ qua 242.

**Trigger:** Hóa đơn mua CCDC.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 153 | Nhập kho CCDC |
| Nợ | 1331 | VAT đầu vào |
| Có | 331 / 112 | Phải trả hoặc thanh toán |

**TK liên quan:** `153`, `1331`, `331`, `112`

**Edge cases:**
- Xuất dùng 1 lần → Nợ 641/642/627 / Có 153
- Phân bổ nhiều kỳ → qua 242

---

#### P04 — Hàng mua đang đi đường

**Mô tả:** Hàng đã thanh toán hoặc đã có hóa đơn nhưng chưa về kho. Ghi 151 tạm thời.

**Trigger:** Hóa đơn NCC xuất nhưng hàng chưa về.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 151 | Hàng đang đi đường |
| Nợ | 1331 | VAT đầu vào |
| Có | 331 | Phải trả NCC |

**TK liên quan:** `151`, `1331`, `331`

**Edge cases:**
- Khi hàng về kho → Nợ 156 / Có 151
- Cuối kỳ phải kiểm tra 151 còn số dư hợp lý

---

#### P05 — Mua dịch vụ (chi phí dịch vụ mua ngoài)

**Mô tả:** Thuê dịch vụ bên ngoài: điện, nước, vận chuyển, tư vấn... Không nhập kho, chi phí ngay.

**Trigger:** Hóa đơn dịch vụ từ nhà cung cấp.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 641 / 642 / 627 | Chi phí theo bộ phận |
| Nợ | 1331 | VAT đầu vào |
| Có | 331 / 112 | Phải trả hoặc thanh toán |

**TK liên quan:** `641`, `642`, `627`, `1331`, `331`, `112`

**Edge cases:**
- Dịch vụ nhiều kỳ (thuê văn phòng) → ghi trước vào 242, phân bổ dần

---

### 2.3 Domain: Thanh toán & Tiền

> **TK chủ lực:** 111, 112, 113, 131, 331, 141, 138

---

#### T01 ★ CORE — Thanh toán công nợ phải trả NCC

**Mô tả:** Chuyển tiền hoặc trả tiền mặt để xóa công nợ 331.

**Trigger:** Lệnh chuyển tiền / phiếu chi tiền mặt.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 331 | Giảm phải trả NCC |
| Có | 112 / 111 | Xuất tiền ngân hàng / tiền mặt |

**TK liên quan:** `331`, `112`, `111`

**Edge cases:**
- Thanh toán một phần → dư 331 còn lại
- Thanh toán ngoại tệ → phát sinh chênh lệch tỷ giá 413/635/515

---

#### T02 ★ CORE — Thu tiền khách hàng (thu hồi công nợ)

**Mô tả:** Khách hàng trả tiền, xóa công nợ 131.

**Trigger:** Giấy báo có ngân hàng / phiếu thu tiền mặt.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 112 / 111 | Tiền về |
| Có | 131 | Giảm phải thu KH |

**TK liên quan:** `112`, `111`, `131`

**Edge cases:**
- Khách trả dư → 131 Có → phải trả lại hoặc ghi 338
- Chiết khấu thanh toán → Nợ 635 / Có 131

---

#### T03 — Tạm ứng tiền cho nhân viên

**Mô tả:** Xuất tiền tạm ứng cho nhân viên đi công tác, mua hàng. Theo dõi qua 141.

**Trigger:** Giấy đề nghị tạm ứng được duyệt.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 141 | Tạm ứng nhân viên |
| Có | 111 / 112 | Xuất tiền |

**TK liên quan:** `141`, `111`, `112`

**Edge cases:**
- Thanh toán tạm ứng → Nợ CP / Có 141
- Nếu chi vượt → Nợ 141 âm → phải hoàn quỹ

---

#### T04 — Chuyển tiền giữa quỹ và ngân hàng

**Mô tả:** Nộp tiền mặt vào ngân hàng hoặc rút tiền về quỹ. Không làm thay đổi tổng tài sản.

**Trigger:** Phiếu chi + giấy nộp tiền ngân hàng.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 113 | Tiền đang chuyển (nếu khác ngày) |
| Có | 111 | Xuất quỹ tiền mặt |
| Nợ | 112 | Khi ngân hàng xác nhận |
| Có | 113 | Xóa tiền đang chuyển |

**TK liên quan:** `111`, `112`, `113`

**Edge cases:**
- Cùng ngày → bỏ qua 113, ghi thẳng 112 / Có 111
- Khác ngày nhớ dùng 113 để tránh sai số dư

---

#### T05 — Thu nhập khác phát sinh bằng tiền

**Mô tả:** Tiền phạt vi phạm hợp đồng, tiền bồi thường, thanh lý tài sản... Ghi 711.

**Trigger:** Biên bản xác nhận khoản thu nhập khác.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 111 / 112 | Tiền nhận được |
| Có | 711 | Thu nhập khác |

**TK liên quan:** `111`, `112`, `711`

**Edge cases:**
- Cuối kỳ kết chuyển 711 về 911

---

### 2.4 Domain: Thuế

> **TK chủ lực:** 333 (3331, 3334, 3335), 1331, 1332, 821, 347, 243

---

#### X01 ★ CORE — Kê khai và nộp thuế GTGT hàng tháng/quý

**Mô tả:** Bù trừ VAT đầu ra (33311) với VAT đầu vào (1331). Nộp phần chênh lệch vào ngân sách.

**Trigger:** Kỳ kê khai VAT (tháng hoặc quý).

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 33311 | Bù trừ VAT đầu ra |
| Có | 1331 | Bù trừ VAT đầu vào |
| Nợ | 3331 | VAT còn phải nộp |
| Có | 112 | Nộp ngân sách |

**TK liên quan:** `33311`, `1331`, `3331`, `112`

**Edge cases:**
- 1331 > 33311 → được hoàn thuế hoặc chuyển kỳ sau
- Cuối tháng vẫn phải bù trừ để xác định số thực nộp

---

#### X02 ★ CORE — Hạch toán chi phí thuế TNDN hiện hành

**Mô tả:** Cuối năm (hoặc tạm tính quý), tính thuế TNDN phải nộp dựa trên thu nhập tính thuế.

**Trigger:** Lập tờ khai thuế TNDN tạm tính / quyết toán.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 8211 | Chi phí thuế TNDN hiện hành |
| Có | 3334 | Thuế TNDN phải nộp |

**TK liên quan:** `8211`, `3334`

**Edge cases:**
- Thuế tối thiểu toàn cầu → TK 82112
- Nộp tiền: Nợ 3334 / Có 112
- Nộp thiếu → phạt chậm nộp

---

#### X03 ★ CORE — Hạch toán và nộp thuế TNCN từ tiền lương

**Mô tả:** Khấu trừ thuế TNCN tại nguồn khi trả lương, kê khai và nộp hộ người lao động.

**Trigger:** Bảng lương tháng được duyệt.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 334 | Khấu trừ thuế TNCN từ lương phải trả |
| Có | 3335 | Thuế TNCN phải nộp |
| Nợ | 3335 | Nộp thuế |
| Có | 112 | Xuất tiền ngân hàng |

**TK liên quan:** `334`, `3335`, `112`

**Edge cases:**
- Thu nhập dưới mức khởi điểm → không phát sinh 3335
- Quyết toán cuối năm có thể hoàn hoặc nộp bổ sung

---

#### X04 — Thuế GTGT đầu vào không được khấu trừ

**Mô tả:** Hóa đơn không hợp lệ, hàng không dùng cho SXKD chịu thuế → VAT đầu vào tính vào chi phí.

**Trigger:** Phát hiện hóa đơn không đủ điều kiện khấu trừ.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 641 / 642 | Tính VAT vào chi phí BH/QLDN |
| Có | 1331 | Giảm VAT đầu vào (nếu đã ghi) |

**TK liên quan:** `1331`, `641`, `642`

**Edge cases:**
- Kiểm tra điều kiện khấu trừ trước khi ghi 1331
- Hóa đơn sai mã số thuế → không được khấu trừ

---

#### X05 — Thuế TNDN hoãn lại

**Mô tả:** Phát sinh từ chênh lệch tạm thời giữa giá trị kế toán và giá trị tính thuế của tài sản/nợ phải trả.

**Trigger:** Cuối năm tài chính, khi rà soát chênh lệch tạm thời.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 243 | Tài sản thuế TNDN hoãn lại |
| Có | 8212 | CP thuế TNDN hoãn lại |

**TK liên quan:** `243`, `347`, `8212`

**Edge cases:**
- Chênh lệch tạm thời chịu thuế → Nợ 8212 / Có 347
- Đảo lại khi chênh lệch giải tỏa

---

### 2.5 Domain: Tài sản & Hàng tồn kho

> **TK chủ lực:** 211, 212, 213, 214, 241, 242, 152, 154, 155, 156

---

#### A01 ★ CORE — Mua tài sản cố định

**Mô tả:** Mua TSCĐ mới đưa vào sử dụng. Tăng nguyên giá TSCĐ, ghi nhận phải trả hoặc thanh toán ngay.

**Trigger:** Biên bản bàn giao TSCĐ + hóa đơn.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 211 | Nguyên giá TSCĐ hữu hình |
| Nợ | 1332 | VAT TSCĐ đầu vào |
| Có | 331 / 112 | Phải trả hoặc thanh toán |

**TK liên quan:** `211`, `1332`, `331`, `112`

**Edge cases:**
- TSCĐ vô hình → dùng 213
- TSCĐ thuê tài chính → 212
- Mua qua XDCB → tập hợp 241 trước, hoàn thành → chuyển 211

---

#### A02 ★ CORE — Trích khấu hao tài sản cố định hàng tháng

**Mô tả:** Phân bổ giá trị TSCĐ vào chi phí theo thời gian sử dụng. Bút toán phát sinh mỗi tháng.

**Trigger:** Cuối tháng, dựa trên bảng khấu hao.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 627 / 641 / 642 | CP khấu hao theo bộ phận sử dụng |
| Có | 2141 / 2143 | Hao mòn lũy kế TSCĐ |

**TK liên quan:** `627`, `641`, `642`, `2141`, `2142`, `2143`, `2147`

**Edge cases:**
- TSCĐ bộ phận nào dùng → bộ phận đó chịu khấu hao
- Ngừng sử dụng → dừng trích khấu hao
- Đánh giá lại → qua 412

---

#### A03 — Xuất kho nguyên vật liệu vào sản xuất

**Mô tả:** Xuất NVL từ kho 152 vào quy trình sản xuất, tập hợp vào 621.

**Trigger:** Phiếu xuất kho NVL.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 621 | CP NVL trực tiếp |
| Có | 152 | Xuất kho NVL |

**TK liên quan:** `621`, `152`

**Edge cases:**
- Cuối kỳ kết chuyển 621 → 154
- NVL xuất thừa nhập lại kho → đảo bút toán

---

#### A04 — Tập hợp chi phí sản xuất và tính giá thành

**Mô tả:** Kết chuyển 621, 622, 627 vào 154. Khi hoàn thành nhập kho thành phẩm.

**Trigger:** Cuối kỳ sản xuất, bảng tính giá thành.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 154 | Chi phí SXKD dở dang |
| Có | 621 | Kết chuyển CP NVL TT |
| Có | 622 | Kết chuyển CP NC TT |
| Có | 627 | Kết chuyển CP SXC |
| Nợ | 155 | Nhập kho thành phẩm |
| Có | 154 | Giá thành sản phẩm hoàn thành |

**TK liên quan:** `621`, `622`, `627`, `154`, `155`

**Edge cases:**
- Sản phẩm dở dang cuối kỳ → 154 còn dư
- Phế liệu thu hồi → giảm 154

---

#### A05 — Thanh lý, nhượng bán TSCĐ

**Mô tả:** Xóa TSCĐ khỏi sổ sách khi thanh lý hoặc nhượng bán. Ghi nhận thu nhập/chi phí khác.

**Trigger:** Biên bản thanh lý TSCĐ.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 214 | Hao mòn lũy kế |
| Nợ | 811 | Giá trị còn lại (nếu lỗ) |
| Có | 211 | Nguyên giá TSCĐ |
| Nợ | 111 / 112 | Tiền thu từ thanh lý |
| Có | 711 | Thu nhập thanh lý (nếu lãi) |

**TK liên quan:** `211`, `214`, `811`, `711`, `111`

**Edge cases:**
- VAT từ thanh lý phải nộp → 33311
- Chi phí thanh lý (vận chuyển...) → 811

---

#### A06 — Lập dự phòng giảm giá hàng tồn kho

**Mô tả:** Cuối năm, hàng tồn kho giá thị trường < giá vốn → lập dự phòng theo TT99.

**Trigger:** Kiểm kê cuối năm, giá thị trường suy giảm.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 642 | Chi phí dự phòng (QLDN) |
| Có | 2294 | Dự phòng giảm giá HTK |

**TK liên quan:** `642`, `2294`

**Edge cases:**
- Năm sau giá phục hồi → hoàn nhập dự phòng, đảo bút toán
- Không được lập quá mức cần thiết

---

### 2.6 Domain: Lương & Bảo hiểm xã hội

> **TK chủ lực:** 334, 338 (3382, 3383, 3384, 3386), 622, 641, 642, 111, 112

---

#### L01 ★ CORE — Tính lương và các khoản phải trả người lao động

**Mô tả:** Hạch toán chi phí lương vào các bộ phận (BH, QLDN, SXC) và ghi nhận công nợ phải trả 334.

**Trigger:** Bảng lương tháng được Giám đốc duyệt.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 622 / 641 / 642 / 627 | Chi phí lương theo bộ phận |
| Có | 334 | Lương phải trả NLĐ (gross - BHXH NLĐ - TNCN) |
| Có | 3383 / 3384 / 3386 | BHXH/BHYT/BHTN phần NLĐ đóng |

**TK liên quan:** `622`, `641`, `642`, `627`, `334`, `3383`, `3384`, `3386`

**Edge cases:**
- Lương thử việc, lương thời vụ → vẫn ghi 334
- Hoa hồng bán hàng → 641

---

#### L02 ★ CORE — Trích bảo hiểm xã hội phần doanh nghiệp

**Mô tả:** DN đóng BHXH/BHYT/BHTN/KPCĐ phần của người sử dụng lao động vào chi phí.

**Trigger:** Bảng lương tháng + tỷ lệ trích theo quy định.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 622 / 641 / 642 | Chi phí BHXH/BHYT/BHTN/KPCĐ của DN |
| Có | 3382 / 3383 / 3384 / 3386 | Các khoản trích theo lương phải nộp |

**TK liên quan:** `3382`, `3383`, `3384`, `3386`, `622`, `641`, `642`

**Edge cases:**
- Tỷ lệ: BHXH 17.5%, BHYT 3%, BHTN 1%, KPCĐ 2% (phần DN)
- Kiểm tra cập nhật tỷ lệ theo quy định mới nhất

---

#### L03 ★ CORE — Chi lương cho người lao động

**Mô tả:** Chuyển tiền lương thực nhận (net) vào tài khoản NLĐ hoặc trả tiền mặt.

**Trigger:** Ngày trả lương hàng tháng.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 334 | Lương phải trả |
| Có | 112 / 111 | Tiền chuyển khoản / tiền mặt |

**TK liên quan:** `334`, `112`, `111`

**Edge cases:**
- Lương chưa lĩnh cuối tháng → 334 còn dư Có
- Tạm ứng lương đã chi → bù trừ với 141

---

#### L04 — Nộp BHXH, BHYT, BHTN, KPCĐ lên cơ quan

**Mô tả:** Chuyển tiền bảo hiểm (cả phần NLĐ và DN) lên BHXH và công đoàn.

**Trigger:** Hạn nộp BHXH (thường cuối tháng hoặc ngày 15 tháng sau).

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 3382 / 3383 / 3384 / 3386 | Xóa công nợ bảo hiểm phải nộp |
| Có | 112 | Chuyển tiền nộp |

**TK liên quan:** `3382`, `3383`, `3384`, `3386`, `112`

**Edge cases:**
- Nộp chậm bị phạt → ghi thêm 811
- Một số DN nộp luôn TNCN cùng thời điểm

---

### 2.7 Domain: Kết chuyển cuối kỳ & Điều chỉnh

> **TK chủ lực:** 911, 421, 821, 242, 229, 335, 521

---

#### G01 ★ CORE — Kết chuyển doanh thu về tài khoản xác định KQKD

**Mô tả:** Cuối kỳ, kết chuyển toàn bộ doanh thu (511, 515) và thu nhập khác (711) về 911.

**Trigger:** Bút toán cuối kỳ kế toán (tháng/quý/năm).

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 511 | Kết chuyển DT bán hàng |
| Nợ | 515 | Kết chuyển DT tài chính |
| Nợ | 711 | Kết chuyển TN khác |
| Có | 911 | Tổng doanh thu kết chuyển |

**TK liên quan:** `511`, `515`, `711`, `911`

**Edge cases:**
- 521 (giảm trừ DT) phải kết chuyển ngược: Nợ 911 / Có 521 trước, sau đó kết chuyển 511 thuần

---

#### G02 ★ CORE — Kết chuyển chi phí về tài khoản xác định KQKD

**Mô tả:** Cuối kỳ, kết chuyển toàn bộ chi phí (632, 635, 641, 642, 811, 821) về 911.

**Trigger:** Bút toán cuối kỳ kế toán.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 911 | Tổng chi phí kết chuyển |
| Có | 632 | Giá vốn hàng bán |
| Có | 635 | Chi phí tài chính |
| Có | 641 | Chi phí bán hàng |
| Có | 642 | Chi phí QLDN |
| Có | 811 | Chi phí khác |
| Có | 821 | Chi phí thuế TNDN |

**TK liên quan:** `911`, `632`, `635`, `641`, `642`, `811`, `821`

**Edge cases:**
- Số dư 911 Có = Lãi, Nợ = Lỗ
- Sau đó kết chuyển 911 sang 4212

---

#### G03 ★ CORE — Kết chuyển lợi nhuận sau thuế

**Mô tả:** Xác định lợi nhuận/lỗ sau thuế, kết chuyển từ 911 sang 421.

**Trigger:** Cuối năm tài chính sau khi xác định đủ CP thuế TNDN.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 911 | Nếu lãi: kết chuyển lãi |
| Có | 4212 | LNST chưa phân phối năm nay |

**TK liên quan:** `911`, `4212`

**Edge cases:**
- Nếu lỗ: Nợ 4212 / Có 911
- Sau đó phân phối LN: trích quỹ (414, 353) → cổ tức (332)

---

#### G04 ★ CORE — Phân bổ chi phí trả trước (242)

**Mô tả:** Chi phí lớn trả một lần (bảo hiểm, thuê văn phòng, công cụ lớn) được phân bổ dần vào chi phí theo kỳ.

**Trigger:** Cuối mỗi kỳ kế toán theo bảng phân bổ.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 641 / 642 / 627 | Chi phí kỳ này |
| Có | 242 | Giảm chi phí chờ phân bổ |

**TK liên quan:** `242`, `641`, `642`, `627`

**Edge cases:**
- Hết thời gian phân bổ → 242 về 0
- Dừng hợp đồng giữa chừng → xử lý phần còn lại vào 811

---

#### G05 — Lập dự phòng phải thu khó đòi

**Mô tả:** Cuối năm, đánh giá các khoản phải thu có nguy cơ không thu hồi được.

**Trigger:** Rà soát tuổi nợ cuối năm.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 642 | Chi phí dự phòng QLDN |
| Có | 2293 | Dự phòng phải thu khó đòi |

**TK liên quan:** `642`, `2293`

**Edge cases:**
- Nợ xóa sổ thực sự → Nợ 2293 / Có 131
- Dự phòng dư thừa → hoàn nhập: Nợ 2293 / Có 642

---

#### G06 — Điều chỉnh chênh lệch tỷ giá cuối kỳ

**Mô tả:** Đánh giá lại các khoản mục tiền tệ có gốc ngoại tệ (111, 112, 131, 331) theo tỷ giá cuối kỳ.

**Trigger:** Cuối kỳ kế toán, khi có số dư ngoại tệ.

**Định khoản:**

| Nợ/Có | Tài khoản | Diễn giải |
|-------|-----------|-----------|
| Nợ | 111 / 112 / 131 | Nếu tỷ giá tăng (khoản thu tăng) |
| Có | 413 | Chênh lệch tỷ giá hối đoái |
| Nợ | 413 | Nếu tỷ giá bất lợi |
| Có | 331 / 341 | Nợ phải trả ngoại tệ tăng |

**TK liên quan:** `413`, `111`, `112`, `131`, `331`, `341`

**Edge cases:**
- Cuối năm kết chuyển 413 vào 635 (lỗ tỷ giá) hoặc 515 (lãi tỷ giá)

---

## 3. Core Use Case Shortlist — 22 nghiệp vụ bắt buộc

> **Tiêu chí chọn lọc:** Phát sinh hàng ngày · Bắt buộc cho BCTC · Tạo vòng kế toán hoàn chỉnh

| # | ID | Tên nghiệp vụ | Domain | TK chủ lực |
|---|-----|--------------|--------|------------|
| 1 | S01 | Bán hàng thu tiền ngay (có VAT) | Bán hàng | 111/112, 511, 33311 |
| 2 | S02 | Bán hàng ghi công nợ (bán chịu) | Bán hàng | 131, 511, 33311 |
| 3 | S03 | Xuất kho ghi nhận giá vốn | Bán hàng | 632, 155/156 |
| 4 | P01 | Mua hàng hóa nhập kho (mua chịu) | Mua hàng | 156, 1331, 331 |
| 5 | P02 | Mua nguyên vật liệu nhập kho | Mua hàng | 152, 1331, 331 |
| 6 | T01 | Thanh toán công nợ phải trả NCC | Thanh toán | 331, 112/111 |
| 7 | T02 | Thu tiền khách hàng (thu hồi công nợ) | Thanh toán | 112/111, 131 |
| 8 | X01 | Kê khai và nộp thuế GTGT hàng tháng/quý | Thuế | 33311, 1331, 3331, 112 |
| 9 | X02 | Hạch toán chi phí thuế TNDN hiện hành | Thuế | 8211, 3334 |
| 10 | X03 | Hạch toán và nộp thuế TNCN từ tiền lương | Thuế | 334, 3335, 112 |
| 11 | A01 | Mua tài sản cố định | Tài sản | 211, 1332, 331/112 |
| 12 | A02 | Trích khấu hao TSCĐ hàng tháng | Tài sản | 627/641/642, 214x |
| 13 | L01 | Tính lương và các khoản phải trả NLĐ | Lương | 622/641/642, 334, 338x |
| 14 | L02 | Trích bảo hiểm xã hội phần doanh nghiệp | Lương | 622/641/642, 3382/83/84/86 |
| 15 | L03 | Chi lương cho người lao động | Lương | 334, 112/111 |
| 16 | G01 | Kết chuyển doanh thu về 911 | GL | 511, 515, 711, 911 |
| 17 | G02 | Kết chuyển chi phí về 911 | GL | 911, 632, 635, 641, 642, 811, 821 |
| 18 | G03 | Kết chuyển lợi nhuận sau thuế | GL | 911, 4212 |
| 19 | G04 | Phân bổ chi phí trả trước (242) | GL | 242, 641/642/627 |

---

## 4. Kiểm tra vòng kế toán

### Chu trình kế toán đầy đủ

```
MUA HÀNG          →  NHẬP KHO         →  SẢN XUẤT
P01/P02              152/156              A03, A04
(331, 152/156)       nhập kho             (621→154→155)
      ↓
THANH TOÁN NCC    ←→  BÁN HÀNG        →  THU TIỀN KH
T01                  S01/S02/S03          T02
(331→112)            (131,511,632)        (131→112)
      ↓
LƯƠNG & BHXH      →  THUẾ             →  KẾT CHUYỂN
L01/L02/L03          X01/X02/X03          G01/G02/G03
(334,338x→112)       (333x→112)           (→911→4212)
      ↓
KHẤU HAO
A02
(214x←641/642/627)
```

### Bảng kiểm tra bao phủ BCTC

| Khoản mục BCTC | Được bao phủ | Use Case |
|----------------|:---:|---------|
| **BCĐKT — Tài sản ngắn hạn** | ✅ | S01, S02, T01, T02, P01, P02 |
| **BCĐKT — Tài sản dài hạn** | ✅ | A01, A02 |
| **BCĐKT — Nợ phải trả** | ✅ | P01, P02, L01, L02, X01, X02 |
| **BCĐKT — Vốn chủ sở hữu** | ✅ | G03 (→ 4212) |
| **BCKQHĐKD — Doanh thu thuần** | ✅ | S01, S02, G01 |
| **BCKQHĐKD — Giá vốn** | ✅ | S03, G02 |
| **BCKQHĐKD — Chi phí BH, QLDN** | ✅ | L01, L02, A02, G04, G02 |
| **BCKQHĐKD — Thuế TNDN** | ✅ | X02, G02 |
| **BCKQHĐKD — LNST** | ✅ | G03 |

**Kết luận:** 22 core use cases bao phủ toàn bộ các khoản mục trọng yếu trên BCĐKT và BCKQHĐKD. Hệ thống đủ điều kiện vận hành một chu kỳ kế toán hoàn chỉnh từ phát sinh nghiệp vụ đến lập báo cáo tài chính.

---

*Tài liệu được soạn theo Thông tư 99/2025/TT-BTC — Phụ lục II Hệ thống tài khoản kế toán doanh nghiệp*  
*Nguồn tham chiếu: https://ketoanthienung.net/he-thong-tai-khoan-ke-toan-theo-thong-tu-99-2025-tt-btc.htm*
