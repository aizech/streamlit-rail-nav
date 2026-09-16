# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - Unreleased

### Added

- Initial release extracted from [halo-core](https://github.com/aizech/halo-core).
- `render(config)` entry point rendering a collapsible icon-rail sidebar that
  expands on hover, built on native Streamlit sidebar widgets plus injected CSS.
- Config schema with normalization via `normalize_settings()` and
  `DEFAULT_RAIL_SETTINGS`.
- Item kinds: `link`, `badge_link`, `separator`, `spacer`, `header`,
  `theme_toggle`, `search`, `upgrade_card`, `user_profile`.
- `THEME_PRESETS` with eight named color palettes, each verified to pass
  WCAG AA contrast for resting and hover text against their backgrounds.
- Brand logo/icon hover-swap with light/dark asset variants.
- Optional callbacks: `on_theme_toggle`, `on_search`, `on_upgrade_click`.
- `hide_default_nav` (default on) hides Streamlit's auto-generated multipage
  navigation so it does not duplicate custom menu items.

### Fixed

- Badges (`badge_link` / `link` `badge`) no longer render while the sidebar is
  collapsed into the rail.
- Sidebar `search` inputs and `upgrade_card` buttons are themed to match the
  configured sidebar palette.
- `sidebar_hover_text_color` is now actually applied to the rollover text and
  icon color; it was defined per preset but never wired into the generated
  CSS.
- Recolored `sidebar_active_bg` across presets to a subtle tint instead of a
  loud accent color, fixing poor text/icon contrast (and, for `Cadet Yam`,
  an icon that was the same color as its own active background).
- Updated `Anthropic Style` to match Anthropic's public brand guidelines.

### Changed

- Renamed the `Slate Orange` preset to `Corpus Analytica`.

### Removed

- Removed the `HALO Core Palette` preset; use `Cadet Yam`, which has the same
  base colors without the HALO-specific extra keys.
