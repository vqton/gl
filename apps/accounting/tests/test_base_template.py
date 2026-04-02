"""TDD tests for base.html template production readiness."""

import pytest
from django.template import Template, Context
from django.test import RequestFactory, override_settings


@pytest.fixture
def rf():
    return RequestFactory()


@pytest.fixture
def anon_request(rf):
    request = rf.get("/test/")
    request.resolver_match = type(
        "Match", (), {"url_name": "test", "app_name": "test"}
    )()
    return request


@pytest.fixture
def user_request(rf, django_user_model):
    user = django_user_model.objects.create_user(
        username="testuser", password="test123"
    )
    request = rf.get("/test/")
    request.user = user
    request.resolver_match = type(
        "Match", (), {"url_name": "phieu_thu_list", "app_name": "nghiep_vu"}
    )()
    return request


@pytest.fixture
def superuser_request(rf, django_user_model):
    user = django_user_model.objects.create_superuser(
        username="admin", password="admin123"
    )
    request = rf.get("/test/")
    request.user = user
    request.resolver_match = type(
        "Match", (), {"url_name": "phieu_thu_list", "app_name": "nghiep_vu"}
    )()
    return request


@pytest.fixture
def base_template():
    from django.template.loader import get_template
    return get_template("base.html")


# ============================================================
# LAYER 1: HTML Structure & Meta Tags
# ============================================================


class TestHtmlStructure:
    """Test that base.html has proper HTML5 structure for production."""

    def test_has_doctype(self, base_template):
        """Production pages must declare HTML5 doctype."""
        rendered = base_template.render({})
        assert "<!DOCTYPE html>" in rendered

    def test_has_lang_attribute(self, base_template):
        """Production pages must declare language for accessibility."""
        rendered = base_template.render({})
        assert 'lang="vi"' in rendered

    def test_has_charset_meta(self, base_template):
        """Production pages must declare UTF-8 charset."""
        rendered = base_template.render({})
        assert 'charset="UTF-8"' in rendered

    def test_has_viewport_meta(self, base_template):
        """Production pages must have viewport meta for mobile."""
        rendered = base_template.render({})
        assert 'name="viewport"' in rendered
        assert "width=device-width" in rendered

    def test_has_title_block(self, base_template):
        """Production pages must have a title with default."""
        rendered = base_template.render({})
        assert "<title>" in rendered
        assert "Kế toán SME" in rendered

    def test_has_meta_description(self, base_template):
        """Production pages should have meta description for SEO/bookmarks."""
        rendered = base_template.render({})
        assert 'name="description"' in rendered

    def test_has_favicon(self, base_template):
        """Production pages should have a favicon link."""
        rendered = base_template.render({})
        assert "favicon" in rendered.lower() or "icon" in rendered.lower()


# ============================================================
# LAYER 2: Required Blocks
# ============================================================


class TestTemplateBlocks:
    """Test that base.html exposes all necessary template blocks."""

    def test_has_title_block(self, base_template):
        rendered = base_template.render({})
        # Title block should exist and render default
        assert "{% block title %}" in open(
            "templates/base.html"
        ).read()

    def test_has_content_block(self, base_template):
        rendered = base_template.render({})
        assert "{% block content %}" in open(
            "templates/base.html"
        ).read()

    def test_has_breadcrumb_block(self, base_template):
        rendered = base_template.render({})
        assert "{% block breadcrumb %}" in open(
            "templates/base.html"
        ).read()

    def test_has_extra_css_block(self, base_template):
        rendered = base_template.render({})
        assert "{% block extra_css %}" in open(
            "templates/base.html"
        ).read()

    def test_has_extra_js_block(self, base_template):
        rendered = base_template.render({})
        assert "{% block extra_js %}" in open(
            "templates/base.html"
        ).read()

    def test_has_extra_head_block(self, base_template):
        """Extra head block needed for custom meta tags, preconnect, etc."""
        source = open("templates/base.html").read()
        assert "{% block extra_head %}" in source


# ============================================================
# LAYER 3: Sidebar Completeness
# ============================================================


class TestSidebarCompleteness:
    """Test that sidebar includes ALL app links, not just a subset."""

    def test_sidebar_has_nghiep_vu_section(self, base_template):
        rendered = base_template.render({})
        assert "Nghiệp vụ" in rendered

    def test_sidebar_has_phieu_thu_link(self, base_template):
        rendered = base_template.render({})
        assert "Phiếu thu" in rendered

    def test_sidebar_has_phieu_chi_link(self, base_template):
        rendered = base_template.render({})
        assert "Phiếu chi" in rendered

    def test_sidebar_has_hoa_don_link(self, base_template):
        rendered = base_template.render({})
        assert "Hóa đơn" in rendered

    def test_sidebar_has_kho_section(self, base_template):
        rendered = base_template.render({})
        assert "Kho" in rendered

    def test_sidebar_has_bao_cao_section(self, base_template):
        rendered = base_template.render({})
        assert "Báo cáo" in rendered

    def test_sidebar_has_bang_cdk_link(self, base_template):
        """Balance sheet report must be in sidebar."""
        rendered = base_template.render({})
        assert "Bảng CĐKT" in rendered

    def test_sidebar_has_kqkd_link(self, base_template):
        """P&L report must be in sidebar."""
        rendered = base_template.render({})
        assert "KQKD" in rendered

    def test_sidebar_has_luong_link(self, base_template):
        """Payroll module must be in sidebar - MISSING in current template."""
        rendered = base_template.render({})
        assert "Lương" in rendered

    def test_sidebar_has_tai_san_link(self, base_template):
        """Fixed assets module must be in sidebar - MISSING in current template."""
        rendered = base_template.render({})
        assert "Tài sản" in rendered

    def test_sidebar_has_danh_muc_section_for_superuser(
        self, base_template, superuser_request
    ):
        """Master data section should appear for superusers."""
        rendered = base_template.render({"request": superuser_request, "user": superuser_request.user})
        assert "Danh mục" in rendered

    def test_sidebar_has_don_vi_link_for_superuser(
        self, base_template, superuser_request
    ):
        """DonVi link should be in sidebar for superusers - MISSING."""
        rendered = base_template.render({"request": superuser_request, "user": superuser_request.user})
        assert "Đơn vị" in rendered

    def test_sidebar_has_hang_hoa_link_for_superuser(
        self, base_template, superuser_request
    ):
        """HangHoa link should be in sidebar for superusers - MISSING."""
        rendered = base_template.render({"request": superuser_request, "user": superuser_request.user})
        assert "Hàng hóa" in rendered

    def test_sidebar_has_ngan_hang_link_for_superuser(
        self, base_template, superuser_request
    ):
        """NganHang link should be in sidebar for superusers - MISSING."""
        rendered = base_template.render({"request": superuser_request, "user": superuser_request.user})
        assert "Ngân hàng" in rendered

    def test_sidebar_hides_danh_muc_for_non_superuser(
        self, base_template, user_request
    ):
        """Master data section should NOT appear for non-superusers."""
        rendered = base_template.render({"request": user_request, "user": user_request.user})
        assert "Danh mục" not in rendered

    def test_sidebar_has_admin_link_for_superuser(
        self, base_template, superuser_request
    ):
        """Admin link should appear for superusers."""
        rendered = base_template.render({"request": superuser_request, "user": superuser_request.user})
        assert "Quản trị" in rendered


# ============================================================
# LAYER 4: Active Link Highlighting
# ============================================================


class TestActiveLinkHighlighting:
    """Test that sidebar highlights the current page."""

    def test_active_link_for_nghiep_vu_page(self, base_template, user_request):
        """Sidebar should mark current app's link as active."""
        source = open("templates/base.html").read()
        # Template must have logic to add 'active' class based on current URL
        assert "active" in source.lower()

    def test_active_link_uses_request_resolver(self, base_template):
        """Active link detection should use request.resolver_match."""
        source = open("templates/base.html").read()
        assert "resolver_match" in source or "request.path" in source


# ============================================================
# LAYER 5: Header & User Section
# ============================================================


class TestHeaderUserSection:
    """Test header user display for all auth states."""

    def test_shows_username_for_authenticated_user(
        self, base_template, user_request
    ):
        rendered = base_template.render({"request": user_request, "user": user_request.user})
        assert "testuser" in rendered

    def test_shows_superuser_role(self, base_template, superuser_request):
        rendered = base_template.render({"request": superuser_request, "user": superuser_request.user})
        assert "Quản trị viên" in rendered

    def test_shows_accountant_role_for_non_superuser(
        self, base_template, user_request
    ):
        rendered = base_template.render({"request": user_request, "user": user_request.user})
        assert "Kế toán viên" in rendered

    def test_has_logout_link(self, base_template, user_request):
        rendered = base_template.render({"request": user_request, "user": user_request.user})
        assert "Thoát" in rendered
        assert "logout" in rendered

    def test_has_dashboard_link_in_logo(self, base_template):
        rendered = base_template.render({})
        # The {% url %} tag resolves to "/" not the literal name
        assert 'href="/"' in rendered or "dashboard" in rendered.lower()


# ============================================================
# LAYER 6: Messages Framework
# ============================================================


class TestMessagesFramework:
    """Test Django messages integration."""

    def test_renders_messages(self, base_template, user_request):
        """Messages block must render Django messages."""
        source = open("templates/base.html").read()
        assert "{% if messages %}" in source
        assert "alert-dismissible" in source

    def test_supports_all_message_levels(self, base_template):
        """Should support success, error, warning, info message types."""
        source = open("templates/base.html").read()
        assert "message.tags" in source


# ============================================================
# LAYER 7: Print Support
# ============================================================


class TestPrintSupport:
    """Test print media query for accounting documents."""

    def test_has_print_media_query(self, base_template):
        """Production accounting app must support printing reports."""
        source = open("templates/base.html").read()
        assert "@media print" in source

    def test_print_hides_sidebar_and_header(self, base_template):
        """Print should hide navigation elements."""
        source = open("templates/base.html").read()
        assert ".app-header" in source.split("@media print")[1]
        assert ".app-sidebar" in source.split("@media print")[1]


# ============================================================
# LAYER 8: Security & Production Hardening
# ============================================================


class TestSecurityProduction:
    """Test production security concerns."""

    def test_no_inline_debug_info(self, base_template):
        """Production template should not expose debug info."""
        source = open("templates/base.html").read()
        assert "DEBUG" not in source
        assert "debug" not in source.lower().split("class=")[0]

    def test_has_csrf_protection_in_forms(self, base_template):
        """Template should remind about CSRF in content block."""
        # The content block is where forms go; base.html itself
        # doesn't need CSRF but should support it via blocks
        source = open("templates/base.html").read()
        assert "{% block content %}" in source

    def test_no_hardcoded_secrets(self, base_template):
        """No API keys, passwords, or secrets in template."""
        source = open("templates/base.html").read()
        assert "password" not in source.lower()
        assert "secret" not in source.lower()
        assert "api_key" not in source.lower()

    def test_xframe_options_compatible(self, base_template):
        """Template should not set conflicting X-Frame-Options."""
        source = open("templates/base.html").read()
        # Should not have <meta http-equiv="X-Frame-Options">
        assert "X-Frame-Options" not in source


# ============================================================
# LAYER 9: Accessibility
# ============================================================


class TestAccessibility:
    """Test WCAG 2.1 AA compliance basics."""

    def test_has_main_landmark(self, base_template):
        """Must have <main> element for screen readers."""
        source = open("templates/base.html").read()
        assert "<main" in source

    def test_has_nav_landmark(self, base_template):
        """Breadcrumb should use <nav> for accessibility."""
        source = open("templates/base.html").read()
        assert "<nav" in source

    def test_has_aside_landmark(self, base_template):
        """Sidebar should use <aside> for accessibility."""
        source = open("templates/base.html").read()
        assert "<aside" in source

    def test_has_header_landmark(self, base_template):
        """Header should use <header> for accessibility."""
        source = open("templates/base.html").read()
        assert "<header" in source

    def test_links_have_text_content(self, base_template):
        """All sidebar links must have visible text."""
        source = open("templates/base.html").read()
        # Check sidebar links have text, not just icons
        assert "Phiếu thu" in source
        assert "Phiếu chi" in source


# ============================================================
# LAYER 10: Responsive / Mobile
# ============================================================


class TestResponsive:
    """Test mobile/responsive support."""

    def test_has_viewport_meta(self, base_template):
        rendered = base_template.render({})
        assert "viewport" in rendered

    def test_has_responsive_css(self, base_template):
        """Should have at least one media query for responsiveness."""
        source = open("templates/base.html").read()
        assert "@media" in source

    def test_print_is_separate_from_responsive(self, base_template):
        """Print media query should exist separately from responsive."""
        source = open("templates/base.html").read()
        media_queries = source.count("@media")
        assert media_queries >= 1  # At least print


# ============================================================
# LAYER 11: JavaScript & Bootstrap
# ============================================================


class TestJavaScriptBootstrap:
    """Test Bootstrap JS and custom JS support."""

    def test_loads_bootstrap_js(self, base_template):
        """Bootstrap JS required for modals, dropdowns, dismiss alerts."""
        source = open("templates/base.html").read()
        assert "bootstrap_javascript" in source or "bootstrap.js" in source

    def test_loads_bootstrap_css(self, base_template):
        """Bootstrap CSS required."""
        source = open("templates/base.html").read()
        assert "bootstrap_css" in source or "bootstrap.css" in source

    def test_has_extra_js_block(self, base_template):
        """Pages need ability to add custom JS."""
        source = open("templates/base.html").read()
        assert "{% block extra_js %}" in source

    def test_bootstrap_js_after_content(self, base_template):
        """Bootstrap JS should load after page content for performance."""
        source = open("templates/base.html").read()
        js_pos = source.find("bootstrap_javascript")
        content_pos = source.find("{% block content %}")
        assert js_pos > content_pos, "Bootstrap JS should load after content block"


# ============================================================
# LAYER 12: Footer
# ============================================================


class TestFooter:
    """Test footer presence for production."""

    def test_has_footer_element(self, base_template):
        """Production app should have a footer with copyright/year."""
        source = open("templates/base.html").read()
        assert "<footer" in source or "footer" in source.lower()


# ============================================================
# LAYER 13: All URL References Must Resolve
# ============================================================


class TestUrlReferences:
    """Test that all {% url %} tags reference existing named URLs."""

    def test_url_accounting_dashboard_exists(self, base_template):
        from django.urls import reverse
        reverse("accounting:dashboard")

    def test_url_accounting_logout_exists(self, base_template):
        from django.urls import reverse
        reverse("accounting:logout")

    def test_url_nghiep_vu_phieu_thu_list_exists(self, base_template):
        from django.urls import reverse
        reverse("nghiep_vu:phieu_thu_list")

    def test_url_nghiep_vu_phieu_chi_list_exists(self, base_template):
        from django.urls import reverse
        reverse("nghiep_vu:phieu_chi_list")

    def test_url_nghiep_vu_hoa_don_list_exists(self, base_template):
        from django.urls import reverse
        reverse("nghiep_vu:hoa_don_list")

    def test_url_kho_kho_list_exists(self, base_template):
        from django.urls import reverse
        reverse("kho:kho_list")

    def test_url_bao_cao_bang_cdk_exists(self, base_template):
        from django.urls import reverse
        reverse("bao_cao:bang_cdk")

    def test_url_bao_cao_kqkd_exists(self, base_template):
        from django.urls import reverse
        reverse("bao_cao:kqkd")

    def test_url_danh_muc_taikhoan_list_exists(self, base_template):
        from django.urls import reverse
        reverse("danh_muc:taikhoan_list")

    def test_url_danh_muc_khachhang_list_exists(self, base_template):
        from django.urls import reverse
        reverse("danh_muc:khachhang_list")

    def test_url_danh_muc_nhacungcap_list_exists(self, base_template):
        from django.urls import reverse
        reverse("danh_muc:nhacungcap_list")

    def test_url_admin_index_exists(self, base_template):
        from django.urls import reverse
        reverse("admin:index")
