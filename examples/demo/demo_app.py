"""Demo app for streamlit-rail-nav.

Run from the package root:

    streamlit run examples/demo/demo_app.py
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from streamlit_rail_nav import THEME_PRESETS, render

st.set_page_config(
    page_title="rail-nav demo",
    page_icon=":material/view_sidebar:",
    layout="wide",
    initial_sidebar_state="expanded",
)

preset_name = st.session_state.get("preset", "Corpus Analytica")

config = {
    **THEME_PRESETS.get(preset_name, {}),
    "logo_src_light": "assets/logo_light.png",
    "logo_src_dark": "assets/logo_dark.png",
    "icon_src_light": "assets/icon_light.png",
    "icon_src_dark": "assets/icon_dark.png",
    "items": [
        {"kind": "link", "label": "Home", "icon": "home", "page": "demo_app.py"},
        {
            "kind": "badge_link",
            "label": "Second page",
            "icon": "table",
            "page": "pages/Second.py",
            "badge": "New",
        },
        {
            "kind": "link",
            "label": "Third page",
            "icon": "science",
            "page": "pages/Third.py",
        },
        {"kind": "separator"},
        {"kind": "header", "label": "Tools"},
        {"kind": "search", "label": "Quick search", "icon": "search"},
        {"kind": "theme_toggle", "label": "Dark mode", "icon": "dark_mode"},
        {"kind": "spacer", "spacer_px": 32},
        {
            "kind": "upgrade_card",
            "title": "Go Pro",
            "text": "Unlock all presets and badge links.",
            "button_label": "Upgrade",
        },
        {
            "kind": "user_profile",
            "name": "Ada Lovelace",
            "subtitle": "Pro trial",
        },
    ],
}


def _toggle_theme() -> None:
    current = st.session_state.get("preset", "Corpus Analytica")
    st.session_state["preset"] = (
        "Black & White (Dark)"
        if current != "Black & White (Dark)"
        else "Black & White (Light)"
    )


def _search(query: str) -> None:
    if query:
        st.session_state["last_search"] = query


render(
    config,
    base_path=Path(__file__).parent,
    on_theme_toggle=_toggle_theme,
    on_search=_search,
    on_upgrade_click=lambda: st.toast("Upgrade clicked!"),
    footer="streamlit-rail-nav demo",
)

st.title("streamlit-rail-nav demo")
st.caption("Hover the sidebar to expand the icon rail.")

preset = st.selectbox(
    "Theme preset",
    options=sorted(THEME_PRESETS.keys()),
    index=sorted(THEME_PRESETS.keys()).index(preset_name),
    key="preset_picker",
)
if preset != preset_name:
    st.session_state["preset"] = preset
    st.rerun()

if st.session_state.get("last_search"):
    st.info(f"Last search: {st.session_state['last_search']}")

st.write(
    "Item kinds in this demo: `link`, `badge_link`, `separator`, `header`, "
    "`search`, `theme_toggle`, `spacer`, `upgrade_card`, `user_profile`."
)
