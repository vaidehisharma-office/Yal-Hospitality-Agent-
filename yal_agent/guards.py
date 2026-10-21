MAX_CHARS = 2000


class InputRejected(ValueError):
    """Raised when input is unusable. No model call is made."""


def check_input(text) -> str:
    if not isinstance(text, str):
        raise InputRejected("not_a_string")
    cleaned = text.strip()
    if not cleaned:
        raise InputRejected("empty")
    if len(cleaned) > MAX_CHARS:
        raise InputRejected("too_long")
    return cleaned