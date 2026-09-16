from __future__ import annotations

import textwrap
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

RENDER_SCRIPT = textwrap.dedent("""
    import streamlit as st
    from streamlit_rail_nav import render

    render({
        "items": [
            {"kind": "header", "label": "Main"},
            {"kind": "link", "label": "Missing", "icon": "home",
             "page": "pages/DoesNotExist.py"},
            {"kind": "separator"},
            {"kind": "spacer", "spacer_px": 24},
            {"kind": "search", "label": "Quick search", "icon": "search"},
            {"kind": "theme_toggle", "label": "Dark mode",
             "icon": "dark_mode"},
            {
                "kind": "upgrade_card",
                "title": "Go Pro",
                "text": "Unlock everything",
                "button_label": "Upgrade",
            },
            {"kind": "user_profile", "name": "Ada Lovelace",
             "subtitle": "Pro trial"},
        ],
    }, footer="Made for tests")
    """)


def test_render_emits_all_item_kinds() -> None:
    at = AppTest.from_string(RENDER_SCRIPT).run()

    assert not at.exception

    sidebar_md = [m.value for m in at.sidebar.markdown]
    assert any("srn-menu-header" in m and "Main" in m for m in sidebar_md)
    assert any("srn-menu-separator" in m for m in sidebar_md)
    assert any("srn-menu-spacer" in m for m in sidebar_md)
    assert any("srn-upgrade-card" in m for m in sidebar_md)
    assert any("srn-user-profile" in m for m in sidebar_md)
    assert any("Ada Lovelace" in m for m in sidebar_md)

    # theme_toggle + upgrade button + fallback nav button for missing page
    button_labels = [b.label for b in at.sidebar.button]
    assert "Dark mode" in button_labels
    assert "Upgrade" in button_labels
    assert "Missing" in button_labels

    assert len(at.sidebar.text_input) == 1
    assert at.sidebar.text_input[0].placeholder == "Quick search"

    captions = [c.value for c in at.sidebar.caption]
    assert any("Made for tests" in c for c in captions)


def test_render_injects_css_once() -> None:
    at = AppTest.from_string(RENDER_SCRIPT).run()

    assert not at.exception
    main_md = [m.value for m in at.markdown]
    style_blocks = [m for m in main_md if "--srn-collapsed-width" in m]
    assert len(style_blocks) == 1


def test_render_empty_config_does_not_crash() -> None:
    at = AppTest.from_string(
        "import streamlit as st\n"
        "from streamlit_rail_nav import render\n"
        "render()\n"
    ).run()

    assert not at.exception
    assert len(at.sidebar.markdown) == 0


def test_theme_toggle_invokes_callback() -> None:
    script = textwrap.dedent("""
        import streamlit as st
        from streamlit_rail_nav import render

        def _toggle():
            st.session_state["toggled"] = True

        render({"items": [{"kind": "theme_toggle", "label": "Dark mode"}]},
               on_theme_toggle=_toggle)
        """)
    at = AppTest.from_string(script).run()
    assert not at.exception

    at.sidebar.button[0].click().run()
    assert not at.exception
    assert at.session_state["toggled"] is True


def test_search_invokes_callback_with_query() -> None:
    script = textwrap.dedent("""
        import streamlit as st
        from streamlit_rail_nav import render

        def _search(q):
            st.session_state["last_query"] = q

        render({"items": [{"kind": "search", "label": "Find"}]},
               on_search=_search)
        """)
    at = AppTest.from_string(script).run()
    assert not at.exception

    at.sidebar.text_input[0].set_value("needle").run()
    assert not at.exception
    assert at.session_state["last_query"] == "needle"


@pytest.fixture()
def multipage_app(tmp_path: Path) -> Path:
    pages_dir = tmp_path / "pages"
    pages_dir.mkdir()
    (pages_dir / "Second.py").write_text(
        "import streamlit as st\nst.title('Second')\n",
        encoding="utf-8",
    )
    app = tmp_path / "app.py"
    app.write_text(
        textwrap.dedent("""
            import streamlit as st
            from streamlit_rail_nav import render

            render({"items": [
                {"kind": "link", "label": "Home", "icon": "home",
                 "page": "app.py"},
                {"kind": "badge_link", "label": "Second",
                 "icon": "table", "page": "pages/Second.py",
                 "badge": "New"},
            ]})
            """),
        encoding="utf-8",
    )
    return app


def test_render_page_links_in_multipage_app(multipage_app: Path) -> None:
    at = AppTest.from_file(str(multipage_app)).run()

    assert not at.exception
    # Real page_link elements render instead of button fallbacks
    assert len(at.sidebar.button) == 0
    # Badge CSS targets the second sidebar element (nth-of-type(2))
    main_md = [m.value for m in at.markdown]
    badge_rules = [
        m for m in main_md if "nth-of-type(2)" in m and "content: 'New'" in m
    ]
    assert len(badge_rules) == 1
