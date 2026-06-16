from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import yaml

from . import config


# ---------------------------------------------------------------------------
# config.yaml override – the single source of secrets
# ---------------------------------------------------------------------------

def _load_yaml_overrides() -> Dict[str, Any]:
    """Load ``config.yaml`` from the project root (parent of the config package)."""
    yaml_path = Path(__file__).resolve().parents[2] / "config.yaml"
    if not yaml_path.is_file():
        return {}
    try:
        with open(yaml_path, "r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh) or {}
    except Exception:
        return {}
    if not isinstance(raw, dict):
        return {}
    return raw


_YAML = _load_yaml_overrides()


def _yaml_value(key: str, default: Any = None) -> Any:
    """Read a flat key from config.yaml (case-sensitive)."""
    return _YAML.get(key, default)


# ---------------------------------------------------------------------------
# env helpers
# ---------------------------------------------------------------------------

def _read_bool_env(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _read_int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return int(default)
    return int(raw)


def _as_non_empty_string(value: Any, field_name: str) -> str:
    normalized = str(value or "").strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty.")
    return normalized


def _as_positive_int(value: Any, field_name: str) -> int:
    try:
        normalized = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be an integer.") from exc
    if normalized <= 0:
        raise ValueError(f"{field_name} must be greater than 0.")
    return normalized


def _as_positive_float(value: Any, field_name: str) -> float:
    try:
        normalized = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a number.") from exc
    if normalized <= 0:
        raise ValueError(f"{field_name} must be greater than 0.")
    return normalized


def _normalize_proxy_pool(raw_value: Any) -> Tuple[Optional[str], ...]:
    if raw_value is None:
        return (None,)
    if not isinstance(raw_value, (list, tuple)):
        raise ValueError("DASHEN_NETEASE_PROXIES must be a list or tuple.")

    normalized = []
    for item in raw_value:
        proxy = str(item or "").strip()
        normalized.append(proxy or None)
    return tuple(normalized or [None])


# ---------------------------------------------------------------------------
# config dataclasses
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class APIConfig:
    host: str
    port: int
    use_stream_response: bool
    dashen_max_concurrent_requests: int
    dashen_max_accepted_requests: int = 4


@dataclass(frozen=True)
class DashenCredentialConfig:
    name: str
    role_id: int
    token: str
    dts: int
    server: int


@dataclass(frozen=True)
class DashenClientConfig:
    accounts: Tuple[DashenCredentialConfig, ...]
    bigdata_dts: int
    account_max_requests_per_second: int
    account_rate_limit_window_seconds: float
    client_type: str
    origin: str
    referer: str
    user_agent: str
    account_failure_cooldown_seconds: int
    international_proxy: str
    netease_proxies: Tuple[Optional[str], ...]
    ow_esports_api_key: str


# ---------------------------------------------------------------------------
# account normalisation (config.py → overridden by config.yaml)
# ---------------------------------------------------------------------------

def _normalize_accounts() -> Tuple[DashenCredentialConfig, ...]:
    # Prefer config.yaml roleid / token when present, otherwise fall back to config.py
    yaml_role_id = _yaml_value("roleid")
    yaml_token = _yaml_value("token")

    raw_accounts = getattr(config, "DASHEN_ACCOUNTS", [])
    if not isinstance(raw_accounts, (list, tuple)):
        raise ValueError("DASHEN_ACCOUNTS must be a list or tuple.")
    if not raw_accounts:
        raise ValueError("DASHEN_ACCOUNTS must contain at least one account.")

    default_dts = _as_positive_int(getattr(config, "DASHEN_DTS", 2026), "DASHEN_DTS")
    default_server = _as_positive_int(getattr(config, "DASHEN_SERVER", 1), "DASHEN_SERVER")

    normalized_accounts = []
    used_names = set()

    for index, raw_account in enumerate(raw_accounts, start=1):
        if not isinstance(raw_account, dict):
            raise ValueError(f"DASHEN_ACCOUNTS[{index - 1}] must be a dict.")

        name = str(raw_account.get("name") or f"account-{index}").strip()
        if not name:
            name = f"account-{index}"
        if name in used_names:
            raise ValueError(f"DASHEN_ACCOUNTS contains duplicate account name: {name}")
        used_names.add(name)

        # config.yaml overrides for the first account
        if index == 1 and yaml_role_id is not None:
            try:
                role_id = int(yaml_role_id)
            except (TypeError, ValueError):
                role_id = _as_positive_int(raw_account.get("role_id"), f"DASHEN_ACCOUNTS[{index - 1}].role_id")
        else:
            role_id = _as_positive_int(raw_account.get("role_id"), f"DASHEN_ACCOUNTS[{index - 1}].role_id")

        if index == 1 and yaml_token is not None:
            token = _as_non_empty_string(yaml_token, f"DASHEN_ACCOUNTS[{index - 1}].token")
        else:
            token = _as_non_empty_string(raw_account.get("token"), f"DASHEN_ACCOUNTS[{index - 1}].token")

        normalized_accounts.append(
            DashenCredentialConfig(
                name=name,
                role_id=role_id,
                token=token,
                dts=default_dts,
                server=default_server,
            )
        )

    return tuple(normalized_accounts)


def _default_dashen_max_accepted_requests() -> int:
    raw_accounts = getattr(config, "DASHEN_ACCOUNTS", [])
    if not isinstance(raw_accounts, (list, tuple)):
        return 4
    return max(1, len(raw_accounts) * 4)


# ---------------------------------------------------------------------------
# public getters
# ---------------------------------------------------------------------------

def get_api_config() -> APIConfig:
    return APIConfig(
        host=os.getenv("OVERSTATS_API_HOST", config.API_HOST),
        port=int(os.getenv("OVERSTATS_API_PORT", str(config.API_PORT))),
        use_stream_response=_read_bool_env(
            "OVERSTATS_USE_STREAM_RESPONSE",
            config.USE_STREAM_RESPONSE,
        ),
        dashen_max_concurrent_requests=_read_int_env(
            "OVERSTATS_DASHEN_MAX_CONCURRENT_REQUESTS",
            getattr(config, "DASHEN_MAX_CONCURRENT_REQUESTS", 2),
        ),
        dashen_max_accepted_requests=max(
            1,
            _read_int_env(
                "OVERSTATS_DASHEN_MAX_ACCEPTED_REQUESTS",
                getattr(
                    config,
                    "DASHEN_MAX_ACCEPTED_REQUESTS",
                    _default_dashen_max_accepted_requests(),
                ),
            ),
        ),
    )


# Map config.yaml flat keys → config.py attribute names.
# When a YAML key is present its value is injected into the config module
# so that every ``getattr(config, "ATTR")`` call sees the secret.
_YAML_OVERRIDE_MAP: Dict[str, str] = {
    "analysis_api_key":    "ANALYSIS_API_KEY",
    "analysis_base_url":   "ANALYSIS_BASE_URL",
    "analysis_proxy":      "ANALYSIS_PROXY",
    "ow_esports_api_key":  "OW_ESPORTS_API_KEY",
}

for _yaml_key, _attr_name in _YAML_OVERRIDE_MAP.items():
    _val = _yaml_value(_yaml_key)
    if _val is not None:
        setattr(config, _attr_name, _val)


def get_dashen_client_config() -> DashenClientConfig:
    accounts = _normalize_accounts()
    cooldown_seconds = _as_positive_int(
        getattr(config, "DASHEN_ACCOUNT_FAILURE_COOLDOWN_SECONDS", 60),
        "DASHEN_ACCOUNT_FAILURE_COOLDOWN_SECONDS",
    )
    return DashenClientConfig(
        accounts=accounts,
        bigdata_dts=_as_positive_int(
            getattr(config, "DASHEN_BIGDATA_DTS", getattr(config, "DASHEN_DTS", accounts[0].dts)),
            "DASHEN_BIGDATA_DTS",
        ),
        account_max_requests_per_second=_as_positive_int(
            getattr(config, "DASHEN_ACCOUNT_MAX_REQUESTS_PER_SECOND", 5),
            "DASHEN_ACCOUNT_MAX_REQUESTS_PER_SECOND",
        ),
        account_rate_limit_window_seconds=_as_positive_float(
            getattr(config, "DASHEN_ACCOUNT_RATE_LIMIT_WINDOW_SECONDS", 1.0),
            "DASHEN_ACCOUNT_RATE_LIMIT_WINDOW_SECONDS",
        ),
        client_type=_as_non_empty_string(
            getattr(config, "DASHEN_CLIENT_TYPE", "60"),
            "DASHEN_CLIENT_TYPE",
        ),
        origin=_as_non_empty_string(
            getattr(config, "DASHEN_ORIGIN", "https://act.ds.163.com"),
            "DASHEN_ORIGIN",
        ),
        referer=_as_non_empty_string(
            getattr(config, "DASHEN_REFERER", "https://act.ds.163.com/"),
            "DASHEN_REFERER",
        ),
        user_agent=_as_non_empty_string(
            getattr(config, "DASHEN_USER_AGENT", ""),
            "DASHEN_USER_AGENT",
        ),
        account_failure_cooldown_seconds=cooldown_seconds,
        international_proxy=str(getattr(config, "DASHEN_INTERNATIONAL_PROXY", "") or "").strip(),
        netease_proxies=_normalize_proxy_pool(getattr(config, "DASHEN_NETEASE_PROXIES", [None])),
        ow_esports_api_key=str(getattr(config, "OW_ESPORTS_API_KEY", "") or "").strip(),
    )
