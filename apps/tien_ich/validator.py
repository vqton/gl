"""Validation utilities for accounting system."""

from decimal import Decimal
from typing import Any

from django.db.models import Sum

from apps.he_thong.models import SoDuDauKy


def reconcile_balances(year: int) -> dict[str, Any]:
    """
    Reconcile opening balances for a given year.

    Checks:
        1. Total Nợ = Total Có (fundamental accounting equation)
        2. Customer sub-ledger (131) matches GL balance
        3. Supplier sub-ledger (331) matches GL balance
        4. Inventory sub-ledger (156) matches GL balance
        5. Fixed asset sub-ledger (211) matches GL balance

    Args:
        year: Fiscal year to reconcile

    Returns:
        Dictionary with:
            - valid: bool - Whether reconciliation passed
            - errors: list[str] - List of error messages
            - tong_no: Decimal - Total debit balance
            - tong_co: Decimal - Total credit balance
            - sub_ledger_*: Decimal - Sub-ledger totals
            - gl_*: Decimal - GL totals

    Legal basis:
        - Thông tư 99/2025/TT-BTC on opening balance reconciliation
        - Chế độ kế toán doanh nghiệp nhỏ và vừa
    """
    result = {
        "valid": True,
        "errors": [],
        "tong_no": Decimal("0"),
        "tong_co": Decimal("0"),
    }

    balances = SoDuDauKy.objects.filter(nam=year)

    if not balances.exists():
        return result

    tong_no = balances.aggregate(total=Sum("so_du_no"))["total"] or Decimal("0")
    tong_co = balances.aggregate(total=Sum("so_du_co"))["total"] or Decimal("0")

    result["tong_no"] = tong_no
    result["tong_co"] = tong_co

    if tong_no != tong_co:
        result["valid"] = False
        chenh_lech = abs(tong_no - tong_co)
        result["errors"].append(
            f"Tổng Nợ ({tong_no:,.0f}) không bằng tổng Có ({tong_co:,.0f}). "
            f"Chênh lệch: {chenh_lech:,.0f} VND."
        )

    sub_ledger_checks = [
        ("131", "sub_ledger_131", "gl_131", "Công nợ khách hàng"),
        ("331", "sub_ledger_331", "gl_331", "Công nợ nhà cung cấp"),
        ("156", "sub_ledger_156", "gl_156", "Hàng tồn kho"),
        ("211", "sub_ledger_211", "gl_211", "Tài sản cố định"),
    ]

    for tk_code, sub_key, gl_key, label in sub_ledger_checks:
        gl_total = _get_gl_total(balances, tk_code)
        sub_total = _get_sub_ledger_total(balances, tk_code)

        result[sub_key] = sub_total
        result[gl_key] = gl_total

        if gl_total > Decimal("0") or sub_total > Decimal("0"):
            if sub_total != gl_total:
                result["valid"] = False
                result["errors"].append(
                    f"{label} (TK {tk_code}): "
                    f"Tổng chi tiết ({sub_total:,.0f}) không khớp "
                    f"với tổng kế toán ({gl_total:,.0f}). "
                    f"Chênh lệch: {abs(gl_total - sub_total):,.0f} VND."
                )

    return result


def _get_gl_total(balances, tk_code: str) -> Decimal:
    """
    Get GL total for a specific account code.

    Args:
        balances: QuerySet of SoDuDauKy
        tk_code: Account code (e.g., "131", "331")

    Returns:
        Total balance (Nợ + Có) for the account
    """
    no_total = balances.filter(tai_khoan__ma_tai_khoan=tk_code).aggregate(
        total=Sum("so_du_no")
    )["total"] or Decimal("0")

    co_total = balances.filter(tai_khoan__ma_tai_khoan=tk_code).aggregate(
        total=Sum("so_du_co")
    )["total"] or Decimal("0")

    return no_total + co_total


def _get_sub_ledger_total(balances, tk_code: str) -> Decimal:
    """
    Get sub-ledger total for accounts with doi_tuong_ma.

    For accounts like 131, 331, 156, 211, sums entries that have
    a specific object code (customer, supplier, item, asset).

    Args:
        balances: QuerySet of SoDuDauKy
        tk_code: Account code

    Returns:
        Total sub-ledger balance
    """
    sub_entries = balances.filter(
        tai_khoan__ma_tai_khoan=tk_code,
    ).exclude(
        doi_tuong_ma="",
    )

    if tk_code in ("156",):
        sub_entries = balances.filter(
            tai_khoan__ma_tai_khoan=tk_code,
            hang_hoa__isnull=False,
        )
    elif tk_code in ("211",):
        sub_entries = balances.filter(
            tai_khoan__ma_tai_khoan=tk_code,
            tai_san__isnull=False,
        )

    no_total = sub_entries.aggregate(total=Sum("so_du_no"))["total"] or Decimal("0")
    co_total = sub_entries.aggregate(total=Sum("so_du_co"))["total"] or Decimal("0")

    return no_total + co_total
