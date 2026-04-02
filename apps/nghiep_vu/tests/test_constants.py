"""Tests for nghiep_vu constants and tax calculations."""

import pytest
from decimal import Decimal

from apps.nghiep_vu.constants import (
    THUE_SUAT_GTGT,
    THUE_SUAT_GTGT_2026,
    THUE_SUAT_TNDN_SME,
    THUE_SUAT_TNDN_DEFAULT,
    NGUONG_DOANH_THU_SME,
    THUE_TNCN_BRACKETS,
    THUE_TNCN_GIAM_TRU_GIA_CANH,
    THUE_TNCN_GIAM_TRU_PHU_THUOC,
)
from apps.nghiep_vu.services import (
    tinh_thue_gtgt,
    tinh_thue_tndn_sme,
    tinh_thue_tndn,
)


class TestThueSuatGtgt2026:
    """Tests for VAT rate constants 2026."""

    def test_thue_suat_gtgt_2026_has_4_rates(self):
        """Test THUE_SUAT_GTGT_2026 has exactly 4 rates."""
        assert len(THUE_SUAT_GTGT_2026) == 4

    def test_thue_suat_gtgt_2026_values(self):
        """Test THUE_SUAT_GTGT_2026 has correct rate values."""
        rates = [v[0] for v in THUE_SUAT_GTGT_2026]
        assert rates == ['0', '5', '8', '10']

    def test_thue_suat_gtgt_2026_labels(self):
        """Test THUE_SUAT_GTGT_2026 has correct labels."""
        labels = [v[1] for v in THUE_SUAT_GTGT_2026]
        assert '0% - Không chịu thuế' in labels
        assert '5% - Nông, thủy sản,..' in labels
        assert '8% - Giảm theo NĐ 70/2025' in labels
        assert '10% - Thuế suất tiêu chuẩn' in labels

    def test_thue_suat_gtgt_dict_exists(self):
        """Test THUE_SUAT_GTGT dict exists with correct values."""
        assert THUE_SUAT_GTGT['0'] == Decimal('0')
        assert THUE_SUAT_GTGT['5'] == Decimal('0.05')
        assert THUE_SUAT_GTGT['8'] == Decimal('0.08')
        assert THUE_SUAT_GTGT['10'] == Decimal('0.10')


class TestThueTndnConstants:
    """Tests for TNDN tax constants."""

    def test_tndn_sme_rate(self):
        """Test SME TNDN rate is 15%."""
        assert THUE_SUAT_TNDN_SME == Decimal('0.15')

    def test_tndn_default_rate(self):
        """Test default TNDN rate is 20%."""
        assert THUE_SUAT_TNDN_DEFAULT == Decimal('0.20')

    def test_sme_threshold(self):
        """Test SME revenue threshold is 3 billion VND."""
        assert NGUONG_DOANH_THU_SME == Decimal('3000000000')


class TestThueTncnConstants:
    """Tests for TNCN (Personal Income Tax) constants."""

    def test_tncn_brackets_count(self):
        """Test TNCN has 7 tax brackets."""
        assert len(THUE_TNCN_BRACKETS) == 7

    def test_tncn_first_bracket(self):
        """Test first bracket: 0-11M at 5%."""
        low, high, rate = THUE_TNCN_BRACKETS[0]
        assert low == Decimal('0')
        assert high == Decimal('11000000')
        assert rate == Decimal('0.05')

    def test_tncn_last_bracket(self):
        """Test last bracket: 198M+ at 35%."""
        low, high, rate = THUE_TNCN_BRACKETS[-1]
        assert low == Decimal('198000000')
        assert high is None
        assert rate == Decimal('0.35')

    def test_tncn_bracket_progression(self):
        """Test brackets are progressive."""
        for i in range(len(THUE_TNCN_BRACKETS) - 1):
            _, _, rate_curr = THUE_TNCN_BRACKETS[i]
            _, _, rate_next = THUE_TNCN_BRACKETS[i + 1]
            assert rate_next > rate_curr

    def test_tncn_giam_tru_gia_canh(self):
        """Test personal deduction is 11 million VND."""
        assert THUE_TNCN_GIAM_TRU_GIA_CANH == Decimal('11000000')

    def test_tncn_giam_tru_phu_thuoc(self):
        """Test dependent deduction is 4.4 million VND."""
        assert THUE_TNCN_GIAM_TRU_PHU_THUOC == Decimal('4400000')


class TestTinhThueGtgt:
    """Tests for VAT calculation service."""

    def test_0_percent(self):
        """Test 0% VAT rate."""
        result = tinh_thue_gtgt(Decimal('1000000'), '0')
        assert result == Decimal('0')

    def test_5_percent(self):
        """Test 5% VAT rate."""
        result = tinh_thue_gtgt(Decimal('1000000'), '5')
        assert result == Decimal('50000')

    def test_8_percent(self):
        """Test 8% VAT rate."""
        result = tinh_thue_gtgt(Decimal('1000000'), '8')
        assert result == Decimal('80000')

    def test_10_percent(self):
        """Test 10% VAT rate."""
        result = tinh_thue_gtgt(Decimal('1000000'), '10')
        assert result == Decimal('100000')

    def test_invalid_rate_raises(self):
        """Test invalid rate raises ValidationError."""
        from django.core.exceptions import ValidationError
        with pytest.raises(ValidationError):
            tinh_thue_gtgt(Decimal('1000000'), '15')

    def test_negative_amount_raises(self):
        """Test negative amount raises ValidationError."""
        from django.core.exceptions import ValidationError
        with pytest.raises(ValidationError):
            tinh_thue_gtgt(Decimal('-1000000'), '10')


class TestTinhThueTndnSme:
    """Tests for SME TNDN calculation."""

    def test_positive_profit(self):
        """Test TNDN on positive profit at 15%."""
        result = tinh_thue_tndn_sme(Decimal('100000000'))
        assert result == Decimal('15000000')

    def test_zero_profit(self):
        """Test TNDN on zero profit."""
        result = tinh_thue_tndn_sme(Decimal('0'))
        assert result == Decimal('0')

    def test_negative_profit(self):
        """Test TNDN on negative profit (loss) returns 0."""
        result = tinh_thue_tndn_sme(Decimal('-50000000'))
        assert result == Decimal('0')


class TestTinhThueTndn:
    """Tests for TNDN calculation with revenue threshold."""

    def test_sme_rate_below_threshold(self):
        """Test SME rate (15%) when revenue < 3 billion."""
        result = tinh_thue_tndn(
            Decimal('2500000000'),
            Decimal('100000000'),
        )
        assert result == Decimal('15000000')

    def test_standard_rate_above_threshold(self):
        """Test standard rate (20%) when revenue >= 3 billion."""
        result = tinh_thue_tndn(
            Decimal('5000000000'),
            Decimal('100000000'),
        )
        assert result == Decimal('20000000')

    def test_negative_profit(self):
        """Test TNDN on negative profit returns 0."""
        result = tinh_thue_tndn(
            Decimal('2500000000'),
            Decimal('-100000000'),
        )
        assert result == Decimal('0')

    def test_exact_threshold(self):
        """Test at exact threshold boundary."""
        result = tinh_thue_tndn(
            Decimal('3000000000'),
            Decimal('100000000'),
        )
        assert result == Decimal('20000000')
