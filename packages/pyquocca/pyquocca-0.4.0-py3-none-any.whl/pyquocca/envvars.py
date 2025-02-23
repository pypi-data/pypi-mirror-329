import re

_NAME_TO_ENV = re.compile(r"[^A-Z0-9_]")


def to_env_var(s: str):
    return _NAME_TO_ENV.sub("", s.upper().replace("-", "_"))
