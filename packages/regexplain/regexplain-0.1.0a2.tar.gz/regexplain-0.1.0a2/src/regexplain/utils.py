_FLAGS_RE2STR = {
    "ascii_": "a",
    "ignorecase": "i",
    "locale": "L",
    "multiline": "m",
    "dotall": "s",
    "unicode": "u",
    "verbose": "x",
    "debug": ""
}

_FLAGS_STR2RE = {v: k for k, v in _FLAGS_RE2STR.items()}
