# api/prediction.py
import os
import requests
from typing import Dict, Tuple

DEFAULT_SCHEME = os.getenv("BE_APP_SCHEME", "http")
DEFAULT_HOST   = os.getenv("BE_APP_HOST",   "127.0.0.1")
DEFAULT_PORT   = os.getenv("BE_APP_PORT",   "8080")
TIMEOUT_SECS   = float(os.getenv("BE_TIMEOUT", "10"))

def build_base_url(host: str = None, port: str = None) -> str:
    host   = (host   or DEFAULT_HOST).strip()
    port   = (port   or DEFAULT_PORT).strip()
    return f"http://{host}" if port in ("80", "", None) else f"http://{host}:{port}"

def healthcheck(base_url: str) -> Tuple[bool, str]:
    """Cek root endpoint untuk memastikan backend up."""
    try:
        r = requests.get(f"{base_url}/", timeout=TIMEOUT_SECS)
        if r.ok:
            return True, "Backend reachable"
        return False, f"Healthcheck failed: {r.status_code}"
    except Exception as e:
        return False, f"Healthcheck error: {e}"

def get_pred(data: Dict, base_url: str = None) -> Tuple[str, str]:
    base = base_url or build_base_url()
    url = f"{base}/predict"
    try:
        r = requests.post(url, json=data, timeout=TIMEOUT_SECS)
        r.raise_for_status()
        payload = r.json()
        message = payload.get("message", "")
        result  = payload.get("result", [])
        # result bisa list enum/string; ambil elemen pertama kalau ada
        result_str = ", ".join(result) if isinstance(result, list) else str(result)
        return message, result_str
    except requests.HTTPError as he:
        raise RuntimeError(f"HTTP {r.status_code} calling {url}: {r.text}") from he
    except Exception as e:
        raise RuntimeError(f"Gagal memanggil {url}: {e}") from e