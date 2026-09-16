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
- `THEME_PRESETS` with nine named color palettes.
- Brand logo/icon hover-swap with light/dark asset variants.
- Optional callbacks: `on_theme_toggle`, `on_search`, `on_upgrade_click`.
