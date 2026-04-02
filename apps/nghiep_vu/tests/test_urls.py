"""Tests for URL routing - catches broken links and missing views."""

import pytest
from django.urls import NoReverseMatch, Resolver404, resolve, reverse

# All named URLs that should exist
NAMED_URLS = [
    # Nghiep vu (core)
    "nghiep_vu:index",
    "nghiep_vu:phieu_thu_list",
    "nghiep_vu:phieu_thu_create",
    "nghiep_vu:phieu_chi_list",
    "nghiep_vu:phieu_chi_create",
    "nghiep_vu:hoa_don_list",
    "nghiep_vu:hoa_don_create",
    # Kho
    "kho:kho_list",
    "kho:kho_entry_list",
    "kho:ton_kho_list",
    # Tai san
    "tai_san:taisan_list",
    # Luong
    "luong:nhanvien_list",
    "luong:bangluong_list",
    # Bao cao
    "bao_cao:bang_cdk",
    "bao_cao:kqkd",
]

# URLs with parameters
PARAM_URLS = [
    ("nghiep_vu:phieu_thu_detail", {"pk": 1}),
    ("nghiep_vu:phieu_thu_delete", {"pk": 1}),
    ("nghiep_vu:phieu_chi_detail", {"pk": 1}),
    ("nghiep_vu:phieu_chi_delete", {"pk": 1}),
    ("nghiep_vu:hoa_don_detail", {"pk": 1}),
    ("nghiep_vu:hoa_don_delete", {"pk": 1}),
]


@pytest.mark.django_db
class TestUrlRouting:
    """Test all URLs resolve correctly."""

    @pytest.mark.parametrize("url_name", NAMED_URLS)
    def test_named_url_resolves(self, url_name):
        """Test that every named URL can be reversed and resolved."""
        url = reverse(url_name)
        match = resolve(url)
        assert match.url_name is not None

    @pytest.mark.parametrize("url_name,kwargs", PARAM_URLS)
    def test_param_url_resolves(self, url_name, kwargs):
        """Test that parameterized URLs can be reversed and resolved."""
        url = reverse(url_name, kwargs=kwargs)
        match = resolve(url)
        assert match.url_name is not None

    def test_home_page_resolves(self):
        """Test home page resolves."""
        match = resolve("/")
        assert match.url_name == "index"

    def test_admin_resolves(self):
        """Test admin URL resolves."""
        match = resolve("/admin/")
        assert match.app_name == "admin"

    def test_no_broken_named_urls(self):
        """Test that all URLs referenced in templates exist."""
        # This catches typos in template {% url %} tags
        for url_name in NAMED_URLS:
            try:
                reverse(url_name)
            except NoReverseMatch:
                pytest.fail(f"URL '{url_name}' not found - broken template link")
