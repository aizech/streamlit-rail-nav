from __future__ import annotations

from streamlit_rail_nav import DEFAULT_RAIL_SETTINGS, normalize_settings


def test_normalize_keeps_custom_item_order_and_kinds() -> None:
    raw = {
        "items": [
            {
                "kind": "link",
                "label": "Help",
                "icon": "help",
                "page": "pages/Help.py",
                "access": "public",
            },
            {"kind": "separator"},
            {"kind": "spacer", "spacer_px": 24},
            {
                "kind": "link",
                "label": "Home",
                "icon": "home",
                "page": "app.py",
                "access": "logged_in",
            },
        ]
    }

    normalized = normalize_settings(raw)

    assert normalized["items"] == [
        {
            "kind": "link",
            "label": "Help",
            "icon": "help",
            "page": "pages/Help.py",
            "access": "public",
        },
        {"kind": "separator"},
        {"kind": "spacer", "spacer_px": 24},
        {
            "kind": "link",
            "label": "Home",
            "icon": "home",
            "page": "app.py",
            "access": "logged_in",
        },
    ]


def test_normalize_defaults_invalid_access_to_public() -> None:
    raw = {
        "items": [
            {
                "kind": "link",
                "label": "Dashboard",
                "icon": "dashboard",
                "page": "pages/Dashboard.py",
                "access": "superuser",
            }
        ]
    }

    normalized = normalize_settings(raw)

    assert normalized["items"][0]["access"] == "public"


def test_normalize_clamps_spacer_and_gap_values() -> None:
    raw = {
        "sidebar_item_gap_px": 99,
        "items": [{"kind": "spacer", "spacer_px": -50}],
    }

    normalized = normalize_settings(raw)

    assert normalized["sidebar_item_gap_px"] == 32
    assert normalized["items"] == [{"kind": "spacer", "spacer_px": 4}]


def test_normalize_accepts_separator_color() -> None:
    raw = {"sidebar_separator_color": "#123ABC"}

    normalized = normalize_settings(raw)

    assert normalized["sidebar_separator_color"] == "#123ABC"


def test_normalize_rejects_invalid_hex_colors() -> None:
    raw = {"sidebar_bg": "not-a-color", "sidebar_hover_bg": "#FFF"}

    normalized = normalize_settings(raw)

    assert normalized["sidebar_bg"] == DEFAULT_RAIL_SETTINGS["sidebar_bg"]
    assert normalized["sidebar_hover_bg"] == "#FFF"


def test_normalize_accepts_theme_and_branding_fields() -> None:
    raw = {
        "theme_mode": "light",
        "theme_preset_light": "Black & White (Light)",
        "theme_preset_dark": "Black & White (Dark)",
        "theme_preset_name": "Black & White (Light)",
        "logo_src_light": "assets/logo_light.png",
        "logo_src_dark": "assets/logo_dark.png",
        "icon_src_light": "assets/icon_light.png",
        "icon_src_dark": "assets/icon_dark.png",
        "logo_height_px": 80,
        "logo_render_height_px": 48,
        "icon_render_height_px": 28,
        "sidebar_hover_text_color": "#101010",
        "sidebar_separator_color_light": "#AAAAAA",
        "sidebar_separator_color_dark": "#222222",
    }

    normalized = normalize_settings(raw)

    assert normalized["theme_mode"] == "light"
    assert normalized["theme_preset_name"] == "Black & White (Light)"
    assert normalized["logo_src_light"] == "assets/logo_light.png"
    assert normalized["icon_src_dark"] == "assets/icon_dark.png"
    assert normalized["logo_height_px"] == 80
    assert normalized["logo_render_height_px"] == 48
    assert normalized["icon_render_height_px"] == 28
    assert normalized["sidebar_hover_text_color"] == "#101010"
    assert normalized["sidebar_separator_color_light"] == "#AAAAAA"
    assert normalized["sidebar_separator_color_dark"] == "#222222"


def test_normalize_keeps_extended_item_fields() -> None:
    raw = {
        "items": [
            {"kind": "header", "label": "Section"},
            {"kind": "theme_toggle", "label": "Theme", "icon": "contrast"},
            {"kind": "search", "label": "Find", "icon": "search"},
            {
                "kind": "upgrade_card",
                "title": "Go Pro",
                "text": "Unlock everything",
                "button_label": "Upgrade",
            },
            {
                "kind": "user_profile",
                "name": "Ada Lovelace",
                "subtitle": "Pro trial",
                "avatar_url": "https://example.com/a.png",
                "avatar_initials": "AL",
            },
            {
                "kind": "badge_link",
                "label": "Beta",
                "icon": "science",
                "page": "pages/Beta.py",
                "badge": "New",
            },
        ]
    }

    normalized = normalize_settings(raw)

    assert normalized["items"] == [
        {"kind": "header", "label": "Section"},
        {"kind": "theme_toggle", "label": "Theme", "icon": "contrast"},
        {"kind": "search", "label": "Find", "icon": "search"},
        {
            "kind": "upgrade_card",
            "title": "Go Pro",
            "text": "Unlock everything",
            "button_label": "Upgrade",
        },
        {
            "kind": "user_profile",
            "name": "Ada Lovelace",
            "subtitle": "Pro trial",
            "avatar_url": "https://example.com/a.png",
            "avatar_initials": "AL",
        },
        {
            "kind": "badge_link",
            "label": "Beta",
            "icon": "science",
            "page": "pages/Beta.py",
            "access": "public",
            "badge": "New",
        },
    ]


def test_normalize_does_not_auto_append_items() -> None:
    normalized = normalize_settings({"items": [{"kind": "separator"}]})

    assert normalized["items"] == [{"kind": "separator"}]


def test_normalize_non_dict_returns_defaults() -> None:
    for raw in (None, "x", 42, [1, 2]):
        normalized = normalize_settings(raw)
        assert normalized["items"] == []
        assert normalized["sidebar_bg"] == DEFAULT_RAIL_SETTINGS["sidebar_bg"]


def test_normalize_drops_links_missing_label_or_page() -> None:
    raw = {
        "items": [
            {"kind": "link", "label": "No page", "icon": "home"},
            {"kind": "link", "page": "app.py"},
            {"kind": "link", "label": "Ok", "page": "app.py"},
        ]
    }

    normalized = normalize_settings(raw)

    assert normalized["items"] == [
        {
            "kind": "link",
            "label": "Ok",
            "icon": "",
            "page": "app.py",
            "access": "public",
        }
    ]


def test_normalize_is_idempotent() -> None:
    raw = {
        "sidebar_bg": "#111111",
        "items": [{"kind": "header", "label": "X"}, {"kind": "separator"}],
    }

    once = normalize_settings(raw)
    twice = normalize_settings(once)

    assert once == twice
