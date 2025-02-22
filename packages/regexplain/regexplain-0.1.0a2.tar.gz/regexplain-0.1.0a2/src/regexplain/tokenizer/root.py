import re
from typing import Self
from . import grouped, non_grouped


class RegexTokenizer(grouped.MiscGroupRegexToken):
    """
    Every regex pattern must start as an object of this class, this is the
    most fundamental token. Every token in the input pattern is a sub-token of
    the root token. Since this is derived from group token, the full pattern
    is available in text form with the 'value' property.
    """

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        instance._parse_for_tokens.insert(  # NOQA
            0, non_grouped.UnpairedParenthesisRegexToken
        )
        return instance

    def __init__(self,
                 pattern: str,
                 flags: re.RegexFlag = re.NOFLAG):
        self._pattern = pattern

        self._ascii = re.ASCII in flags
        self._ignorecase = re.IGNORECASE in flags
        self._locale = re.LOCALE in flags
        self._multiline = re.MULTILINE in flags
        self._dotall = re.DOTALL in flags
        self._verbose = re.VERBOSE in flags
        self._debug = re.DEBUG in flags

        super().__init__(opening="", start_pos=0, super_token=None)

        self._closed = True  # root token is always considered closed

    @property
    def id(self) -> bool | None:
        return None

    @property
    def index(self) -> int | None:
        return None

    @property
    def is_last_sibling(self) -> bool | None:
        return None

    @property
    def level(self) -> int:
        return 0

    @property
    def pattern(self) -> str:
        return self._pattern

    @property
    def root_token(self) -> type[Self]:
        return self

    @property
    def summary(self) -> str:
        return ""

    def get_sibling(self, *args, **kwargs) -> type[Self] | None:
        raise NotImplementedError("Root token cannot have a sibling")
