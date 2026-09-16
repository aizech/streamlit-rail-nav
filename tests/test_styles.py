from __future__ import annotations

from streamlit_rail_nav import normalize_settings
from streamlit_rail_nav.styles import (
    build_badge_css,
    build_brand_icon_css,
    build_rail_css,
)


def _css(raw: dict | None = None) -> str:
    return build_rail_css(normalize_settings(raw or {}))


def test_rail_css_defines_srn_custom_properties() -> None:
    css = _css()

    for var in (
        "--srn-bg",
        "--srn-text",
        "--srn-icon",
        "--srn-hover-bg",
        "--srn-hover-text",
        "--srn-active-bg",
        "--srn-focus-outline",
        "--srn-separator-color",
        "--srn-font-size",
        "--srn-icon-size",
        "--srn-collapsed-width",
        "--srn-hover-width",
        "--srn-item-gap",
        "--srn-transition",
    ):
        assert var in css


def test_rail_css_uses_configured_values() -> None:
    css = _css(
        {
            "sidebar_bg": "#112233",
            "sidebar_collapsed_width_px": 80,
            "sidebar_hover_width_px": 300,
        }
    )

    assert "--srn-bg: #112233" in css
    assert "--srn-collapsed-width: 80px" in css
    assert "--srn-hover-width: 300px" in css


def test_rail_css_scopes_rules_to_sidebar() -> None:
    css = _css()

    assert "section[data-testid='stSidebar']:not(:hover)" in css
    assert "section[data-testid='stSidebar']:hover" in css
    assert "section[data-testid='stSidebar'] [data-testid='stPageLink']" in css


def test_rail_css_has_custom_component_classes() -> None:
    css = _css()

    for cls in (
        ".srn-menu-separator",
        ".srn-menu-header",
        ".srn-user-profile",
        ".srn-avatar",
        ".srn-upgrade-card",
        ".srn-badge",
    ):
        assert cls in css


def test_rail_css_hides_labels_in_rail_mode() -> None:
    css = _css()

    assert "not(:hover) [data-testid='stPageLink'] a p" in css
    assert "not(:hover) .srn-user-info" in css
    assert "not(:hover) .srn-menu-header" in css


def test_badge_css_uses_nth_of_type() -> None:
    css = build_badge_css(3, "New")

    assert "nth-of-type(3)" in css
    assert "content: 'New'" in css
    assert "[data-testid='stPageLink'] a::after" in css


def test_badge_css_escapes_quotes() -> None:
    css = build_badge_css(1, "it's")

    assert "it\\'s" in css


def test_brand_icon_css() -> None:
    css = build_brand_icon_css("data:image/png;base64,AAA", 36)

    assert "background-image:url('data:image/png;base64,AAA')" in css
    assert "height:36px" in css
    assert "flex:0 0 36px" in css
