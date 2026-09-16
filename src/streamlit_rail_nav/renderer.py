"""Renderer for the rail navigation sidebar.

``render()`` restyles Streamlit's native sidebar into a collapsible icon rail
and renders the configured items as native sidebar widgets. All CSS is injected
through main-area ``st.markdown`` calls, so every ``st.sidebar.*`` emission
maps to exactly one sidebar element container — the renderer counts them to
position per-item CSS (badges) via ``nth-of-type`` selectors.

If you render other widgets into ``st.sidebar`` before calling ``render()``,
badge positions may shift. Call ``render()`` before adding other sidebar
content.
"""

from __future__ import annotations

import html
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

import streamlit as st

from streamlit_rail_nav.assets import src_to_css_url
from streamlit_rail_nav.settings import normalize_settings
from streamlit_rail_nav.styles import (
    BRAND_CSS,
    build_badge_css,
    build_brand_icon_css,
    build_brand_logo_css,
    build_rail_css,
)


def _pick_brand_sources(cfg: Mapping[str, Any]) -> tuple[str, str]:
    """Pick logo/icon variants based on sidebar background brightness."""
    sidebar_bg = str(cfg.get("sidebar_bg") or "").strip()
    bg_hex = sidebar_bg.lstrip("#").lower()
    luminance_hint = int(bg_hex[:2], 16) if len(bg_hex) >= 2 else 255
    use_dark_assets = luminance_hint < 128
    logo_key = "logo_src_dark" if use_dark_assets else "logo_src_light"
    icon_key = "icon_src_dark" if use_dark_assets else "icon_src_light"
    logo_src = (
        str(cfg.get(logo_key) or "").strip() or str(cfg.get("logo_src") or "").strip()
    )
    icon_src = str(cfg.get(icon_key) or "").strip()
    return logo_src, icon_src


def _initials(name: str) -> str:
    words = [w for w in name.split() if w]
    if not words:
        return ""
    return "".join(word[0].upper() for word in words[:2])


def _icon_token(icon: str) -> str | None:
    icon = icon.strip()
    if not icon:
        return None
    if icon.startswith(":"):
        return icon
    return f":material/{icon}:"


def render(
    config: Mapping[str, Any] | None = None,
    *,
    base_path: str | Path | None = None,
    on_theme_toggle: Callable[[], None] | None = None,
    on_search: Callable[[str], None] | None = None,
    on_upgrade_click: Callable[[], None] | None = None,
    footer: str | None = None,
) -> None:
    """Render the rail navigation into ``st.sidebar``.

    Args:
        config: Settings dict matching the ``normalize_settings`` schema.
            Raw/partial dicts are merged over ``DEFAULT_RAIL_SETTINGS``.
        base_path: Directory used to resolve relative ``logo_src``/``icon_src``
            paths. Pass ``Path(__file__).parent`` of your entrypoint.
        on_theme_toggle: Called when a ``theme_toggle`` item is clicked.
        on_search: Called with the query string when a ``search`` item changes.
        on_upgrade_click: Called when an ``upgrade_card`` button is clicked.
        footer: Optional caption rendered at the bottom of the sidebar.
    """
    cfg = normalize_settings(config)

    css_parts: list[str] = [build_rail_css(cfg)]
    badge_rules: list[str] = []
    sidebar_index = 0  # 1-based count of elements emitted into st.sidebar

    # ── Brand block ────────────────────────────────────────────────────
    logo_src, icon_src = _pick_brand_sources(cfg)
    logo_url = src_to_css_url(logo_src, base_path)
    icon_url = src_to_css_url(icon_src, base_path)

    logo_render_height_px = int(cfg.get("logo_render_height_px") or 36)
    icon_render_height_px = int(cfg.get("icon_render_height_px") or 24)
    if logo_url or icon_url:
        css_parts.append(BRAND_CSS)
        if icon_url:
            css_parts.append(build_brand_icon_css(icon_url, icon_render_height_px))
        if logo_url:
            css_parts.append(build_brand_logo_css(logo_url, logo_render_height_px))
        st.sidebar.markdown(
            """
            <div class="srn-brand">
              <div class="srn-brand-icon"></div>
              <div class="srn-brand-logo"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        sidebar_index += 1

    logo_height_px = int(cfg.get("logo_height_px") or 0)
    if (logo_url or icon_url) and logo_height_px > 0:
        st.sidebar.markdown(
            f"<div style='height: {logo_height_px}px;'></div>",
            unsafe_allow_html=True,
        )
        sidebar_index += 1

    # ── Items ──────────────────────────────────────────────────────────
    for index, item in enumerate(cfg.get("items", [])):
        item_kind = str(item.get("kind", "link")).strip().lower()

        if item_kind == "separator":
            st.sidebar.markdown(
                "<div class='srn-menu-separator'></div>",
                unsafe_allow_html=True,
            )
            sidebar_index += 1
            continue

        if item_kind == "spacer":
            try:
                spacer_px = int(item.get("spacer_px", 16))
            except (TypeError, ValueError):
                spacer_px = 16
            spacer_px = max(4, min(64, spacer_px))
            st.sidebar.markdown(
                f"<div class='srn-menu-spacer' style='height: {spacer_px}px;'></div>",
                unsafe_allow_html=True,
            )
            sidebar_index += 1
            continue

        if item_kind == "header":
            label = html.escape(str(item.get("label") or "").strip())
            if label:
                st.sidebar.markdown(
                    f"<div class='srn-menu-header'>{label}</div>",
                    unsafe_allow_html=True,
                )
                sidebar_index += 1
            continue

        if item_kind == "theme_toggle":
            label = str(item.get("label") or "Dark mode").strip()
            icon_token = _icon_token(str(item.get("icon") or "dark_mode"))
            if st.sidebar.button(
                label,
                key=f"srn_theme_toggle_{index}",
                icon=icon_token,
                width="stretch",
            ):
                if on_theme_toggle is not None:
                    on_theme_toggle()
                st.rerun()
            sidebar_index += 1
            continue

        if item_kind == "search":
            label = str(item.get("label") or "Quick search").strip()
            icon_token = _icon_token(str(item.get("icon") or "search"))
            search_key = f"srn_search_{index}"

            def _on_search_change(key: str = search_key) -> None:
                if on_search is not None:
                    on_search(str(st.session_state.get(key) or ""))

            st.sidebar.text_input(
                label,
                key=search_key,
                placeholder=label,
                icon=icon_token,
                label_visibility="collapsed",
                on_change=_on_search_change if on_search is not None else None,
            )
            sidebar_index += 1
            continue

        if item_kind == "upgrade_card":
            title = html.escape(str(item.get("title") or "").strip())
            text = html.escape(str(item.get("text") or "").strip())
            button_label = str(item.get("button_label") or "").strip()
            st.sidebar.markdown(
                f"""
                <div class='srn-upgrade-card'>
                    <div class='srn-card-title'>{title}</div>
                    <div class='srn-card-text'>{text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            sidebar_index += 1
            if button_label:
                if st.sidebar.button(
                    button_label,
                    key=f"srn_upgrade_{index}",
                    width="stretch",
                ):
                    if on_upgrade_click is not None:
                        on_upgrade_click()
                    st.rerun()
                sidebar_index += 1
            continue

        if item_kind == "user_profile":
            name = str(item.get("name") or "").strip() or "User"
            subtitle = str(item.get("subtitle") or "").strip()
            avatar_url = str(item.get("avatar_url") or "").strip()
            initials = str(item.get("avatar_initials") or "").strip() or _initials(name)
            avatar_style = (
                f"background-image:url('{html.escape(avatar_url)}');"
                if avatar_url
                else ""
            )
            avatar_content = "" if avatar_url else html.escape(initials)
            profile_html = (
                "<div class='srn-user-profile'>"
                f"<div class='srn-avatar' style=\"{avatar_style}\">"
                f"{avatar_content}</div>"
                "<div class='srn-user-info' style='flex-grow: 1;'>"
                f"<div class='srn-user-name'>{html.escape(name)}</div>"
                f"<div class='srn-user-subtitle'>{html.escape(subtitle)}</div>"
                "</div>"
                "<div class='srn-user-info'>"
                "<span class='material-icons-sharp'>unfold_more</span>"
                "</div>"
                "</div>"
            )
            st.sidebar.markdown(profile_html, unsafe_allow_html=True)
            sidebar_index += 1
            continue

        # link / badge_link
        label = str(item.get("label", "")).strip()
        page = str(item.get("page", "")).strip()
        icon = str(item.get("icon", "")).strip()
        badge = str(item.get("badge", "")).strip()
        if not label or not page:
            continue
        icon_token = _icon_token(icon)

        try:
            st.sidebar.page_link(
                page,
                label=label,
                icon=icon_token,
                width="stretch",
            )
            sidebar_index += 1
            if badge:
                badge_rules.append(build_badge_css(sidebar_index, badge))
            continue
        except Exception:
            pass

        nav_key = f"srn_nav_{index}"
        if st.sidebar.button(
            label,
            key=nav_key,
            icon=icon_token,
            width="stretch",
        ):
            try:
                st.switch_page(page)
            except Exception:
                st.sidebar.error(f"{label} navigation requires Streamlit multipage.")
        sidebar_index += 1

    # ── Inject accumulated CSS (main area — does not consume a slot) ────
    st.markdown(
        f"<style>{''.join(css_parts)}{''.join(badge_rules)}</style>",
        unsafe_allow_html=True,
    )

    # ── Footer ─────────────────────────────────────────────────────────
    if footer:
        st.sidebar.divider()
        st.sidebar.caption(footer)
