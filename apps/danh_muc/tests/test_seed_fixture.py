"""Tests for seed_accounts.json fixture."""

import json
import os
import pytest


@pytest.fixture
def fixture_path():
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "danh_muc",
        "fixtures",
        "seed_accounts.json",
    )


@pytest.fixture
def fixture_data(fixture_path):
    with open(fixture_path) as f:
        return json.load(f)


class TestSeedFixtureStructure:
    """Tests for fixture file structure."""

    def test_fixture_is_list(self, fixture_data):
        """Test fixture is a JSON list."""
        assert isinstance(fixture_data, list)

    def test_all_entries_have_model(self, fixture_data):
        """Test all entries have model field."""
        for entry in fixture_data:
            assert "model" in entry
            assert entry["model"] == "danh_muc.taikhoanketoan"

    def test_all_entries_have_fields(self, fixture_data):
        """Test all entries have required fields."""
        required = [
            "ma_tai_khoan",
            "ten_tai_khoan",
            "cap_do",
            "tai_khoan_me",
            "loai_tai_khoan",
            "mo_ta",
            "is_active",
            "is_immutable",
            "created_by",
            "updated_by",
        ]
        for entry in fixture_data:
            for field in required:
                assert field in entry["fields"], (
                    f"Missing {field} in {entry['fields'].get('ma_tai_khoan')}"
                )


class TestTier1Accounts:
    """Tests for Tier-1 accounts in fixture."""

    def test_tier1_count(self, fixture_data):
        """Test exactly 80 Tier-1 accounts."""
        tier1 = [x for x in fixture_data if x["fields"]["cap_do"] == 1]
        assert len(tier1) == 80

    def test_all_tier1_null_parent(self, fixture_data):
        """Test all Tier-1 accounts have null parent."""
        tier1 = [x for x in fixture_data if x["fields"]["cap_do"] == 1]
        for acc in tier1:
            assert acc["fields"]["tai_khoan_me"] is None

    def test_tier1_immutable(self, fixture_data):
        """Test all Tier-1 accounts are immutable."""
        tier1 = [x for x in fixture_data if x["fields"]["cap_do"] == 1]
        for acc in tier1:
            assert acc["fields"]["is_immutable"] is True

    def test_tier1_created_by_system(self, fixture_data):
        """Test all Tier-1 accounts created by system."""
        tier1 = [x for x in fixture_data if x["fields"]["cap_do"] == 1]
        for acc in tier1:
            assert acc["fields"]["created_by"] == "system"


class TestTier2Accounts:
    """Tests for Tier-2 accounts in fixture."""

    def test_tier2_count(self, fixture_data):
        """Test exactly 93 Tier-2 accounts."""
        tier2 = [x for x in fixture_data if x["fields"]["cap_do"] == 2]
        assert len(tier2) == 93

    def test_all_tier2_have_parent(self, fixture_data):
        """Test all Tier-2 accounts have a parent."""
        tier2 = [x for x in fixture_data if x["fields"]["cap_do"] == 2]
        for acc in tier2:
            assert acc["fields"]["tai_khoan_me"] is not None

    def test_all_tier2_parents_exist(self, fixture_data):
        """Test all Tier-2 parent codes exist as Tier-1."""
        tier1_codes = {
            x["fields"]["ma_tai_khoan"]
            for x in fixture_data
            if x["fields"]["cap_do"] == 1
        }
        tier2 = [x for x in fixture_data if x["fields"]["cap_do"] == 2]
        for acc in tier2:
            parent = acc["fields"]["tai_khoan_me"]
            assert parent in tier1_codes, (
                f"Parent {parent} not found for {acc['fields']['ma_tai_khoan']}"
            )


class TestWrongAccountsRemoved:
    """Test that wrong account codes are removed."""

    WRONG_CODES = [
        "268", "357", "358", "431", "441", "442", "461",
        "518", "611", "651", "881", "001", "002", "007", "008",
        "009", "315", "348", "351",
    ]

    def test_no_wrong_codes(self, fixture_data):
        """Test none of the wrong codes exist."""
        all_codes = {x["fields"]["ma_tai_khoan"] for x in fixture_data}
        for code in self.WRONG_CODES:
            assert code not in all_codes, f"Wrong code {code} still present"


class TestRequiredTier1Accounts:
    """Test that all required Tier-1 accounts exist."""

    REQUIRED_TIER1 = {
        "111": "tai_san",
        "112": "tai_san",
        "113": "tai_san",
        "121": "tai_san",
        "122": "tai_san",
        "128": "tai_san",
        "131": "tai_san",
        "133": "tai_san",
        "136": "tai_san",
        "137": "tai_san",
        "138": "tai_san",
        "139": "tai_san",
        "141": "tai_san",
        "142": "tai_san",
        "144": "tai_san",
        "151": "tai_san",
        "152": "tai_san",
        "153": "tai_san",
        "154": "tai_san",
        "155": "tai_san",
        "156": "tai_san",
        "157": "tai_san",
        "158": "tai_san",
        "161": "tai_san",
        "171": "tai_san",
        "211": "tai_san",
        "212": "tai_san",
        "213": "tai_san",
        "214": "tai_san",
        "215": "tai_san",
        "217": "tai_san",
        "221": "tai_san",
        "222": "tai_san",
        "228": "tai_san",
        "229": "tai_san",
        "241": "tai_san",
        "242": "tai_san",
        "243": "tai_san",
        "244": "tai_san",
        "261": "tai_san",
        "311": "no_phai_tra",
        "312": "no_phai_tra",
        "331": "no_phai_tra",
        "333": "no_phai_tra",
        "334": "no_phai_tra",
        "335": "no_phai_tra",
        "336": "no_phai_tra",
        "337": "no_phai_tra",
        "338": "no_phai_tra",
        "332": "no_phai_tra",
        "341": "no_phai_tra",
        "342": "no_phai_tra",
        "343": "no_phai_tra",
        "344": "no_phai_tra",
        "347": "no_phai_tra",
        "349": "no_phai_tra",
        "352": "no_phai_tra",
        "353": "no_phai_tra",
        "356": "no_phai_tra",
        "357": "no_phai_tra",
        "411": "von_chu_so_huu",
        "412": "von_chu_so_huu",
        "413": "von_chu_so_huu",
        "414": "von_chu_so_huu",
        "415": "von_chu_so_huu",
        "418": "von_chu_so_huu",
        "419": "von_chu_so_huu",
        "420": "von_chu_so_huu",
        "421": "von_chu_so_huu",
        "511": "doanh_thu",
        "512": "doanh_thu",
        "515": "doanh_thu",
        "521": "doanh_thu",
        "621": "chi_phi",
        "622": "chi_phi",
        "623": "chi_phi",
        "627": "chi_phi",
        "631": "chi_phi",
        "632": "chi_phi",
        "635": "chi_phi",
        "641": "chi_phi",
        "642": "chi_phi",
        "711": "thu_nhap_khac",
        "811": "chi_phi_khac",
        "821": "chi_phi_khac",
        "911": "xac_dinh_kq",
    }

    def test_all_required_tier1_exist(self, fixture_data):
        """Test all required Tier-1 accounts are present."""
        tier1 = {
            x["fields"]["ma_tai_khoan"]: x
            for x in fixture_data
            if x["fields"]["cap_do"] == 1
        }
        for code, expected_type in self.REQUIRED_TIER1.items():
            assert code in tier1, f"Missing Tier-1 account {code}"
            assert tier1[code]["fields"]["loai_tai_khoan"] == expected_type, (
                f"Account {code} has wrong type: "
                f"{tier1[code]['fields']['loai_tai_khoan']} != {expected_type}"
            )


class TestRequiredTier2Accounts:
    """Test that all required Tier-2 accounts exist with correct parents."""

    REQUIRED_TIER2 = {
        "1281": "128", "1282": "128", "1283": "128", "1288": "128",
        "1331": "133", "1332": "133",
        "1361": "136", "1362": "136", "1363": "136", "1368": "136",
        "1381": "138", "1383": "138", "1388": "138",
        "2141": "214", "2142": "214", "2143": "214", "2147": "214",
        "2151": "215", "2152": "215",
        "2291": "229", "2292": "229", "2293": "229", "2294": "229", "2295": "229",
        "2411": "241", "2412": "241", "2413": "241", "2414": "241",
        "3331": "333", "3332": "333", "3333": "333", "3334": "333",
        "3335": "333", "3336": "333", "3337": "333", "3338": "333", "3339": "333",
        "3381": "338", "3382": "338", "3383": "338", "3384": "338",
        "3385": "338", "3386": "338", "3387": "338", "3388": "338",
        "3411": "341", "3412": "341",
        "3431": "343", "3432": "343",
        "3521": "352", "3522": "352", "3523": "352",
        "3531": "353", "3532": "353",
        "3561": "356", "3562": "356",
        "4111": "411", "4112": "411", "4113": "411", "4118": "411",
        "4211": "421", "4212": "421",
        "5111": "511", "5112": "511", "5113": "511", "5114": "511",
        "5115": "511", "5116": "511", "5117": "511", "5118": "511", "5119": "511",
        "5211": "521", "5212": "521", "5213": "521", "5214": "521",
        "6211": "621",
        "6221": "622",
        "6231": "623", "6232": "623", "6233": "623", "6234": "623",
        "6235": "623", "6236": "623",
        "6271": "627", "6272": "627", "6273": "627", "6274": "627",
        "6275": "627", "6276": "627",
        "6421": "642", "6422": "642", "6423": "642", "6424": "642",
        "6425": "642", "6426": "642", "6427": "642", "6428": "642",
        "8211": "821", "8212": "821",
    }

    def test_all_required_tier2_exist(self, fixture_data):
        """Test all required Tier-2 accounts are present."""
        tier2 = {
            x["fields"]["ma_tai_khoan"]: x
            for x in fixture_data
            if x["fields"]["cap_do"] == 2
        }
        for code, expected_parent in self.REQUIRED_TIER2.items():
            assert code in tier2, f"Missing Tier-2 account {code}"
            assert tier2[code]["fields"]["tai_khoan_me"] == expected_parent, (
                f"Account {code} has wrong parent: "
                f"{tier2[code]['fields']['tai_khoan_me']} != {expected_parent}"
            )


class TestAccountTypeCorrectness:
    """Test account types are correctly assigned."""

    def test_711_is_thu_nhap_khac(self, fixture_data):
        """Test 711 is thu_nhap_khac, not doanh_thu."""
        acc = next(
            x for x in fixture_data
            if x["fields"]["ma_tai_khoan"] == "711"
        )
        assert acc["fields"]["loai_tai_khoan"] == "thu_nhap_khac"

    def test_811_is_chi_phi_khac(self, fixture_data):
        """Test 811 is chi_phi_khac."""
        acc = next(
            x for x in fixture_data
            if x["fields"]["ma_tai_khoan"] == "811"
        )
        assert acc["fields"]["loai_tai_khoan"] == "chi_phi_khac"

    def test_821_is_chi_phi_khac(self, fixture_data):
        """Test 821 is chi_phi_khac."""
        acc = next(
            x for x in fixture_data
            if x["fields"]["ma_tai_khoan"] == "821"
        )
        assert acc["fields"]["loai_tai_khoan"] == "chi_phi_khac"

    def test_911_is_xac_dinh_kq(self, fixture_data):
        """Test 911 is xac_dinh_kq."""
        acc = next(
            x for x in fixture_data
            if x["fields"]["ma_tai_khoan"] == "911"
        )
        assert acc["fields"]["loai_tai_khoan"] == "xac_dinh_kq"

    def test_511_is_doanh_thu(self, fixture_data):
        """Test 511 is doanh_thu."""
        acc = next(
            x for x in fixture_data
            if x["fields"]["ma_tai_khoan"] == "511"
        )
        assert acc["fields"]["loai_tai_khoan"] == "doanh_thu"

    def test_632_is_chi_phi(self, fixture_data):
        """Test 632 (giá vốn) is chi_phi."""
        acc = next(
            x for x in fixture_data
            if x["fields"]["ma_tai_khoan"] == "632"
        )
        assert acc["fields"]["loai_tai_khoan"] == "chi_phi"
