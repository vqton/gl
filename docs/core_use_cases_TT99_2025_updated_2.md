```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "TT99_2025_Core_Accounting_UseCases",
  "description": "Production-ready JSON Schema definitions for 22 core accounting use cases per Thông tư 99/2025/TT-BTC",
  "version": "1.0.0",
  "type": "object",
  "$defs": {
    "Decimal": { "type": "number", "multipleOf": 0.01, "minimum": 0 },
    "Date": { "type": "string", "format": "date", "pattern": "^\\d{4}-\\d{2}-\\d{2}$" },
    "UUID": { "type": "string", "format": "uuid" },
    "AccountCode": { "type": "string", "pattern": "^(111|112|113|131|1331|1332|138|141|151|152|153|154|155|156|157|211|212|213|2141|2142|2143|2147|2293|2294|241|242|243|331|3331|33311|33312|3333|3334|3335|334|335|3382|3383|3384|3386|341|413|4212|511|515|521|621|622|627|632|635|641|642|711|811|8211|8212|911)$" },
    "JournalLine": {
      "type": "object",
      "properties": {
        "account_code": { "$ref": "#/$defs/AccountCode" },
        "debit": { "$ref": "#/$defs/Decimal" },
        "credit": { "$ref": "#/$defs/Decimal" },
        "description": { "type": "string" },
        "auxiliary": { "type": "object" }
      },
      "required": ["account_code", "debit", "credit"],
      "oneOf": [
        { "properties": { "debit": { "exclusiveMinimum": 0 }, "credit": { "const": 0 } } },
        { "properties": { "debit": { "const": 0 }, "credit": { "exclusiveMinimum": 0 } } }
      ]
    },
    "PeriodStatus": { "type": "string", "enum": ["OPEN", "CLOSED", "LOCKED"] },
    "PaymentMethod": { "type": "string", "enum": ["CASH", "BANK_TRANSFER", "OFFSET"] },
    "VatRate": { "type": "number", "enum": [0, 0.05, 0.08, 0.1] }
  },
  "properties": {
    "use_cases": {
      "type": "array",
      "minItems": 22,
      "maxItems": 22,
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string", "pattern": "^[A-Z]\\d{2}$" },
          "name": { "type": "string" },
          "domain": { "type": "string", "enum": ["SALES", "PURCHASE", "PAYMENT", "TAX", "ASSET_INVENTORY", "PAYROLL", "GENERAL_LEDGER"] },
          "trigger": { "type": "string" },
          "request_schema": {
            "type": "object",
            "properties": {
              "properties": { "type": "object" },
              "required": { "type": "array", "items": { "type": "string" } },
              "additionalProperties": false
            }
          },
          "journal_template": {
            "type": "array",
            "items": { "$ref": "#/$defs/JournalLine" },
            "minItems": 2
          },
          "validation_rules": { "type": "array", "items": { "type": "string" } },
          "compliance_ref": { "type": "string" }
        },
        "required": ["id", "name", "domain", "request_schema", "journal_template", "validation_rules"]
      }
    }
  },
  "use_cases": [
    {
      "id": "S01",
      "name": "Bán hàng thu tiền ngay (có VAT)",
      "domain": "SALES",
      "trigger": "Xuất hóa đơn GTGT, nhận tiền mặt hoặc chuyển khoản",
      "request_schema": {
        "properties": {
          "invoice_id": { "type": "string" },
          "invoice_date": { "$ref": "#/$defs/Date" },
          "customer_id": { "$ref": "#/$defs/UUID" },
          "payment_method": { "$ref": "#/$defs/PaymentMethod" },
          "revenue_amount_vnd": { "$ref": "#/$defs/Decimal" },
          "vat_rate": { "$ref": "#/$defs/VatRate" },
          "accounting_period_id": { "$ref": "#/$defs/UUID" }
        },
        "required": ["invoice_id", "invoice_date", "customer_id", "payment_method", "revenue_amount_vnd", "vat_rate", "accounting_period_id"]
      },
      "journal_template": [
        { "account_code": "111|112", "debit": "{{revenue_amount_vnd * (1 + vat_rate)}}", "credit": 0, "description": "Tổng tiền thu" },
        { "account_code": "511", "debit": 0, "credit": "{{revenue_amount_vnd}}", "description": "Doanh thu chưa VAT" },
        { "account_code": "33311", "debit": 0, "credit": "{{revenue_amount_vnd * vat_rate}}", "description": "Thuế GTGT đầu ra" }
      ],
      "validation_rules": ["revenue_amount_vnd >= 0", "vat_rate IN [0, 0.05, 0.08, 0.1]", "period_status == 'OPEN'"],
      "compliance_ref": "TT99/2025 - TK 511, 33311, 111/112"
    },
    {
      "id": "S02",
      "name": "Bán hàng ghi công nợ (bán chịu)",
      "domain": "SALES",
      "trigger": "Xuất hóa đơn GTGT, chưa thu tiền",
      "request_schema": {
        "properties": {
          "invoice_id": { "type": "string" },
          "invoice_date": { "$ref": "#/$defs/Date" },
          "customer_id": { "$ref": "#/$defs/UUID" },
          "due_date": { "$ref": "#/$defs/Date" },
          "revenue_amount_vnd": { "$ref": "#/$defs/Decimal" },
          "vat_rate": { "$ref": "#/$defs/VatRate" },
          "accounting_period_id": { "$ref": "#/$defs/UUID" }
        },
        "required": ["invoice_id", "invoice_date", "customer_id", "due_date", "revenue_amount_vnd", "vat_rate", "accounting_period_id"]
      },
      "journal_template": [
        { "account_code": "131", "debit": "{{revenue_amount_vnd * (1 + vat_rate)}}", "credit": 0, "description": "Phải thu khách hàng" },
        { "account_code": "511", "debit": 0, "credit": "{{revenue_amount_vnd}}", "description": "Doanh thu bán hàng" },
        { "account_code": "33311", "debit": 0, "credit": "{{revenue_amount_vnd * vat_rate}}", "description": "Thuế GTGT đầu ra" }
      ],
      "validation_rules": ["due_date >= invoice_date", "revenue_amount_vnd > 0"],
      "compliance_ref": "TT99/2025 - TK 131, 511, 33311"
    },
    {
      "id": "S03",
      "name": "Xuất kho ghi nhận giá vốn",
      "domain": "SALES",
      "trigger": "Xuất kho hàng hóa/thành phẩm giao khách",
      "request_schema": {
        "properties": {
          "delivery_id": { "type": "string" },
          "delivery_date": { "$ref": "#/$defs/Date" },
          "sales_invoice_id": { "type": "string" },
          "inventory_lines": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "inventory_item_id": { "$ref": "#/$defs/UUID" },
                "quantity": { "$ref": "#/$defs/Decimal" },
                "unit_cost_vnd": { "$ref": "#/$defs/Decimal" },
                "inventory_account": { "type": "string", "enum": ["155", "156"] }
              },
              "required": ["inventory_item_id", "quantity", "unit_cost_vnd", "inventory_account"]
            }
          },
          "accounting_period_id": { "$ref": "#/$defs/UUID" }
        },
        "required": ["delivery_id", "delivery_date", "sales_invoice_id", "inventory_lines", "accounting_period_id"]
      },
      "journal_template": [
        { "account_code": "632", "debit": "{{SUM(line.quantity * line.unit_cost_vnd)}}", "credit": 0, "description": "Giá vốn hàng bán" },
        { "account_code": "155|156", "debit": 0, "credit": "{{line.quantity * line.unit_cost_vnd}}", "description": "Xuất kho" }
      ],
      "validation_rules": ["quantity <= available_stock", "unit_cost_vnd > 0", "costing_method_consistent"],
      "compliance_ref": "TT99/2025 - TK 632, 155/156"
    },
    {
      "id": "S04",
      "name": "Chiết khấu thương mại, giảm giá hàng bán",
      "domain": "SALES",
      "trigger": "Phát sinh chiết khấu TM hoặc giảm giá theo hợp đồng",
      "request_schema": {
        "properties": {
          "adjustment_id": { "type": "string" },
          "adjustment_date": { "$ref": "#/$defs/Date" },
          "original_invoice_id": { "type": "string" },
          "customer_id": { "$ref": "#/$defs/UUID" },
          "discount_amount_vnd": { "$ref": "#/$defs/Decimal" },
          "is_cash_refund": { "type": "boolean" },
          "accounting_period_id": { "$ref": "#/$defs/UUID" }
        },
        "required": ["adjustment_id", "adjustment_date", "original_invoice_id", "customer_id", "discount_amount_vnd", "accounting_period_id"]
      },
      "journal_template": [
        { "account_code": "521", "debit": "{{discount_amount_vnd}}", "credit": 0, "description": "Giảm trừ doanh thu" },
        { "account_code": "131|111", "debit": 0, "credit": "{{discount_amount_vnd}}", "description": "Giảm công nợ hoặc hoàn tiền" }
      ],
      "validation_rules": ["discount_amount_vnd <= original_revenue", "requires_adjustment_invoice"],
      "compliance_ref": "TT99/2025 - TK 521, 131/111"
    },
    {
      "id": "S05",
      "name": "Hàng bán bị trả lại",
      "domain": "SALES",
      "trigger": "Biên bản trả hàng + hóa đơn điều chỉnh",
      "request_schema": {
        "properties": {
          "return_id": { "type": "string" },
          "return_date": { "$ref": "#/$defs/Date" },
          "original_invoice_id": { "type": "string" },
          "customer_id": { "$ref": "#/$defs/UUID" },
          "return_amount_vnd": { "$ref": "#/$defs/Decimal" },
          "return_vat_amount_vnd": { "$ref": "#/$defs/Decimal" },
          "return_cost_vnd": { "$ref": "#/$defs/Decimal" },
          "accounting_period_id": { "$ref": "#/$defs/UUID" }
        },
        "required": ["return_id", "return_date", "original_invoice_id", "customer_id", "return_amount_vnd", "return_vat_amount_vnd", "return_cost_vnd", "accounting_period_id"]
      },
      "journal_template": [
        { "account_code": "521", "debit": "{{return_amount_vnd}}", "credit": 0, "description": "Hàng bán bị trả lại" },
        { "account_code": "33311", "debit": "{{return_vat_amount_vnd}}", "credit": 0, "description": "Điều chỉnh VAT đầu ra" },
        { "account_code": "131", "debit": 0, "credit": "{{return_amount_vnd + return_vat_amount_vnd}}", "description": "Giảm phải thu" },
        { "account_code": "156", "debit": "{{return_cost_vnd}}", "credit": 0, "description": "Nhập kho hàng trả" },
        { "account_code": "632", "debit": 0, "credit": "{{return_cost_vnd}}", "description": "Giảm giá vốn" }
      ],
      "validation_rules": ["return_amount_vnd + return_vat_amount_vnd <= original_total", "return_cost_vnd > 0"],
      "compliance_ref": "TT99/2025 - TK 521, 33311, 131, 156, 632"
    },
    {
      "id": "P01",
      "name": "Mua hàng hóa nhập kho (mua chịu)",
      "domain": "PURCHASE",
      "trigger": "Nhận hàng + hóa đơn GTGT của NCC",
      "request_schema": {
        "properties": {
          "supplier_invoice_id": { "type": "string" },
          "invoice_date": { "$ref": "#/$defs/Date" },
          "supplier_id": { "$ref": "#/$defs/UUID" },
          "payment_terms_days": { "type": "integer", "minimum": 0 },
          "goods_value_vnd": { "$ref": "#/$defs/Decimal" },
          "vat_amount_vnd": { "$ref": "#/$defs/Decimal" },
          "additional_costs_vnd": { "$ref": "#/$defs/Decimal" },
          "accounting_period_id": { "$ref": "#/$defs/UUID" }
        },
        "required": ["supplier_invoice_id", "invoice_date", "supplier_id", "payment_terms_days", "goods_value_vnd", "vat_amount_vnd", "accounting_period_id"]
      },
      "journal_template": [
        { "account_code": "156", "debit": "{{goods_value_vnd + additional_costs_vnd}}", "credit": 0, "description": "Giá trị hàng nhập kho" },
        { "account_code": "1331", "debit": "{{vat_amount_vnd}}", "credit": 0, "description": "Thuế GTGT đầu vào" },
        { "account_code": "331", "debit": 0, "credit": "{{goods_value_vnd + vat_amount_vnd + additional_costs_vnd}}", "description": "Phải trả NCC" }
      ],
      "validation_rules": ["goods_value_vnd >= 0", "vat_amount_vnd == goods_value_vnd * vat_rate"],
      "compliance_ref": "TT99/2025 - TK 156, 1331, 331"
    },
    {
      "id": "P02",
      "name": "Mua nguyên vật liệu nhập kho",
      "domain": "PURCHASE",
      "trigger": "Hóa đơn mua NVL + phiếu nhập kho",
      "request_schema": {
        "properties": {
          "supplier_invoice_id": { "type": "string" },
          "invoice_date": { "$ref": "#/$defs/Date" },
          "supplier_id": { "$ref": "#/$defs/UUID" },
          "material_value_vnd": { "$ref": "#/$defs/Decimal" },
          "vat_amount_vnd": { "$ref": "#/$defs/Decimal" },
          "payment_method": { "$ref": "#/$defs/PaymentMethod" },
          "accounting_period_id": { "$ref": "#/$defs/UUID" }
        },
        "required": ["supplier_invoice_id", "invoice_date", "supplier_id", "material_value_vnd", "vat_amount_vnd", "accounting_period_id"]
      },
      "journal_template": [
        { "account_code": "152", "debit": "{{material_value_vnd}}", "credit": 0, "description": "Giá trị NVL nhập kho" },
        { "account_code": "1331", "debit": "{{vat_amount_vnd}}", "credit": 0, "description": "VAT đầu vào" },
        { "account_code": "331|112", "debit": 0, "credit": "{{material_value_vnd + vat_amount_vnd}}", "description": "Phải trả hoặc thanh toán" }
      ],
      "validation_rules": ["material_value_vnd > 0", "period_status == 'OPEN'"],
      "compliance_ref": "TT99/2025 - TK 152, 1331, 331/112"
    },
    {
      "id": "T01",
      "name": "Thanh toán công nợ phải trả NCC",
      "domain": "PAYMENT",
      "trigger": "Lệnh chuyển tiền / phiếu chi tiền mặt",
      "request_schema": {
        "properties": {
          "payment_id": { "type": "string" },
          "payment_date": { "$ref": "#/$defs/Date" },
          "supplier_id": { "$ref": "#/$defs/UUID" },
          "payment_method": { "$ref": "#/$defs/PaymentMethod" },
          "payment_amount_vnd": { "$ref": "#/$defs/Decimal" },
          "applied_invoices": { "type": "array", "items": { "type": "string" } },
          "bank_account_id": { "$ref": "#/$defs/UUID" },
          "accounting_period_id": { "$ref": "#/$defs/UUID" }
        },
        "required": ["payment_id", "payment_date", "supplier_id", "payment_method", "payment_amount_vnd", "accounting_period_id"]
      },
      "journal_template": [
        { "account_code": "331", "debit": "{{payment_amount_vnd}}", "credit": 0, "description": "Giảm phải trả NCC" },
        { "account_code": "112|111", "debit": 0, "credit": "{{payment_amount_vnd}}", "description": "Xuất tiền thanh toán" }
      ],
      "validation_rules": ["payment_amount_vnd <= outstanding_331_balance", "bank_account_id required if payment_method == 'BANK_TRANSFER'"],
      "compliance_ref": "TT99/2025 - TK 331, 111/112"
    },
    {
      "id": "T02",
      "name": "Thu tiền khách hàng (thu hồi công nợ)",
      "domain": "PAYMENT",
      "trigger": "Giấy báo có ngân hàng / phiếu thu tiền mặt",
      "request_schema": {
        "properties": {
          "receipt_id": { "type": "string" },
          "receipt_date": { "$ref": "#/$defs/Date" },
          "customer_id": { "$ref": "#/$defs/UUID" },
          "payment_method": { "$ref": "#/$defs/PaymentMethod" },
          "receipt_amount_vnd": { "$ref": "#/$defs/Decimal" },
          "applied_invoices": { "type": "array", "items": { "type": "string" } },
          "accounting_period_id": { "$ref": "#/$defs/UUID" }
        },
        "required": ["receipt_id", "receipt_date", "customer_id", "payment_method", "receipt_amount_vnd", "accounting_period_id"]
      },
      "journal_template": [
        { "account_code": "112|111", "debit": "{{receipt_amount_vnd}}", "credit": 0, "description": "Tiền về" },
        { "account_code": "131", "debit": 0, "credit": "{{receipt_amount_vnd}}", "description": "Giảm phải thu KH" }
      ],
      "validation_rules": ["receipt_amount_vnd <= outstanding_131_balance", "period_status == 'OPEN'"],
      "compliance_ref": "TT99/2025 - TK 111/112, 131"
    },
    {
      "id": "T03",
      "name": "Tạm ứng tiền cho nhân viên",
      "domain": "PAYMENT",
      "trigger": "Giấy đề nghị tạm ứng được duyệt",
      "request_schema": {
        "properties": {
          "advance_id": { "type": "string" },
          "advance_date": { "$ref": "#/$defs/Date" },
          "employee_id": { "$ref": "#/$defs/UUID" },
          "advance_amount_vnd": { "$ref": "#/$defs/Decimal" },
          "payment_method": { "$ref": "#/$defs/PaymentMethod" },
          "purpose": { "type": "string" },
          "accounting_period_id": { "$ref": "#/$defs/UUID" }
        },
        "required": ["advance_id", "advance_date", "employee_id", "advance_amount_vnd", "payment_method", "purpose", "accounting_period_id"]
      },
      "journal_template": [
        { "account_code": "141", "debit": "{{advance_amount_vnd}}", "credit": 0, "description": "Tạm ứng nhân viên" },
        { "account_code": "111|112", "debit": 0, "credit": "{{advance_amount_vnd}}", "description": "Xuất tiền tạm ứng" }
      ],
      "validation_rules": ["advance_amount_vnd > 0", "employee_active == true"],
      "compliance_ref": "TT99/2025 - TK 141, 111/112"
    },
    {
      "id": "X01",
      "name": "Kê khai và nộp thuế GTGT hàng tháng/quý",
      "domain": "TAX",
      "trigger": "Kỳ kê khai VAT (tháng hoặc quý)",
      "request_schema": {
        "properties": {
          "declaration_period_id": { "type": "string" },
          "declaration_date": { "$ref": "#/$defs/Date" },
          "output_vat_total": { "$ref": "#/$defs/Decimal" },
          "input_vat_total": { "$ref": "#/$defs/Decimal" },
          "payment_method": { "$ref": "#/$defs/PaymentMethod" },
          "bank_account_id": { "$ref": "#/$defs/UUID" },
          "accounting_period_id": { "$ref": "#/$defs/UUID" }
        },
        "required": ["declaration_period_id", "declaration_date", "output_vat_total", "input_vat_total", "accounting_period_id"]
      },
      "journal_template": [
        { "account_code": "33311", "debit": "{{MIN(output_vat_total, input_vat_total)}}", "credit": 0, "description": "Bù trừ VAT đầu ra" },
        { "account_code": "1331", "debit": 0, "credit": "{{MIN(output_vat_total, input_vat_total)}}", "description": "Bù trừ VAT đầu vào" },
        { "account_code": "3331", "debit": 0, "credit": "{{MAX(0, output_vat_total - input_vat_total)}}", "description": "VAT còn phải nộp" },
        { "account_code": "112", "debit": "{{MAX(0, output_vat_total - input_vat_total)}}", "credit": 0, "description": "Nộp ngân sách" }
      ],
      "validation_rules": ["output_vat_total >= 0", "input_vat_total >= 0", "bank_account_id required if net_vat_payable > 0"],
      "compliance_ref": "TT99/2025 - TK 33311, 1331, 3331, 112"
    },
    {
      "id": "X02",
      "name": "Hạch toán chi phí thuế TNDN hiện hành",
      "domain": "TAX",
      "trigger": "Lập tờ khai thuế TNDN tạm tính / quyết toán",
      "request_schema": {
        "properties": {
          "tax_period_id": { "type": "string" },
          "calculation_date": { "$ref": "#/$defs/Date" },
          "taxable_income_vnd": { "$ref": "#/$defs/Decimal" },
          "cit_rate": { "type": "number", "enum": [0.2, 0.1, 0.15, 0.03, 0.17, 0.05, 0.08, 0.1] },
          "accounting_period_id": { "$ref": "#/$defs/UUID" }
        },
        "required": ["tax_period_id", "calculation_date", "taxable_income_vnd", "cit_rate", "accounting_period_id"]
      },
      "journal_template": [
        { "account_code": "8211", "debit": "{{taxable_income_vnd * cit_rate}}", "credit": 0, "description": "Chi phí thuế TNDN hiện hành" },
        { "account_code": "3334", "debit": 0, "credit": "{{taxable_income_vnd * cit_rate}}", "description": "Thuế TNDN phải nộp" }
      ],
      "validation_rules": ["cit_rate IN [0.2, 0.1, 0.15]", "taxable_income_vnd >= 0"],
      "compliance_ref": "TT99/2025 - TK 8211, 3334"
    },
    {
      "id": "X03",
      "name": "Hạch toán và nộp thuế TNCN từ tiền lương",
      "domain": "TAX",
      "trigger": "Bảng lương tháng được duyệt",
      "request_schema": {
        "properties": {
          "payroll_period_id": { "type": "string" },
          "withholding_date": { "$ref": "#/$defs/Date" },
          "total_pit_withheld_vnd": { "$ref": "#/$defs/Decimal" },
          "payment_date": { "$ref": "#/$defs/Date" },
          "bank_account_id": { "$ref": "#/$defs/UUID" },
          "accounting_period_id": { "$ref": "#/$defs/UUID" }
        },
        "required": ["payroll_period_id", "withholding_date", "total_pit_withheld_vnd", "payment_date", "bank_account_id", "accounting_period_id"]
      },
      "journal_template": [
        { "account_code": "334", "debit": "{{total_pit_withheld_vnd}}", "credit": 0, "description": "Khấu trừ TNCN từ lương" },
        { "account_code": "3335", "debit": 0, "credit": "{{total_pit_withheld_vnd}}", "description": "Thuế TNCN phải nộp" },
        { "account_code": "3335", "debit": "{{total_pit_withheld_vnd}}", "credit": 0, "description": "Nộp thuế TNCN" },
        { "account_code": "112", "debit": 0, "credit": "{{total_pit_withheld_vnd}}", "description": "Xuất tiền nộp thuế" }
      ],
      "validation_rules": ["total_pit_withheld_vnd >= 0", "payment_date >= withholding_date"],
      "compliance_ref": "TT99/2025 - TK 334, 3335, 112"
    },
    {
      "id": "A01",
      "name": "Mua tài sản cố định",
      "domain": "ASSET_INVENTORY",
      "trigger": "Biên bản bàn giao TSCĐ + hóa đơn",
      "request_schema": {
        "properties": {
          "asset_handover_id": { "type": "string" },
          "handover_date": { "$ref": "#/$defs/Date" },
          "asset_type": { "type": "string", "enum": ["TANGIBLE", "INTANGIBLE", "LEASED"] },
          "original_cost_vnd": { "$ref": "#/$defs/Decimal" },
          "vat_amount_vnd": { "$ref": "#/$defs/Decimal" },
          "supplier_id": { "$ref": "#/$defs/UUID" },
          "payment_method": { "$ref": "#/$defs/PaymentMethod" },
          "accounting_period_id": { "$ref": "#/$defs/UUID" }
        },
        "required": ["asset_handover_id", "handover_date", "asset_type", "original_cost_vnd", "vat_amount_vnd", "supplier_id", "accounting_period_id"]
      },
      "journal_template": [
        { "account_code": "211|213|212", "debit": "{{original_cost_vnd}}", "credit": 0, "description": "Nguyên giá TSCĐ" },
        { "account_code": "1332", "debit": "{{vat_amount_vnd}}", "credit": 0, "description": "VAT TSCĐ đầu vào" },
        { "account_code": "331|112", "debit": 0, "credit": "{{original_cost_vnd + vat_amount_vnd}}", "description": "Phải trả hoặc thanh toán" }
      ],
      "validation_rules": ["original_cost_vnd >= 10000000", "useful_life_months >= 12"],
      "compliance_ref": "TT99/2025 - TK 211/212/213, 1332, 331/112"
    },
    {
      "id": "A02",
      "name": "Trích khấu hao TSCĐ hàng tháng",
      "domain": "ASSET_INVENTORY",
      "trigger": "Cuối tháng, dựa trên bảng khấu hao",
      "request_schema": {
        "properties": {
          "depreciation_period_id": { "type": "string" },
          "calculation_date": { "$ref": "#/$defs/Date" },
          "assets": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "asset_id": { "$ref": "#/$defs/UUID" },
                "department": { "type": "string", "enum": ["PRODUCTION", "SALES", "ADMIN"] },
                "monthly_depreciation_vnd": { "$ref": "#/$defs/Decimal" }
              },
              "required": ["asset_id", "department", "monthly_depreciation_vnd"]
            }
          },
          "accounting_period_id": { "$ref": "#/$defs/UUID" }
        },
        "required": ["depreciation_period_id", "calculation_date", "assets", "accounting_period_id"]
      },
      "journal_template": [
        { "account_code": "627|641|642", "debit": "{{SUM(depreciation)}}", "credit": 0, "description": "CP khấu hao" },
        { "account_code": "2141|2143", "debit": 0, "credit": "{{SUM(depreciation)}}", "description": "Hao mòn lũy kế" }
      ],
      "validation_rules": ["monthly_depreciation_vnd > 0", "department_mapping_correct"],
      "compliance_ref": "TT99/2025 - TK 627/641/642, 2141/2143"
    },
    {
      "id": "L01",
      "name": "Tính lương và các khoản phải trả NLĐ",
      "domain": "PAYROLL",
      "trigger": "Bảng lương tháng được Giám đốc duyệt",
      "request_schema": {
        "properties": {
          "payroll_id": { "type": "string" },
          "payroll_month": { "$ref": "#/$defs/Date" },
          "total_gross_vnd": { "$ref": "#/$defs/Decimal" },
          "employee_deductions_vnd": { "$ref": "#/$defs/Decimal" },
          "net_pay_vnd": { "$ref": "#/$defs/Decimal" },
          "department_allocation": { "type": "object", "additionalProperties": { "$ref": "#/$defs/Decimal" } },
          "accounting_period_id": { "$ref": "#/$defs/UUID" }
        },
        "required": ["payroll_id", "payroll_month", "total_gross_vnd", "employee_deductions_vnd", "net_pay_vnd", "accounting_period_id"]
      },
      "journal_template": [
        { "account_code": "622|641|642|627", "debit": "{{total_gross_vnd}}", "credit": 0, "description": "Chi phí lương" },
        { "account_code": "334", "debit": 0, "credit": "{{net_pay_vnd}}", "description": "Lương phải trả" },
        { "account_code": "3383|3384|3386", "debit": 0, "credit": "{{employee_deductions_vnd}}", "description": "BHXH/BHYT/BHTN phần NLĐ" }
      ],
      "validation_rules": ["net_pay_vnd == total_gross_vnd - employee_deductions_vnd", "department_allocation_sum == total_gross_vnd"],
      "compliance_ref": "TT99/2025 - TK 622/641/642/627, 334, 338x"
    },
    {
      "id": "L02",
      "name": "Trích bảo hiểm xã hội phần doanh nghiệp",
      "domain": "PAYROLL",
      "trigger": "Bảng lương tháng + tỷ lệ trích theo quy định",
      "request_schema": {
        "properties": {
          "payroll_id": { "type": "string" },
          "calculation_date": { "$ref": "#/$defs/Date" },
          "employer_contributions": {
            "type": "object",
            "properties": {
              "bhxh_17_5": { "$ref": "#/$defs/Decimal" },
              "bhyt_3_0": { "$ref": "#/$defs/Decimal" },
              "bhtn_1_0": { "$ref": "#/$defs/Decimal" },
              "kpcd_2_0": { "$ref": "#/$defs/Decimal" }
            },
            "required": ["bhxh_17_5", "bhyt_3_0", "bhtn_1_0", "kpcd_2_0"]
          },
          "accounting_period_id": { "$ref": "#/$defs/UUID" }
        },
        "required": ["payroll_id", "calculation_date", "employer_contributions", "accounting_period_id"]
      },
      "journal_template": [
        { "account_code": "622|641|642", "debit": "{{SUM(contributions)}}", "credit": 0, "description": "CP BHXH DN" },
        { "account_code": "3382|3383|3384|3386", "debit": 0, "credit": "{{SUM(contributions)}}", "description": "Trích theo lương phải nộp" }
      ],
      "validation_rules": ["contributions_calculated_on_valid_base", "rates_match_current_law"],
      "compliance_ref": "TT99/2025 - TK 622/641/642, 3382/3383/3384/3386"
    },
    {
      "id": "L03",
      "name": "Chi lương cho người lao động",
      "domain": "PAYROLL",
      "trigger": "Ngày trả lương hàng tháng",
      "request_schema": {
        "properties": {
          "payment_batch_id": { "type": "string" },
          "payment_date": { "$ref": "#/$defs/Date" },
          "total_net_pay_vnd": { "$ref": "#/$defs/Decimal" },
          "payment_method": { "$ref": "#/$defs/PaymentMethod" },
          "bank_transfer_file_ref": { "type": "string" },
          "accounting_period_id": { "$ref": "#/$defs/UUID" }
        },
        "required": ["payment_batch_id", "payment_date", "total_net_pay_vnd", "payment_method", "accounting_period_id"]
      },
      "journal_template": [
        { "account_code": "334", "debit": "{{total_net_pay_vnd}}", "credit": 0, "description": "Lương phải trả" },
        { "account_code": "112|111", "debit": 0, "credit": "{{total_net_pay_vnd}}", "description": "Tiền chuyển khoản / tiền mặt" }
      ],
      "validation_rules": ["total_net_pay_vnd == SUM(pending_334_balances)", "payment_date >= payroll_approval_date"],
      "compliance_ref": "TT99/2025 - TK 334, 111/112"
    },
    {
      "id": "G01",
      "name": "Kết chuyển doanh thu về tài khoản xác định KQKD",
      "domain": "GENERAL_LEDGER",
      "trigger": "Bút toán cuối kỳ kế toán",
      "request_schema": {
        "properties": {
          "closing_period_id": { "type": "string" },
          "closing_date": { "$ref": "#/$defs/Date" },
          "revenue_balances": {
            "type": "object",
            "properties": {
              "511_credit": { "$ref": "#/$defs/Decimal" },
              "515_credit": { "$ref": "#/$defs/Decimal" },
              "711_credit": { "$ref": "#/$defs/Decimal" }
            }
          },
          "contra_revenue_balances": {
            "type": "object",
            "properties": { "521_debit": { "$ref": "#/$defs/Decimal" } }
          },
          "accounting_period_id": { "$ref": "#/$defs/UUID" }
        },
        "required": ["closing_period_id", "closing_date", "revenue_balances", "accounting_period_id"]
      },
      "journal_template": [
        { "account_code": "511|515|711", "debit": "{{SUM(revenue)}}", "credit": 0, "description": "Kết chuyển doanh thu" },
        { "account_code": "911", "debit": 0, "credit": "{{SUM(revenue) - contra_521}}", "description": "Tổng doanh thu thuần" },
        { "account_code": "521", "debit": 0, "credit": "{{contra_521}}", "description": "Kết chuyển giảm trừ" }
      ],
      "validation_rules": ["is_closing_entry == true", "period_status in ['OPEN', 'CLOSING']", "all_revenue_accounts_zeroed_after"],
      "compliance_ref": "TT99/2025 - TK 511, 515, 711, 521, 911"
    },
    {
      "id": "G02",
      "name": "Kết chuyển chi phí về tài khoản xác định KQKD",
      "domain": "GENERAL_LEDGER",
      "trigger": "Bút toán cuối kỳ kế toán",
      "request_schema": {
        "properties": {
          "closing_period_id": { "type": "string" },
          "closing_date": { "$ref": "#/$defs/Date" },
          "expense_balances": {
            "type": "object",
            "properties": {
              "632_debit": { "$ref": "#/$defs/Decimal" },
              "635_debit": { "$ref": "#/$defs/Decimal" },
              "641_debit": { "$ref": "#/$defs/Decimal" },
              "642_debit": { "$ref": "#/$defs/Decimal" },
              "811_debit": { "$ref": "#/$defs/Decimal" },
              "821_debit": { "$ref": "#/$defs/Decimal" }
            }
          },
          "accounting_period_id": { "$ref": "#/$defs/UUID" }
        },
        "required": ["closing_period_id", "closing_date", "expense_balances", "accounting_period_id"]
      },
      "journal_template": [
        { "account_code": "911", "debit": "{{SUM(expenses)}}", "credit": 0, "description": "Tổng chi phí kết chuyển" },
        { "account_code": "632|635|641|642|811|821", "debit": 0, "credit": "{{individual_expense}}", "description": "Kết chuyển chi phí" }
      ],
      "validation_rules": ["G01_must_be_posted_first", "all_expense_accounts_zeroed_after"],
      "compliance_ref": "TT99/2025 - TK 911, 632, 635, 641, 642, 811, 821"
    },
    {
      "id": "G03",
      "name": "Kết chuyển lợi nhuận sau thuế",
      "domain": "GENERAL_LEDGER",
      "trigger": "Cuối năm tài chính sau khi xác định đủ CP thuế TNDN",
      "request_schema": {
        "properties": {
          "fiscal_year_id": { "type": "string" },
          "closing_date": { "$ref": "#/$defs/Date" },
          "profit_after_tax_vnd": { "type": "number" },
          "accounting_period_id": { "$ref": "#/$defs/UUID" }
        },
        "required": ["fiscal_year_id", "closing_date", "profit_after_tax_vnd", "accounting_period_id"]
      },
      "journal_template": [
        { "account_code": "911", "debit": "{{MAX(0, profit_after_tax_vnd)}}", "credit": "{{MAX(0, -profit_after_tax_vnd)}}", "description": "Kết chuyển lãi/lỗ" },
        { "account_code": "4212", "debit": "{{MAX(0, -profit_after_tax_vnd)}}", "credit": "{{MAX(0, profit_after_tax_vnd)}}", "description": "LNST chưa phân phối năm nay" }
      ],
      "validation_rules": ["profit_after_tax_vnd == 911_credit - 911_debit", "is_fiscal_year_end == true"],
      "compliance_ref": "TT99/2025 - TK 911, 4212"
    },
    {
      "id": "G04",
      "name": "Phân bổ chi phí trả trước (242)",
      "domain": "GENERAL_LEDGER",
      "trigger": "Cuối mỗi kỳ kế toán theo bảng phân bổ",
      "request_schema": {
        "properties": {
          "allocation_period_id": { "type": "string" },
          "allocation_date": { "$ref": "#/$defs/Date" },
          "prepaid_items": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "contract_id": { "type": "string" },
                "remaining_balance_vnd": { "$ref": "#/$defs/Decimal" },
                "period_allocation_vnd": { "$ref": "#/$defs/Decimal" },
                "target_account": { "type": "string", "enum": ["641", "642", "627"] }
              },
              "required": ["contract_id", "remaining_balance_vnd", "period_allocation_vnd", "target_account"]
            }
          },
          "accounting_period_id": { "$ref": "#/$defs/UUID" }
        },
        "required": ["allocation_period_id", "allocation_date", "prepaid_items", "accounting_period_id"]
      },
      "journal_template": [
        { "account_code": "641|642|627", "debit": "{{SUM(period_allocation)}}", "credit": 0, "description": "Chi phí kỳ này" },
        { "account_code": "242", "debit": 0, "credit": "{{SUM(period_allocation)}}", "description": "Giảm chi phí chờ phân bổ" }
      ],
      "validation_rules": ["period_allocation_vnd <= remaining_balance_vnd", "allocation_schedule_approved"],
      "compliance_ref": "TT99/2025 - TK 242, 641/642/627"
    }
  ]
}
```