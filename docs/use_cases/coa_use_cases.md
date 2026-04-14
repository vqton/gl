# 🧱 DOMAIN: CHART OF ACCOUNTS (COA)

# 🔥 1. CREATE ACCOUNT

## 🎯 Mục tiêu
Tạo tài khoản kế toán mới trong hệ thống

## 📥 Input
```json
{
  "account_code": "string",
  "account_name": "string",
  "account_type": "asset | liability | equity | revenue | expense",
  "normal_balance": "debit | credit",
  "parent_account_code": "string | null"
}
```

## ⚙️ Trigger
```text
User creates new account
```

## 📌 Business Rules
* account_code MUST unique
* parent_account MUST exist (if provided)
* parent MUST NOT allow posting
* normal_balance MUST match account_type

## 🔗 Output
* account created in DB
* hierarchy updated

## ⚠️ Edge Cases
* duplicate code → reject
* parent not exist → reject
* circular hierarchy → reject

---

# 🔥 2. UPDATE ACCOUNT

## 🎯 Mục tiêu
Chỉnh sửa thông tin tài khoản

## ⚠️ Critical Rule
👉 KHÔNG cho phép update nếu đã phát sinh journal

## 📌 Business Rules
* cannot change account_code
* cannot change account_type if used
* parent change must revalidate hierarchy

## ⚠️ Edge Cases
* move account to its child → reject

---

# 🔥 3. DELETE ACCOUNT

## 🎯 Mục tiêu
Xóa tài khoản khỏi hệ thống

## 📌 Business Rules
* ONLY allow if:
  * no journal exists
  * no child accounts

## ⚠️ Edge Cases
* has children → reject
* has transactions → reject

---

# 🔥 4. VALIDATE ACCOUNT HIERARCHY

## 🎯 Mục tiêu
Đảm bảo cấu trúc cây hợp lệ

## 📌 Rules
* no circular reference
* parent must exist
* max depth (optional)

## ⚠️ Khi trigger
* create
* update

---

# 🔥 5. SET ACCOUNT POSTING FLAG

## 🎯 Mục tiêu
Xác định tài khoản có được hạch toán không

## 📌 Rules
```text
if account has children:
    allow_posting = false
```

## ⚠️ Edge Cases
* manually set posting=true on parent → override = false

---

# 🔥 6. GET ACCOUNT TREE

## 🎯 Mục tiêu
Trả về cấu trúc cây tài khoản

## 📤 Output
```json
[
  {
    "code": "111",
    "children": [...]
  }
]
```

## ⚠️ Requirement
* sorted by account_code
* full hierarchy

---

# 🔥 7. VALIDATE ACCOUNT BEFORE JOURNAL

## 🎯 Mục tiêu
Đảm bảo tài khoản hợp lệ trước khi hạch toán

## 📌 Rules
* account exists
* allow_posting = true

## ⚠️ Edge Cases
* posting vào parent → reject

---

# 🔥 8. IMPORT COA (OPTIONAL BUT REAL)

## 🎯 Mục tiêu
Import danh mục tài khoản từ file

## 📌 Input
```text
CSV / Excel
```

## 📌 Rules
* validate từng dòng
* rollback nếu có lỗi

---

# 🔥 9. EXPORT COA

## 🎯 Mục tiêu
Xuất danh mục tài khoản