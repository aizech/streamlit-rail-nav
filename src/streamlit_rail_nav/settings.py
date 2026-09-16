"""Rail-nav settings schema and normalization helpers.

The settings schema is a plain dict so it round-trips cleanly with JSON
config files. ``normalize_settings()`` merges a raw (possibly partial or
malformed) dict over :data:`DEFAULT_RAIL_SETTINGS`, validating colors,
clamping sizes, and cleaning the item list.

Item kinds and their fields:

- ``link``: ``label``, ``icon``, ``page``, optional ``access``
- ``badge_link``: same as ``link`` plus ``badge``
- ``separator``: no fields
- ``spacer``: ``spacer_px``
- ``header``: ``label``
- ``theme_toggle``: ``label``, ``icon``
- ``search``: ``label`` (used as placeholder), ``icon``
- ``upgrade_card``: ``title``, ``text``, ``button_label``
- ``user_profile``: ``name``, ``subtitle``, ``avatar_url``, ``avatar_initials``

The ``access`` field (``public``/``logged_in``/``admin``) is normalized and
preserved but never evaluated by this package — filter items caller-side
before passing the config to ``render()``.
"""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

_HEX_COLOR_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")

ALLOWED_ACCESS_LEVELS = {"public", "logged_in", "admin"}

ITEM_KINDS = {
    "link",
    "separator",
    "spacer",
    "theme_toggle",
    "search",
    "badge_link",
    "header",
    "upgrade_card",
    "user_profile",
}

DEFAULT_RAIL_SETTINGS: dict[str, Any] = {
    "sidebar_bg": "#313841",
    "sidebar_text_color": "#EEEEEE",
    "sidebar_icon_color": "#EEEEEE",
    "sidebar_hover_bg": "#3A4750",
    "sidebar_hover_text_color": "#EEEEEE",
    "sidebar_active_bg": "#EA9216",
    "sidebar_focus_outline": "#EA9216",
    "sidebar_separator_color": "#3A4750",
    "sidebar_separator_color_light": "#3A4750",
    "sidebar_separator_color_dark": "#3A4750",
    "theme_mode": "dark",
    "logo_src": "",
    "logo_src_light": "",
    "logo_src_dark": "",
    "icon_src_light": "",
    "icon_src_dark": "",
    "logo_height_px": 44,
    "logo_render_height_px": 36,
    "icon_render_height_px": 36,
    "sidebar_font_size_px": 14,
    "sidebar_icon_size_px": 20,
    "sidebar_collapsed_width_px": 68,
    "sidebar_hover_width_px": 260,
    "sidebar_item_gap_px": 4,
    "sidebar_transition": "0.2s",
    "items": [],
}

_DEFAULT_ITEMS: list[dict[str, Any]] | None = None
_DEFAULT_SETTINGS: dict[str, Any] | None = None


def _valid_hex(value: Any) -> bool:
    return isinstance(value, str) and bool(_HEX_COLOR_RE.match(value.strip()))


def _as_int(value: Any, *, default: int, minimum: int, maximum: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return max(minimum, min(maximum, parsed))


def _normalize_item_kind(value: Any) -> str:
    item_kind = str(value or "link").strip().lower()
    if item_kind in ITEM_KINDS:
        return item_kind
    return "link"


def _normalize_access_level(value: Any) -> str:
    access_level = str(value or "public").strip().lower()
    if access_level in ALLOWED_ACCESS_LEVELS:
        return access_level
    return "public"


def _get_default_items() -> list[dict[str, Any]]:
    global _DEFAULT_ITEMS
    if _DEFAULT_ITEMS is None:
        _DEFAULT_ITEMS = deepcopy(DEFAULT_RAIL_SETTINGS["items"])
    return _DEFAULT_ITEMS


def _get_default_settings() -> dict[str, Any]:
    global _DEFAULT_SETTINGS
    if _DEFAULT_SETTINGS is None:
        _DEFAULT_SETTINGS = deepcopy(DEFAULT_RAIL_SETTINGS)
    return _DEFAULT_SETTINGS


def _normalize_items(value: Any) -> list[dict[str, Any]]:
    defaults = deepcopy(_get_default_items())
    if not isinstance(value, list):
        return defaults
    cleaned: list[dict[str, Any]] = []
    for raw in value:
        if not isinstance(raw, dict):
            continue
        item_kind = _normalize_item_kind(raw.get("kind"))
        if item_kind == "separator":
            cleaned.append({"kind": "separator"})
            continue
        if item_kind == "spacer":
            cleaned.append(
                {
                    "kind": "spacer",
                    "spacer_px": _as_int(
                        raw.get("spacer_px"),
                        default=16,
                        minimum=4,
                        maximum=250,
                    ),
                }
            )
            continue
        if item_kind == "theme_toggle":
            cleaned.append(
                {
                    "kind": "theme_toggle",
                    "label": str(raw.get("label") or "Dark mode").strip(),
                    "icon": str(raw.get("icon") or "dark_mode").strip(),
                }
            )
            continue
        if item_kind == "search":
            cleaned.append(
                {
                    "kind": "search",
                    "label": str(raw.get("label") or "Quick search").strip(),
                    "icon": str(raw.get("icon") or "search").strip(),
                }
            )
            continue
        if item_kind == "header":
            cleaned.append(
                {
                    "kind": "header",
                    "label": str(raw.get("label") or "").strip(),
                }
            )
            continue
        if item_kind == "upgrade_card":
            cleaned.append(
                {
                    "kind": "upgrade_card",
                    "title": str(raw.get("title") or "").strip(),
                    "text": str(raw.get("text") or "").strip(),
                    "button_label": str(raw.get("button_label") or "").strip(),
                }
            )
            continue
        if item_kind == "user_profile":
            cleaned.append(
                {
                    "kind": "user_profile",
                    "name": str(raw.get("name") or "").strip(),
                    "subtitle": str(raw.get("subtitle") or "").strip(),
                    "avatar_url": str(raw.get("avatar_url") or "").strip(),
                    "avatar_initials": str(raw.get("avatar_initials") or "").strip(),
                }
            )
            continue

        label = str(raw.get("label") or "").strip()
        icon = str(raw.get("icon") or "").strip()
        page = str(raw.get("page") or "").strip()
        if not label or not page:
            continue

        item = {
            "kind": item_kind,
            "label": label,
            "icon": icon,
            "page": page,
            "access": _normalize_access_level(raw.get("access")),
        }
        if item_kind == "badge_link":
            item["badge"] = str(raw.get("badge") or "").strip()

        cleaned.append(item)

    return cleaned or defaults


def normalize_settings(raw: Any) -> dict[str, Any]:
    defaults = deepcopy(_get_default_settings())
    if not isinstance(raw, dict):
        return defaults

    preset_name = raw.get("theme_preset_name")
    if isinstance(preset_name, str):
        defaults["theme_preset_name"] = preset_name.strip()

    theme_mode = str(raw.get("theme_mode") or "").strip().lower()
    if theme_mode in {"light", "dark"}:
        defaults["theme_mode"] = theme_mode

    for key in (
        "theme_preset_light",
        "theme_preset_dark",
        "logo_src",
        "logo_src_light",
        "logo_src_dark",
        "icon_src_light",
        "icon_src_dark",
    ):
        value = raw.get(key)
        if isinstance(value, str):
            defaults[key] = value.strip()

    for key in (
        "sidebar_bg",
        "sidebar_text_color",
        "sidebar_icon_color",
        "sidebar_hover_bg",
        "sidebar_hover_text_color",
        "sidebar_active_bg",
        "sidebar_focus_outline",
        "sidebar_separator_color",
        "sidebar_separator_color_light",
        "sidebar_separator_color_dark",
    ):
        value = raw.get(key)
        if _valid_hex(value):
            defaults[key] = str(value).strip()

    if not defaults.get("sidebar_separator_color_light"):
        defaults["sidebar_separator_color_light"] = defaults["sidebar_separator_color"]
    if not defaults.get("sidebar_separator_color_dark"):
        defaults["sidebar_separator_color_dark"] = defaults["sidebar_separator_color"]

    defaults["sidebar_font_size_px"] = _as_int(
        raw.get("sidebar_font_size_px"),
        default=int(DEFAULT_RAIL_SETTINGS["sidebar_font_size_px"]),
        minimum=12,
        maximum=24,
    )
    defaults["sidebar_icon_size_px"] = _as_int(
        raw.get("sidebar_icon_size_px"),
        default=int(DEFAULT_RAIL_SETTINGS["sidebar_icon_size_px"]),
        minimum=16,
        maximum=32,
    )
    defaults["sidebar_collapsed_width_px"] = _as_int(
        raw.get("sidebar_collapsed_width_px"),
        default=int(DEFAULT_RAIL_SETTINGS["sidebar_collapsed_width_px"]),
        minimum=56,
        maximum=120,
    )
    defaults["sidebar_hover_width_px"] = _as_int(
        raw.get("sidebar_hover_width_px"),
        default=int(DEFAULT_RAIL_SETTINGS["sidebar_hover_width_px"]),
        minimum=180,
        maximum=360,
    )
    defaults["sidebar_item_gap_px"] = _as_int(
        raw.get("sidebar_item_gap_px"),
        default=int(DEFAULT_RAIL_SETTINGS["sidebar_item_gap_px"]),
        minimum=0,
        maximum=32,
    )
    defaults["logo_height_px"] = _as_int(
        raw.get("logo_height_px"),
        default=int(DEFAULT_RAIL_SETTINGS["logo_height_px"]),
        minimum=24,
        maximum=128,
    )
    defaults["logo_render_height_px"] = _as_int(
        raw.get("logo_render_height_px"),
        default=int(DEFAULT_RAIL_SETTINGS["logo_render_height_px"]),
        minimum=20,
        maximum=96,
    )
    defaults["icon_render_height_px"] = _as_int(
        raw.get("icon_render_height_px"),
        default=int(DEFAULT_RAIL_SETTINGS["icon_render_height_px"]),
        minimum=16,
        maximum=64,
    )

    transition = str(raw.get("sidebar_transition") or "").strip()
    if transition:
        defaults["sidebar_transition"] = transition

    defaults["items"] = _normalize_items(raw.get("items"))
    return defaults
