"""streamlit-rail-nav — collapsible icon-rail sidebar navigation for Streamlit.

Pure Python: renders native ``st.sidebar`` widgets and restyles the sidebar
into an icon rail that expands on hover, via injected CSS. No frontend build.

Quickstart::

    import streamlit as st
    from streamlit_rail_nav import render

    st.set_page_config(layout="wide", initial_sidebar_state="expanded")

    render({
        "items": [
            {"kind": "link", "label": "Home", "icon": "home", "page": "app.py"},
            {"kind": "link", "label": "Data", "icon": "table",
             "page": "pages/Data.py"},
            {"kind": "separator"},
            {"kind": "user_profile", "name": "Ada Lovelace",
             "subtitle": "Pro trial"},
        ],
    })
"""

from streamlit_rail_nav.presets import THEME_PRESETS
from streamlit_rail_nav.renderer import render
from streamlit_rail_nav.settings import (
    ALLOWED_ACCESS_LEVELS,
    DEFAULT_RAIL_SETTINGS,
    ITEM_KINDS,
    normalize_settings,
)

__version__ = "0.1.0"

__all__ = [
    "ALLOWED_ACCESS_LEVELS",
    "DEFAULT_RAIL_SETTINGS",
    "ITEM_KINDS",
    "THEME_PRESETS",
    "__version__",
    "normalize_settings",
    "render",
]
