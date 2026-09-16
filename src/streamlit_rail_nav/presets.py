"""Named color presets for the rail navigation sidebar.

Each preset maps a subset of the settings keys (see
:mod:`streamlit_rail_nav.settings`) to color values. Apply a preset by merging
it over a settings dict before calling ``render()``.

Colors are chosen so every state passes WCAG AA contrast for normal text
(>= 4.5:1) against its own background:

- ``sidebar_bg`` / ``sidebar_text_color`` -- the resting state.
- ``sidebar_hover_bg`` / ``sidebar_hover_text_color`` -- momentary rollover;
  ``sidebar_hover_bg`` is typically the boldest, most saturated brand color.
- ``sidebar_active_bg`` -- the persistent "selected page" background. It is
  deliberately a *subtle* tint close to ``sidebar_bg`` rather than the loud
  hover color, so the label text (which always uses ``sidebar_text_color``,
  not a separate active-text setting) stays readable. ``sidebar_focus_outline``
  supplies the accent color for the selected item's icon, giving a clear
  selection indicator without sacrificing contrast.
"""

from __future__ import annotations

THEME_PRESETS: dict[str, dict[str, str]] = {
    "Anthropic Style": {
        # Colors from Anthropic's public brand guidelines
        # (github.com/anthropics/skills, skills/brand-guidelines).
        "sidebar_bg": "#E8E6DC",
        "sidebar_text_color": "#141413",
        "sidebar_icon_color": "#141413",
        "sidebar_hover_bg": "#D97757",
        "sidebar_hover_text_color": "#141413",
        "sidebar_active_bg": "#F0EEE6",
        "sidebar_focus_outline": "#D97757",
        "sidebar_separator_color": "#D1CFC5",
    },
    "Ocean Palette": {
        "sidebar_bg": "#395B77",
        "sidebar_text_color": "#F6F7EF",
        "sidebar_icon_color": "#F6F7EF",
        "sidebar_hover_bg": "#7BA8CA",
        "sidebar_hover_text_color": "#0B1220",
        "sidebar_active_bg": "#4C6B84",
        "sidebar_focus_outline": "#A8DAFF",
        "sidebar_separator_color": "#7BA8CA",
    },
    "Corpus Analytica": {
        "sidebar_bg": "#263741",
        "sidebar_text_color": "#EEF2F1",
        "sidebar_icon_color": "#EEF2F1",
        "sidebar_hover_bg": "#EA9216",
        "sidebar_hover_text_color": "#263741",
        "sidebar_active_bg": "#374750",
        "sidebar_focus_outline": "#C3CCD2",
        "sidebar_separator_color": "#C3CCD2",
    },
    "Navy Gold Aqua": {
        "sidebar_bg": "#083A4F",
        "sidebar_text_color": "#E5E1DD",
        "sidebar_icon_color": "#E5E1DD",
        "sidebar_hover_bg": "#407E8C",
        "sidebar_hover_text_color": "#FFFFFF",
        "sidebar_active_bg": "#204D60",
        "sidebar_focus_outline": "#A58D66",
        "sidebar_separator_color": "#C0D5D6",
    },
    "Cadet Yam": {
        "sidebar_bg": "#313841",
        "sidebar_text_color": "#EEEEEE",
        "sidebar_icon_color": "#EEEEEE",
        "sidebar_hover_bg": "#3A4750",
        "sidebar_hover_text_color": "#EEEEEE",
        "sidebar_active_bg": "#515D65",
        "sidebar_focus_outline": "#EA9216",
        "sidebar_separator_color": "#3A4750",
    },
    "Matcha Almond": {
        "sidebar_bg": "#1A3636",
        "sidebar_text_color": "#D6BD98",
        "sidebar_icon_color": "#D6BD98",
        "sidebar_hover_bg": "#40534C",
        "sidebar_hover_text_color": "#D6BD98",
        "sidebar_active_bg": "#354E4E",
        "sidebar_focus_outline": "#677D6A",
        "sidebar_separator_color": "#40534C",
    },
    "Black & White (Light)": {
        "sidebar_bg": "#EBEBEB",
        "sidebar_text_color": "#111111",
        "sidebar_icon_color": "#111111",
        "sidebar_hover_bg": "#F2F2F2",
        "sidebar_hover_text_color": "#111111",
        "sidebar_active_bg": "#E6E6E6",
        "sidebar_focus_outline": "#111111",
        "sidebar_separator_color": "#D0D0D0",
    },
    "Black & White (Dark)": {
        "sidebar_bg": "#2E333A",
        "sidebar_text_color": "#EBEBEB",
        "sidebar_icon_color": "#EBEBEB",
        "sidebar_hover_bg": "#3B4048",
        "sidebar_hover_text_color": "#EBEBEB",
        "sidebar_active_bg": "#3B4048",
        "sidebar_focus_outline": "#EBEBEB",
        "sidebar_separator_color": "#4A4F57",
    },
}
