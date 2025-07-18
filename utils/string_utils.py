from typing import Optional


def parse_text(value: Optional[str]) -> Optional[str]:
    return value.strip().lower() if value and value.strip() else None

def parse_float(raw: Optional[str]) -> Optional[float]:
    if not raw:
        return None
    try:
        return float(raw)
    except (ValueError, TypeError):
        return None