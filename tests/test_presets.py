from __future__ import annotations

import pytest

from streamlit_rail_nav import THEME_PRESETS

# WCAG AA minimum for normal-size text.
_MIN_TEXT_CONTRAST = 4.5


def _relative_luminance(hex_color: str) -> float:
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i : i + 2], 16) / 255 for i in (0, 2, 4))

    def channel(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = channel(r), channel(g), channel(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _contrast_ratio(hex_a: str, hex_b: str) -> float:
    lum_a, lum_b = _relative_luminance(hex_a), _relative_luminance(hex_b)
    lighter, darker = max(lum_a, lum_b), min(lum_a, lum_b)
    return (lighter + 0.05) / (darker + 0.05)


@pytest.mark.parametrize("preset_name", sorted(THEME_PRESETS.keys()))
def test_resting_text_meets_aa_contrast(preset_name: str) -> None:
    preset = THEME_PRESETS[preset_name]
    ratio = _contrast_ratio(preset["sidebar_bg"], preset["sidebar_text_color"])
    assert ratio >= _MIN_TEXT_CONTRAST, (
        f"{preset_name}: sidebar_bg/sidebar_text_color contrast {ratio:.2f} "
        f"< {_MIN_TEXT_CONTRAST}"
    )


@pytest.mark.parametrize("preset_name", sorted(THEME_PRESETS.keys()))
def test_hover_text_meets_aa_contrast(preset_name: str) -> None:
    preset = THEME_PRESETS[preset_name]
    ratio = _contrast_ratio(
        preset["sidebar_hover_bg"], preset["sidebar_hover_text_color"]
    )
    assert ratio >= _MIN_TEXT_CONTRAST, (
        f"{preset_name}: sidebar_hover_bg/sidebar_hover_text_color contrast "
        f"{ratio:.2f} < {_MIN_TEXT_CONTRAST}"
    )


@pytest.mark.parametrize("preset_name", sorted(THEME_PRESETS.keys()))
def test_active_bg_stays_readable_with_resting_text(preset_name: str) -> None:
    """Active state reuses sidebar_text_color (no separate setting), so
    sidebar_active_bg must itself contrast well against it."""
    preset = THEME_PRESETS[preset_name]
    ratio = _contrast_ratio(preset["sidebar_active_bg"], preset["sidebar_text_color"])
    assert ratio >= _MIN_TEXT_CONTRAST, (
        f"{preset_name}: sidebar_active_bg/sidebar_text_color contrast "
        f"{ratio:.2f} < {_MIN_TEXT_CONTRAST}"
    )


def test_renamed_and_removed_presets() -> None:
    assert "Corpus Analytica" in THEME_PRESETS
    assert "Slate Orange" not in THEME_PRESETS
    assert "HALO Core Palette" not in THEME_PRESETS


def test_required_keys_present_on_every_preset() -> None:
    required = {
        "sidebar_bg",
        "sidebar_text_color",
        "sidebar_icon_color",
        "sidebar_hover_bg",
        "sidebar_hover_text_color",
        "sidebar_active_bg",
        "sidebar_focus_outline",
        "sidebar_separator_color",
    }
    for name, preset in THEME_PRESETS.items():
        missing = required - preset.keys()
        assert not missing, f"{name} missing keys: {missing}"
