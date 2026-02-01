import re

def convert_kr_code(user_code: str) -> str:
    """
    Convert user input like 'kr005930', 'kr:005930', or '005930.KS' into a yfinance-compatible ticker like '005930.KS' or '005930.KQ'.
    Default mapping is to .KS (KOSPI) when no suffix is provided.

    Examples:
    - kr005930 -> 005930.KS
    - kr:035720 -> 035720.KS
    - 035720.KQ -> 035720.KQ
    """
    code = user_code.strip()
    # Remove kr prefix variants
    if code.lower().startswith('kr:'):
        code = code[3:]
    elif code.lower().startswith('kr'):
        code = code[2:]
    code = code.strip()

    # If already a 6-digit with suffix like .KS or .KQ, normalize
    m = re.match(r'^(?P<num>\d{1,6})\.(?P<suf>KS|KQ)$', code, re.IGNORECASE)
    if m:
        num = m.group('num').zfill(6)
        suf = m.group('suf').upper()
        return f"{num}.{suf}"

    # If it's already exactly 6 digits, assume .KS by default
    if re.match(r'^\d{6}$', code):
        return f"{code}.KS"

    # Strip non-digits and pad to 6 digits
    digits = re.sub(r'\D', '', code)
    if not digits:
        # Fallback: return original uppercased
        return user_code.upper()
    digits = digits.zfill(6)
    return f"{digits}.KS"

def is_kr_code(user_code: str) -> bool:
    """Return True if the input looks like a Korea stock identifier we should convert.

    Recognizes prefixes like 'kr', 'kr:' (case-insensitive), or a 6-digit code with .KS/.KQ suffix.
    """
    c = user_code.strip()
    if not c:
        return False
    if c.lower().startswith('kr') or c.lower().startswith('kr:'):
        return True
    if re.match(r'^\d{6}\.(ks|kq)$', c, re.IGNORECASE):
        return True
    return False
