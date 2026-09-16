"""Asset helpers for resolving logo/icon sources to CSS-usable URLs."""

from __future__ import annotations

import base64
import mimetypes
from pathlib import Path


def src_to_css_url(src: str, base_path: str | Path | None = None) -> str:
    """Resolve an image source to a URL usable inside CSS.

    - ``http(s)://`` sources are returned unchanged.
    - Local files are embedded as base64 data URLs.
    - Relative paths resolve against ``base_path``; pass the directory
      containing your app's entrypoint (e.g. ``Path(__file__).parent``).
    - Missing/unresolvable sources return ``""``.
    """
    cleaned = str(src or "").strip()
    if not cleaned:
        return ""
    if cleaned.startswith("http://") or cleaned.startswith("https://"):
        return cleaned
    if cleaned.startswith("data:"):
        return cleaned

    candidate = Path(cleaned)
    if not candidate.is_absolute():
        if base_path is None:
            return ""
        candidate = Path(base_path) / cleaned
    if not candidate.exists() or not candidate.is_file():
        return ""

    mime, _ = mimetypes.guess_type(str(candidate))
    if not mime:
        mime = "application/octet-stream"
    encoded = base64.b64encode(candidate.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"
