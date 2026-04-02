# User Journey Upgrade - Vietnamese SME Accounting System

## Target Users
- **Kế toán trưởng** (Chief Accountant) - 20 năm kinh nghiệm
- **Kế toán viên** (Accountant) - 3-5 năm kinh nghiệm
- **Quản trị viên** (System Admin) - IT support

---

## Current Problems
1. Web app trống, không có dashboard
2. Phải vào Django admin để làm việc - không professional
3. Không có quick actions
4. Thiếu keyboard shortcuts
5. Permission không đồng nhất giữa web và admin

---

## User Journey V2 - Market Standard

```
┌─────────────────────────────────────────────────────────────────────┐
│ LOGIN → DASHBOARD → MODULE MENU → WORK AREA                        │
└─────────────────────────────────────────────────────────────────────┘
```

### Phase 1: LOGIN
```
┌─────────────────────────────────────────┐
│  🏢 SME ACCOUNTING                       │
│  ─────────────────────────────────────   │
│  Username: [____________]                │
│  Password: [____________]                │
│  [ ] Remember me                         │
│  [ ] Đăng nhập                           │
│  ─────────────────────────────────────   │
│  Demo: admin / admin123                  │
│  © 2026 TT99/2025/TT-BTC                │
└─────────────────────────────────────────┘
```
- Remember last 5 users
- Password visibility toggle

---

### Phase 2: DASHBOARD (Role-based)

**Kế toán trưởng Dashboard:**
```
┌──────────────────────────────────────────────────────────────────────────────┐
│ 🔔 3 │ 👤 Kế toán trưởng │ ⏰ 01/04/2026 14:45 │ 🔴 Báo cáo │ 🚪 Logout       │
├──────────────────────────────────────────────────────────────────────────────┤
│ ╔══════════════════════════════════════════════════════════════════════════╗│
│ ║  TỔNG QUAN THÁNG 03/2026                                    [Xem chi tiết]║│
│ ╠══════════════════════════════════════════════════════════════════════════╣│
│ ║  💰 Doanh thu    │ 📊 Công nợ    │ 📦 Tồn kho    │ 💵 Tiền mặt         ║│
│ ║  2,450,000,000   │ 125,000,000   │ 890,000,000   │ 45,000,000          ║│
│ ║  ▲12% vs tháng   │ ▲5% vs tháng  │ ▼3% vs tháng  │ ▲8% vs tháng        ║│
│ ╚══════════════════════════════════════════════════════════════════════════╝│
│                                                                            │
│ ┌─────────────────────────────┐  ┌──────────────────────────────────────┐   │
│ │ 📋 CÔNG VIỆC CẦN LÀM        │  │ 🔔 THÔNG BÁO & CẢNH BÁO             │   │
│ │ ─────────────────────────── │  │ ─────────────────────────────────── │   │
│ │ □ Hóa đơn chưa xuất (5)    │  │ ⚠️ 3 hóa đơn GTGT sắp hết hạn       │   │
│ │ □ Phiếu thu chưa đối (2)   │  │ ⚠️ Tồn kho sản phẩm A dưới tối thiểu│   │
│ │ □ Báo cáo thuế tháng       │  │ ℹ️ Đã đối phiếu thu 15/03           │   │
│ │ □ Kiểm tra công nợ         │  │ ✓ Kết chuyển cuối tháng hoàn tất   │   │
│ └─────────────────────────────┘  └──────────────────────────────────────┘   │
│                                                                            │
│ ┌─────────────────────────────┐  ┌──────────────────────────────────────┐   │
│ │ ⚡ THAO TÁC NHANH           │  │ 📈 BIỂU ĐỒ DOANH THU 6 THÁNG        │   │
│ │ ─────────────────────────── │  │ ─────────────────────────────────── │   │
│ │ [+ Tạo hóa đơn]  [Ctrl+N]  │  │      █                    █           │   │
│ │ [+ Tạo phiếu thu] [Ctrl+T] │  │   █  █  █      █       █  █           │   │
│ │ [+ Tạo phiếu chi] [Ctrl+C] │  │  █  █  █  █   █  █   █  █  █          │   │
│ │ [+ Nhập kho]    [Ctrl+P]  │  │  10 11 12  01  02  03                │   │
│ │ [+ Xuất kho]    [Ctrl+X]  │  └──────────────────────────────────────┘   │
│ │ [+ Bút toán]   [Ctrl+B]   │                                               │
│ └─────────────────────────────┘                                             │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

### Phase 3: LEFT SIDEBAR NAVIGATION

**Role: Kế toán trưởng**
```
┌─────────────────────┐
│ 🏢 CÔNG TY ABC      │
│ ─────────────────── │
│                     │
│ 📊 BÁO CÁO      ▶  │  ← Click để expand
│   ├ Báo cáo tài chính
│   ├ Báo cáo thuế  
│   ├ Báo cáo quản trị
│   └ Xuất Excel/PDF
│                     │
│ 💰 NGHIỆP VỤ     ▶  │
│   ├ Hóa đơn
│   ├ Phiếu thu/chi
│   ├ Bút toán
│   └ Chứng từ gốc
│                     │
│ 📦 KHO             ▶  │
│   ├ Nhập/xuất kho
│   ├ Tồn kho
│   └ Báo cáo kho
│                     │
│ 👥 NHÂN SỰ       ▶  │
│   ├ Lương
│   └ Bảo hiểm
│                     │
│ 🏢 DANH MỤC      ▶  │
│   ├ Khách hàng
│   ├ Nhà cung cấp
│   └ Tài khoản KT
│                     │
│ ⚙️ CẤU HÌNH      ▶  │
│   ├ Người dùng
│   ├ Đơn vị
│   └ Hệ thống
│ ─────────────────── │
│ 🎯 Cuối kỳ: 31/03   │
└─────────────────────┘
```

**Role: Kế toán viên** (không thấy Cấu hình)
```
┌─────────────────────┐
│ 🏢 CÔNG TY ABC      │
│ ─────────────────── │
│                     │
│ 📊 BÁO CÁO      ▶  │
│ 💰 NGHIỆP VỤ     ▶  │
│ 📦 KHO           ▶  │
│ 👥 NHÂN SỰ       ▶  │
│ 🏢 DANH MỤC      ▶  │  ← Chỉ xem, không edit
│                     │
│ ─────────────────── │
│ 🎯 Cuối kỳ: 31/03   │
└─────────────────────┘
```

---

### Phase 4: WORK AREA - Example: Hóa đơn

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ 💰 NGHIỆP VỤ > Hóa đơn                                      [+ Tạo mới]       │
├──────────────────────────────────────────────────────────────────────────────┤
│ Tìm kiếm: [_________________________] [🔍] [Hóa đơn] [▼] [Lọc] [Xuất Excel] │
├──────────────────────────────────────────────────────────────────────────────┤
│ │ STT │ Số hóa đơn   │ Ngày      │ Khách hàng      │ Tiền       │ Thuế  │ TT  │
│ ├─────┼──────────────┼───────────┼─────────────────┼────────────┼───────┼─────┤
│ │  1  │ HD-2026-0045 │ 01/04/2026│ Công ty TNHH X  │ 50,000,000 │ 5,000,000│ ✓  │
│ │  2  │ HD-2026-0044 │ 31/03/2026│ Công ty CP Y    │ 25,000,000 │ 2,500,000│ ✓  │
│ │  3  │ HD-2026-0043 │ 30/03/2026│ Doanh nghiệp Z  │ 80,000,000 │ 8,000,000│ ⏳ │
│───────┴──────────────┴───────────┴─────────────────┴────────────┴───────┴────│
│                     │                                                    │     │
│    [◀ 1 2 3 4 5 ▶] │              Tổng: 155,000,000  │  15,500,000         │     │
└──────────────────────────────────────────────────────────────────────────────┘

[Keyboard shortcuts: Ctrl+N=new, Enter=edit, Del=delete, F5=refresh, Ctrl+F=search]
```

---

### Phase 5: FORM - Quick Entry (Keyboard-first)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ 💰 NGHIỆP VỤ > Hóa đơn > Tạo mới                               [Lưu] [Hủy] │
├──────────────────────────────────────────────────────────────────────────────┤
│ Số hóa đơn: [HD-2026-0046_______________]  Ngày: [01/04/2026] [Today]       │
│ Mẫu số:    [01GTKT0_001_______________]  Ký hiệu: [AA/23P_______________]  │
│ ─────────────────────────────────────────────────────────────────────────────│
│ Khách hàng: [Công ty TNHH X__________________________🔍] [+]                │
│             Mã số thuế: [1234567890____________]                           │
│             Địa chỉ: [123 Đường Nguyễn Trãi, Q1, TP.HCM___________]       │
│ ─────────────────────────────────────────────────────────────────────────────│
│ Hàng hóa/Dịch vụ:                                                            │
│ ┌─────┬──────────────────────┬─────┬────────────┬─────────────┬───────────┐ │
│ │ STT │ Tên hàng              │ SốL │ Đơn giá   │ Thành tiền  │ Thuế GTGT│ │
│ ├─────┼──────────────────────┼─────┼────────────┼─────────────┼───────────┤ │
│ │  1  │ [Sản phẩm A____🔍]   │ 10  │ 5,000,000 │ 50,000,000  │ [10%__▼] │ │
│ │  2  │ [+ Thêm dòng]        │     │           │             │           │ │
│ └─────┴──────────────────────┴─────┴────────────┴─────────────┴───────────┘ │
│ ─────────────────────────────────────────────────────────────────────────────│
│                    Tổng tiền trước thuế: [55,000,000______________________] │
│                           Thuế GTGT (10%): [5,500,000______________________] │
│                           TỔNG CỘNG:       [60,500,000______________________] │
│ ─────────────────────────────────────────────────────────────────────────────│
│ [Tab] moves to next field, [Enter] saves, [Esc] cancels                      │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Keyboard Shortcuts (Mandatory)

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | Tạo mới |
| `Ctrl+S` | Lưu |
| `Ctrl+F` | Tìm kiếm |
| `F5` | Refresh |
| `Ctrl+P` | In/Export |
| `Tab` | Next field |
| `Enter` | Save/Confirm |
| `Esc` | Cancel/Close |

---

## Permission Matrix

| Feature | Admin | Chief Accountant | Accountant | Viewer |
|---------|-------|------------------|-------------|--------|
| Dashboard | ✓ | ✓ | ✓ | ✓ |
| Hóa đơn CRUD | ✓ | ✓ | ✓ | View only |
| Phiếu Thu/Chi | ✓ | ✓ | ✓ | View only |
| Bút toán | ✓ | ✓ | ✓ | View only |
| Kho CRUD | ✓ | ✓ | ✓ | View only |
| Lương | ✓ | ✓ | ✓ | View only |
| Báo cáo | ✓ | ✓ | View only | View only |
| Danh mục | ✓ | ✓ | View only | View only |
| Người dùng | ✓ | ✓ | None | None |
| Cấu hình | ✓ | None | None | None |

---

## Implementation Priority

1. **Week 1**: Dashboard + Quick Actions
2. **Week 2**: Left sidebar with role-based menu
3. **Week 3**: Work area templates + keyboard shortcuts
4. **Week 4**: Permission sync between web and admin
5. **Week 5**: Reports + Export features

---

## Technical Requirements

- Session-based auth (keep simple, no JWT for internal app)
- All forms: keyboard navigable
- Auto-save draft every 30 seconds
- Audit log for all CRUD operations
- Vietnamese datetime format: DD/MM/YYYY
- Vietnamese number format: 1.234.567 (dot as thousand separator)
- Currency: VND with .00 decimals
