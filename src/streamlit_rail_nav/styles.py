"""CSS builders for the rail navigation sidebar.

The generated CSS restyles Streamlit's native ``stSidebar`` so it collapses to
an icon rail when not hovered and expands on hover. All rules are scoped to
``section[data-testid='stSidebar']`` and use ``srn-`` prefixed classes and
``--srn-*`` custom properties to avoid collisions.

Note: selectors rely on Streamlit ``data-testid`` attributes which are not a
stable public API. Verified against Streamlit 1.57.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

FONT_IMPORT = (
    "@import url('https://fonts.googleapis.com/icon?family=Material+Icons+Sharp');"
)

BRAND_CSS = """
section[data-testid='stSidebar'] .srn-brand {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 12px 8px 6px 8px;
}
section[data-testid='stSidebar'] .srn-brand-icon,
section[data-testid='stSidebar'] .srn-brand-logo {
    background-repeat: no-repeat;
    background-position: center;
    background-size: contain;
    width: 100%;
}
section[data-testid='stSidebar']:hover .srn-brand-icon {
    display: none;
}
section[data-testid='stSidebar']:not(:hover) .srn-brand-logo {
    display: none;
}
"""

_NAV_HIDE_CSS = """
            /* Hide Streamlit's auto-generated multipage nav */
            section[data-testid='stSidebar'] [data-testid='stSidebarNav'] {
                display: none !important;
            }
"""


def build_brand_icon_css(icon_url: str, height_px: int) -> str:
    return (
        f".srn-brand-icon{{background-image:url('{icon_url}');"
        f"height:{height_px}px;width:{height_px}px;flex:0 0 {height_px}px;}}"
    )


def build_brand_logo_css(logo_url: str, height_px: int) -> str:
    return (
        f".srn-brand-logo{{background-image:url('{logo_url}');"
        f"height:{height_px}px;max-width:100%;}}"
    )


def build_rail_css(cfg: Mapping[str, Any]) -> str:
    """Build the full sidebar stylesheet from a normalized settings dict."""
    separator_color = str(cfg.get("sidebar_separator_color") or "#6C757D").strip()
    sidebar_text_color = str(cfg.get("sidebar_text_color") or "").strip()
    sidebar_icon_color = str(cfg.get("sidebar_icon_color") or "").strip()
    sidebar_bg_color = str(cfg.get("sidebar_bg") or "").strip()

    return f"""
        {FONT_IMPORT}
        :root {{
            /* Use Streamlit's native theme colors as fallbacks */
            --srn-bg: {sidebar_bg_color or "var(--secondaryBackgroundColor)"};
            --srn-text: {sidebar_text_color or "var(--textColor)"};
            --srn-icon: {sidebar_icon_color or "var(--textColor)"};
            --srn-hover-bg: {cfg["sidebar_hover_bg"] or "var(--primaryColor)"};
            --srn-hover-text: {cfg.get("sidebar_hover_text_color", sidebar_text_color) or "var(--textColor)"};
            --srn-active-bg: {cfg["sidebar_active_bg"] or "var(--primaryColor)"};
            --srn-focus-outline: {cfg["sidebar_focus_outline"] or "var(--primaryColor)"};
            --srn-accent: {cfg.get("sidebar_focus_outline", "#3B5998") or "var(--primaryColor)"};
            --srn-separator-color: {separator_color or "rgba(0,0,0,0.1)"};
            --srn-font-size: {cfg["sidebar_font_size_px"]}px;
            --srn-icon-size: {cfg.get("sidebar_icon_size_px", 20)}px;
            --srn-collapsed-width: {cfg["sidebar_collapsed_width_px"]}px;
            --srn-hover-width: {cfg["sidebar_hover_width_px"]}px;
            --srn-item-gap: {cfg.get("sidebar_item_gap_px", 4)}px;
            --srn-transition: {cfg["sidebar_transition"]};
        }}
            {_NAV_HIDE_CSS if cfg.get("hide_default_nav") else ""}
            /* Apply sidebar background color */
            section[data-testid='stSidebar'] {{
                background-color: var(--srn-bg) !important;
            }}

            /* Keep the first menu item at the same vertical position while
               the sidebar changes width on hover. */
            section[data-testid='stSidebar'] > div:first-child,
            section[data-testid='stSidebar'] [data-testid='stSidebarContent'],
            section[data-testid='stSidebar'] [data-testid='stSidebarUserContent'] {{
                padding-top: 12px !important;
            }}

            /* Page Links and Buttons - Expanded State */
            section[data-testid='stSidebar'] [data-testid='stPageLink'] a,
            section[data-testid='stSidebar'] .stButton button {{
                display: flex;
                align-items: center;
                gap: 12px;
                border-radius: 8px;
                padding: 6px 12px;
                height: 50px;
                box-sizing: border-box;
                text-decoration: none;
                white-space: nowrap;
                overflow: hidden;
                transition: background-color var(--srn-transition);
                background-color: transparent !important;
                border: none !important;
                width: 100%;
                text-align: left;
                justify-content: flex-start !important;
            }}

            section[data-testid='stSidebar'] [data-testid='stPageLink'] a:hover,
            section[data-testid='stSidebar'] .stButton button:hover {{
                background-color: var(--srn-hover-bg) !important;
            }}

            /* Active State */
            section[data-testid='stSidebar'] [data-testid='stPageLink'] a[aria-current='page'],
            section[data-testid='stSidebar'] [data-testid='stPageLink'] a[data-active='true'],
            section[data-testid='stSidebar'] [data-testid='stPageLink'] a[data-selected='true'],
            section[data-testid='stSidebar'] [data-testid='stPageLink'] a[aria-selected='true'],
            section[data-testid='stSidebar'] .stButton button[data-active='true'] {{
                background-color: var(--srn-active-bg) !important;
                box-shadow: none !important;
            }}

            /* Text color for menu labels */
            section[data-testid='stSidebar'] [data-testid='stPageLink'] a p,
            section[data-testid='stSidebar'] [data-testid='stPageLink'] a span,
            section[data-testid='stSidebar'] .stButton button p,
            section[data-testid='stSidebar'] .stButton button span,
            section[data-testid='stSidebar'] .stMarkdown p,
            section[data-testid='stSidebar'] .stMarkdown span {{
                color: var(--srn-text) !important;
            }}

            section[data-testid='stSidebar'] [data-testid='stPageLink'] a svg,
            section[data-testid='stSidebar'] .stButton button svg,
            section[data-testid='stSidebar'] .stButton button [data-testid='stIconMaterial'] {{
                fill: var(--srn-icon) !important;
                color: var(--srn-icon) !important;
            }}

            section[data-testid='stSidebar'] [data-testid='stPageLink'] a[aria-current='page'] svg,
            section[data-testid='stSidebar'] [data-testid='stPageLink'] a[data-active='true'] svg,
            section[data-testid='stSidebar'] .stButton button[data-active='true'] svg {{
                fill: var(--srn-accent) !important;
                color: var(--srn-accent) !important;
            }}

            /* Rail Mode Adjustments */
            section[data-testid='stSidebar']:not(:hover) {{
                width: var(--srn-collapsed-width) !important;
                min-width: var(--srn-collapsed-width) !important;
                max-width: var(--srn-collapsed-width) !important;
            }}

            section[data-testid='stSidebar']:not(:hover) > div:first-child,
            section[data-testid='stSidebar']:not(:hover) [data-testid='stSidebarContent'],
            section[data-testid='stSidebar']:not(:hover) [data-testid='stSidebarUserContent'] {{
                width: var(--srn-collapsed-width) !important;
                min-width: var(--srn-collapsed-width) !important;
                padding: 12px 0 0 !important;
            }}

            section[data-testid='stSidebar']:not(:hover) [data-testid='stElementContainer'],
            section[data-testid='stSidebar']:not(:hover) [data-testid='stVerticalBlock'] {{
                width: var(--srn-collapsed-width) !important;
                display: flex !important;
                justify-content: center !important;
                padding: 0 !important;
                margin: 0 !important;
            }}

            section[data-testid='stSidebar']:not(:hover) [data-testid='stPageLink'],
            section[data-testid='stSidebar']:not(:hover) .stButton {{
                width: var(--srn-collapsed-width) !important;
                padding: 0 !important;
                margin: 0 !important;
                display: flex !important;
                justify-content: center !important;
            }}

            section[data-testid='stSidebar']:not(:hover) [data-testid='stPageLink'] a,
            section[data-testid='stSidebar']:not(:hover) .stButton button {{
                display: flex !important;
                flex-direction: row !important;
                justify-content: center !important;
                align-items: center !important;
                padding: 0 !important;
                width: var(--srn-collapsed-width) !important;
                height:42px !important;
                margin: 0 !important;
                gap: 0 !important;
                border-radius: 8px !important;
                padding-left: 0 !important;
            }}

            /* Override Streamlit default 16px gap between sidebar items */
            section[data-testid='stSidebar'] [data-testid='stVerticalBlock'] {{
                gap: var(--srn-item-gap) !important;
                row-gap: var(--srn-item-gap) !important;
            }}

            section[data-testid='stSidebar'] [data-testid='stElementContainer'] {{
                padding-top: 0 !important;
                padding-bottom: 0 !important;
            }}

            /* Custom non-widget items need their own predictable rhythm. */
            section[data-testid='stSidebar'] .srn-menu-header {{
                line-height: 16px;
                margin: 4px 0 0;
            }}
            section[data-testid='stSidebar'] .srn-menu-spacer {{
                display: block;
                width: 100%;
            }}

            section[data-testid='stSidebar'] [data-testid='stPageLink'] a p,
            section[data-testid='stSidebar'] .stButton button p {{
                margin: 0 !important;
                white-space: nowrap !important;
                overflow: hidden !important;
            }}

            section[data-testid='stSidebar']:not(:hover) [data-testid='stPageLink'] a p,
            section[data-testid='stSidebar']:not(:hover) .stButton button p,
            section[data-testid='stSidebar']:not(:hover) .srn-menu-header,
            section[data-testid='stSidebar']:not(:hover) .srn-user-info,
            section[data-testid='stSidebar']:not(:hover) .srn-card-text,
            section[data-testid='stSidebar']:not(:hover) .stTextInput,
            section[data-testid='stSidebar']:not(:hover) .srn-upgrade-card,
            section[data-testid='stSidebar']:not(:hover) .stMarkdown p {{
                display: none !important;
            }}

            /* Badges only make sense next to their (hidden) labels */
            section[data-testid='stSidebar']:not(:hover) [data-testid='stPageLink'] a::after {{
                display: none !important;
            }}

            /* CTA button paired with a hidden upgrade card */
            section[data-testid='stSidebar']:not(:hover)
                [data-testid='stElementContainer']:has(.srn-upgrade-card)
                + [data-testid='stElementContainer'] {{
                display: none !important;
            }}

            section[data-testid='stSidebar']:not(:hover) .stButton {{
                padding: 0 !important;
                margin: 0 !important;
            }}
            section[data-testid='stSidebar']:not(:hover) [data-testid='stPageLink'] {{
                padding: 0 !important;
                margin: 0 !important;
            }}
            section[data-testid='stSidebar']:not(:hover) .srn-avatar {{
                margin: 0 auto !important;
            }}
            section[data-testid='stSidebar']:not(:hover) .srn-user-profile {{
                justify-content: center !important;
                padding: 12px 0 !important;
            }}

            section[data-testid='stSidebar']:hover [data-testid='stPageLink'] a p,
            section[data-testid='stSidebar']:hover .stButton button p {{
                opacity: 1;
                max-width: 200px;
            }}

            /* Custom Components */
            section[data-testid='stSidebar'] .srn-menu-separator {{
                height: 1px;
                margin: 8px 12px;
                background-color: var(--srn-separator-color);
            }}

            section[data-testid='stSidebar'] .srn-menu-header {{
                padding: 16px 12px 8px 12px;
                font-size: calc(var(--srn-font-size) - 2px);
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                color: var(--srn-text);
                opacity: 0.6;
            }}

            section[data-testid='stSidebar'] .srn-user-profile {{
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 12px;
                margin-top: auto;
                border-top: 1px solid var(--srn-separator-color);
            }}

            section[data-testid='stSidebar'] .srn-user-info {{
                color: var(--srn-text);
            }}

            section[data-testid='stSidebar'] .srn-user-info .srn-user-name {{
                font-weight: 600;
                font-size: 13px;
            }}

            section[data-testid='stSidebar'] .srn-user-info .srn-user-subtitle {{
                font-weight: 300;
                font-size: 10px;
                opacity: 0.7;
            }}

            section[data-testid='stSidebar'] .srn-user-info .material-icons-sharp {{
                font-size: 16px;
                opacity: 0.7;
            }}

            section[data-testid='stSidebar'] .srn-avatar {{
                width: 32px;
                height: 32px;
                border-radius: 50%;
                background-color: var(--srn-hover-bg);
                background-size: cover;
                background-position: center;
                flex-shrink: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                color: var(--srn-text);
                font-size: 13px;
                font-weight: 600;
            }}

            section[data-testid='stSidebar'] .srn-upgrade-card {{
                margin: 8px 12px;
                padding: 12px;
                border-radius: 8px;
                border: 1px solid var(--srn-separator-color);
                background-color: var(--srn-hover-bg);
            }}

            section[data-testid='stSidebar'] .srn-upgrade-card .srn-card-title {{
                color: var(--srn-text);
                font-weight: 600;
                font-size: var(--srn-font-size);
            }}

            section[data-testid='stSidebar'] .srn-upgrade-card .srn-card-text {{
                color: var(--srn-text);
                opacity: 0.75;
                font-size: calc(var(--srn-font-size) - 2px);
            }}

            section[data-testid='stSidebar'] .srn-badge {{
                background: var(--srn-hover-bg);
                color: var(--srn-text);
                padding: 2px 6px;
                border-radius: 10px;
                font-size: 11px;
                font-weight: 600;
                margin-left: auto;
            }}

            /* Search input blends into the sidebar palette */
            section[data-testid='stSidebar'] [data-testid='stTextInput'] {{
                margin: 4px 0 !important;
            }}
            section[data-testid='stSidebar'] [data-testid='stTextInput'] [data-baseweb='input'] {{
                height: 40px !important;
                min-height: 40px !important;
                background-color: var(--srn-bg) !important;
                border: 1px solid var(--srn-separator-color) !important;
                border-radius: 8px !important;
                box-shadow: none !important;
            }}
            section[data-testid='stSidebar'] [data-testid='stTextInput'] [data-baseweb='input'] > div {{
                background-color: transparent !important;
            }}
            section[data-testid='stSidebar'] [data-testid='stTextInput'] input {{
                height: 38px !important;
                background-color: transparent !important;
                color: var(--srn-text) !important;
                font-size: 13px !important;
            }}
            section[data-testid='stSidebar'] [data-testid='stTextInput'] input::placeholder {{
                color: var(--srn-text) !important;
                opacity: 0.6 !important;
            }}
            section[data-testid='stSidebar'] [data-testid='stTextInput'] [data-testid='stIconMaterial'] {{
                color: var(--srn-icon) !important;
                font-size: 18px !important;
            }}

            /* Button directly after an upgrade card renders as a CTA */
            section[data-testid='stSidebar'] [data-testid='stElementContainer']:has(.srn-upgrade-card)
                + [data-testid='stElementContainer'] {{
                padding-top: 8px !important;
            }}
            section[data-testid='stSidebar'] [data-testid='stElementContainer']:has(.srn-upgrade-card)
                + [data-testid='stElementContainer'] .stButton button {{
                height: 42px !important;
                background-color: var(--srn-bg) !important;
                border: 1px solid var(--srn-separator-color) !important;
                justify-content: center !important;
            }}

            /* Sidebar caption, small text, auth notices */
            section[data-testid='stSidebar'] [data-testid='stCaptionContainer'] p,
            section[data-testid='stSidebar'] small,
            section[data-testid='stSidebar'] .stCaption p,
            section[data-testid='stSidebar'] [data-testid='stText'] p {{
                color: var(--srn-text) !important;
                opacity: 0.75;
            }}

            /* Secondary/primary buttons in sidebar */
            section[data-testid='stSidebar'] [data-testid='stBaseButton-secondary'],
            section[data-testid='stSidebar'] [data-testid='stBaseButton-primary'] {{
                color: var(--srn-text) !important;
                border-color: var(--srn-separator-color) !important;
                background-color: transparent !important;
            }}
            section[data-testid='stSidebar'] [data-testid='stBaseButton-secondary']:hover,
            section[data-testid='stSidebar'] [data-testid='stBaseButton-primary']:hover {{
                background-color: var(--srn-hover-bg) !important;
                border-color: var(--srn-focus-outline) !important;
            }}
            section[data-testid='stSidebar'] [data-testid='stBaseButton-secondary'] p,
            section[data-testid='stSidebar'] [data-testid='stBaseButton-primary'] p,
            section[data-testid='stSidebar'] [data-testid='stBaseButton-secondary'] [data-testid='stIconMaterial'],
            section[data-testid='stSidebar'] [data-testid='stBaseButton-primary'] [data-testid='stIconMaterial'] {{
                color: var(--srn-text) !important;
            }}

            section[data-testid='stSidebar']:hover [data-testid='stPageLink'] a p {{
                opacity: 1;
                max-width: 200px;
            }}
    """


def build_badge_css(element_index: int, badge_text: str) -> str:
    """Build CSS that appends a badge pill to the nth sidebar element.

    ``element_index`` is the 1-based ordinal of the item's element container
    among all element containers rendered into the sidebar. The renderer tracks
    this while emitting items.
    """
    safe_text = badge_text.replace("'", "\\'")
    return (
        "section[data-testid='stSidebar'] "
        f"[data-testid='stVerticalBlock'] > [data-testid='stElementContainer']:nth-of-type({element_index}) "
        f"[data-testid='stPageLink'] a::after {{"
        f"content: '{safe_text}';"
        "background: var(--srn-hover-bg);"
        "color: var(--srn-text);"
        "padding: 2px 6px;"
        "border-radius: 10px;"
        "font-size: 11px;"
        "font-weight: 600;"
        "margin-left: auto;"
        "}"
    )
