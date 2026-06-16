from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus
import json
from pathlib import Path
from typing import Optional

from .registry import get_http_ui_bootstrap_payload, get_http_ui_module_specs


_ASSET_DIR = Path(__file__).resolve().parent / "assets"

_VUE_DIST_DIR = Path(__file__).resolve().parents[2] / "ui" / "dist"


@dataclass(frozen=True)
class HTTPUIAssetResponse:
    status: HTTPStatus
    content_type: str
    body: bytes


def _read_binary(path: Path) -> bytes:
    return path.read_bytes()


def _guess_mime(path: str) -> str:
    lower = path.lower()
    if lower.endswith(".html") or lower.endswith(".htm"):
        return "text/html; charset=utf-8"
    if lower.endswith(".css"):
        return "text/css; charset=utf-8"
    if lower.endswith(".js"):
        return "application/javascript; charset=utf-8"
    if lower.endswith(".json"):
        return "application/json; charset=utf-8"
    if lower.endswith(".svg"):
        return "image/svg+xml"
    if lower.endswith(".png"):
        return "image/png"
    if lower.endswith(".ico"):
        return "image/x-icon"
    return "application/octet-stream"


def _serve_vue_file(path: str) -> Optional[HTTPUIAssetResponse]:
    if not _VUE_DIST_DIR.exists():
        return None

    normalized = str(path or "").strip().rstrip("/") or "/"

    if normalized == "/":
        index_path = _VUE_DIST_DIR / "index.html"
        if index_path.exists():
            return HTTPUIAssetResponse(
                status=HTTPStatus.OK,
                content_type="text/html; charset=utf-8",
                body=_read_binary(index_path),
            )
        return None

    prefix = "/ui/"
    if normalized.startswith(prefix):
        asset_rel = normalized[len(prefix):]
        # Prevent path traversal
        if ".." in asset_rel or asset_rel.startswith("/"):
            return None
        candidate = _VUE_DIST_DIR / asset_rel
        if candidate.is_file():
            return HTTPUIAssetResponse(
                status=HTTPStatus.OK,
                content_type=_guess_mime(asset_rel),
                body=_read_binary(candidate),
            )

    candidate = _VUE_DIST_DIR / normalized.lstrip("/")
    if candidate.is_file():
        return HTTPUIAssetResponse(
            status=HTTPStatus.OK,
            content_type=_guess_mime(normalized),
            body=_read_binary(candidate),
        )

    return None


def resolve_http_ui_asset(path: str) -> Optional[HTTPUIAssetResponse]:
    normalized = str(path or "").strip() or "/"

    # Try Vue build output first
    vue_asset = _serve_vue_file(normalized)
    if vue_asset is not None:
        return vue_asset

    # Fallback to legacy assets
    if normalized == "/":
        return HTTPUIAssetResponse(
            status=HTTPStatus.OK,
            content_type="text/html; charset=utf-8",
            body=_render_index_html(),
        )
    if normalized == "/ui/app.css":
        return HTTPUIAssetResponse(
            status=HTTPStatus.OK,
            content_type="text/css; charset=utf-8",
            body=_read_binary(_ASSET_DIR / "app.css"),
        )
    if normalized == "/ui/app.js":
        return HTTPUIAssetResponse(
            status=HTTPStatus.OK,
            content_type="application/javascript; charset=utf-8",
            body=_read_binary(_ASSET_DIR / "app.js"),
        )
    if normalized == "/ui/healthz":
        payload = {
            "ok": True,
            "service": "overstats-http-ui",
            "module_count": len(get_http_ui_module_specs()),
            "root_path": "/",
        }
        return HTTPUIAssetResponse(
            status=HTTPStatus.OK,
            content_type="application/json; charset=utf-8",
            body=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        )
    return None


def _render_index_html() -> bytes:
    bootstrap_json = json.dumps(get_http_ui_bootstrap_payload(), ensure_ascii=False).replace("<", "\\u003c")
    bootstrap_script = (
        "<script>"
        "window.__OVERSTATS_UI_BOOTSTRAP__ = "
        f"{bootstrap_json};"
        "</script>"
    )
    html_text = (_ASSET_DIR / "index.html").read_text(encoding="utf-8")
    replaced = html_text.replace("__OVERSTATS_UI_BOOTSTRAP__", bootstrap_script)
    return replaced.encode("utf-8")
