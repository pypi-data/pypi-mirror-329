from __future__ import annotations
import re
from . import base, grouped


class NonGroupedRegexToken(base.BaseRegexToken):
    """
    This is a foundational token type. Subclasses have no groups, just a value.
    Derived token types can define additional attributes extracted from the
    value.
    """

    def __init__(self,
                 value: str,
                 start_pos: int,
                 super_token: grouped.GroupedRegexToken):
        super().__init__(start_pos=start_pos,
                         super_token=super_token)

        self._value = value

    def __str__(self) -> str:
        return self._value

    @property
    def summary(self) -> str:
        return ""

    @property
    def value(self) -> str:
        return self._value


class BoundedRegexToken(NonGroupedRegexToken):
    _OPEN_CLOSE_PAIRS = {"(": ")"}

    def __init__(self,
                 value: str,
                 start_pos: int,
                 super_token: grouped.GroupedRegexToken):
        super().__init__(value=value,
                         start_pos=start_pos,
                         super_token=super_token)

        re_match = self._TOKEN_PATTERN.match(value)
        self._closed = bool(re_match.group("closing"))
        if not self._closed:
            opening = re_match.group("opening")
            self._err(f"Missing {self._OPEN_CLOSE_PAIRS[opening[0]]}")

    @property
    def closed(self) -> bool:
        return self._closed


class UnboundedRegexToken(NonGroupedRegexToken):
    pass


class RangeRegexToken(UnboundedRegexToken):
    def __init__(self,
                 super_token: grouped.GroupedRegexToken | None,
                 from_token: UnboundedRegexToken,
                 hyphen_token: LiteralRegexToken,
                 to_token: UnboundedRegexToken):
        super().__init__(value=f"{from_token.value}"
                               f"{hyphen_token.value}"
                               f"{to_token.value}",
                         start_pos=from_token.start_pos,
                         super_token=super_token)

        self._from_token = from_token
        self._hyphen_token = hyphen_token
        self._to_token = to_token

        if not isinstance(self._from_token, LiteralRegexToken):
            self._err(f"Bad 'from' character '{self._from_token.value}'")
        if not isinstance(self._to_token, LiteralRegexToken):
            self._err(f"Bad 'to' character '{self._to_token.value}'")

    @property
    def from_token(self) -> UnboundedRegexToken:
        return self._from_token

    @property
    def hyphen_token(self) -> LiteralRegexToken:
        return self._hyphen_token

    @property
    def to_token(self) -> UnboundedRegexToken:
        return self._to_token

    def _merge_sub_tokens(self, **kwargs) -> None:
        pass

    def _parse_pattern(self) -> None:
        pass

    @property
    def summary(self) -> str:
        return (f"Matches a character in the range '{self._from_token.value}'"
                f" to '{self._to_token.value}' ({self.case_sensitivity})")


class AnchorRegexToken(UnboundedRegexToken):
    _TOKEN_PATTERN = re.compile(r"[\^$]", re.NOFLAG)
    _ANCHOR_DESCRIPTION = {
        "^": ("Beginning", "Matches beginning of the string, or beginning of a"
                           " line if multiline flag is active"),
        "$": ("End", "Matches end of the string, or end of a line if multiline"
                     " flag is active")
    }

    def __init__(self,
                 value: str,
                 start_pos: int,
                 super_token: grouped.GroupedRegexToken):
        super().__init__(value=value,
                         start_pos=start_pos,
                         super_token=super_token)

        self._anchor_class, self._anchor_class_desc = \
            self._ANCHOR_DESCRIPTION[value]

    @property
    def label(self) -> str:
        return f"{self._friendly_type}:{self._anchor_class}"

    @property
    def summary(self) -> str:
        return self._anchor_class_desc


class CharClassRegexToken(UnboundedRegexToken):
    CHAR_CLASS_DESCRIPTION = {
        r"\\A": ("Beginning of String",
                 "Matches beginning of the string"),
        r"\\Z": ("End of String",
                 "Matches end of the string"),
        r"\\b": ("Word Boundary",
                 "Matches an empty string at the beginning or the end of word"),
        r"\\B": ("Not Word Boundary",
                 "Matches an empty string not at the beginning or the end of a"
                 " word"),
        r"\\d": ("Digit",
                 "Matches any digit character 0-9"),
        r"\\D": ("Non-Digit",
                 "Matches any character that is not a digit 0-9"),
        r"\\w": ("Word",
                 "Matches any word character (alphanumeric and underscore)"),
        r"\\W": ("Non-Word",
                 "Matches any character that is not a word character"
                 " (alphanumeric and underscore)"),
        r"\\s": ("Whitespace",
                 "Matches any whitespace character (space, tab, line-break"),
        r"\\S": ("Non-Whitespace",
                 "Matches any character that is not a whitespace character"
                 " (space, tab, line-break)")
    }
    _TOKEN_PATTERN = re.compile(
        f"(?P<char_class>{'|'.join(CHAR_CLASS_DESCRIPTION.keys())})",
        re.NOFLAG
    )

    def __init__(self,
                 value: str,
                 start_pos: int,
                 super_token: grouped.GroupedRegexToken):
        super().__init__(value=value,
                         start_pos=start_pos,
                         super_token=super_token)

        re_match = self._TOKEN_PATTERN.match(value)
        self._char_class, self._char_class_desc = self.CHAR_CLASS_DESCRIPTION[
            re_match.group("char_class").replace("\\", "\\\\")
        ]

    @property
    def label(self) -> str:
        return f"{self._friendly_type}:{self._char_class}"

    @property
    def summary(self) -> str:
        return self._char_class_desc


class CommentRegexToken(BoundedRegexToken):
    """
    The comment token.
    """
    _TOKEN_PATTERN = re.compile(
        r"(?P<opening>\(\?#)(?:.*?(?<!\\)(?P<closing>\))|.*)",
        re.NOFLAG
    )

    @property
    def summary(self) -> str:
        return ("Treats as a comment, ignores and bypasses when looking for a"
                " match")


class EscapedCharRegexToken(UnboundedRegexToken):
    _ESC_CHAR_DESCRIPTION = {
        r"\\\^": "Caret",
        r"\\\$": "Dollar",
        r"\\\.": "Dot",
        r"\\\\": "Backslash",
        r"\\-": "Hyphen",
        r"\\\*": "Asterisk",
        r"\\\+": "Plus",
        r"\\\?": "Question Mark",
        r"\\\|": "Pipe",
        r"\\x1B": "Escape",

        r"\\a": "Alert",
        r"\\b": "Backspace",
        r"\\t": "Tab",
        r"\\v": "Vertical Tab",
        r"\\f": "Form Feed",
        r"\\n": "line Feed",  # aka unix_line_break
        r"\\r": "Carriage Return",
        # vr"\\r\\n": "Carriage Return Line Feed",  # aka windows_line_break

        r"\\'": "Single Quote",
        r'\\"': "Double Quote",
        r"\\:": "Colon",
        r"\\,": "Comma",
        r"\\=": "Equal",
        r"\\!": "Exclamation Mark",

        r"\\\(": "Opening Parentheses",
        r"\\\)": "Closing Parentheses",
        r"\\\[": "Opening Square Bracket",
        r"\\]": "Closing Square Bracket",
        r"\\{": "Opening Curly Bracket",
        r"\\}": "Closing Curly Bracket",
        r"\\<": "Less Than Symbol",
        r"\\>": "Greater Than Symbol",
    }
    _TOKEN_PATTERN = re.compile(
        f"(?P<escaped_char>{'|'.join(_ESC_CHAR_DESCRIPTION.keys())})",
        re.NOFLAG
    )
    _KEY_SUBSTITUTE_PATTERN = re.compile(r"([\\\[.()*+?^$|])")

    def __init__(self,
                 value: str,
                 start_pos: int,
                 super_token: grouped.GroupedRegexToken):
        super().__init__(value=value,
                         start_pos=start_pos,
                         super_token=super_token)

        self._escaped_char_class = self._ESC_CHAR_DESCRIPTION[
            self._KEY_SUBSTITUTE_PATTERN.sub(r"\\\1", self._value)
        ]

    @property
    def label(self) -> str:
        return f"{self._friendly_type}:{self._escaped_char_class}"

    @property
    def summary(self) -> str:
        return f"Matches escaped character for {self._escaped_char_class}"


class GroupIdBackrefRegexToken(UnboundedRegexToken):
    _TOKEN_PATTERN = re.compile(r"\\(?P<backref_group_id>[1-9][0-9]?)(?![0-9])",
                                re.NOFLAG)

    def __init__(self,
                 value: str,
                 start_pos: int,
                 super_token: grouped.GroupedRegexToken):
        super().__init__(value=value,
                         start_pos=start_pos,
                         super_token=super_token)

        re_match = self._TOKEN_PATTERN.match(value)
        self._group_id = int(re_match.group("backref_group_id"))
        if not abs(self._group_id) in self.backref_group_ids:
            self._err(f"Group id '{self._group_id}' is undefined or not closed"
                      f" yet at this position")

    @property
    def summary(self) -> str:
        return f"Matches result of the capturing group #{self._group_id}"


class GroupNameBackrefRegexToken(BoundedRegexToken):
    _TOKEN_PATTERN = re.compile(r"(?P<opening>\(\?P=)"
                                r"(?P<backref_group_name>"
                                r"(.*?(?<!\\)(?=\)))"
                                r"|.*"
                                r")"
                                r"(?<!\\)(?P<closing>\))", re.NOFLAG)

    def __init__(self,
                 value: str,
                 start_pos: int,
                 super_token: grouped.GroupedRegexToken):
        super().__init__(value=value,
                         start_pos=start_pos,
                         super_token=super_token)

        re_match = self._TOKEN_PATTERN.match(value)
        self._group_name = re_match.group("backref_group_name")
        if self._group_name not in self.backref_group_names:
            self._err(f"Group name '{self._group_name}' is undefined or not"
                      f" closed yet")

    @property
    def summary(self) -> str:
        return f"Matches result of the named group '{self._group_name}'"


class HexValueRegexToken(UnboundedRegexToken):
    r"""
    Token type for hex-valued tokens of pattern '\xnn'(where n=0-9A-F).
    """
    _TOKEN_PATTERN = re.compile(r"\\x(?P<hex_value>[0-9A-F]{0,2})",
                                re.IGNORECASE)

    def __init__(self,
                 value: str,
                 start_pos: int,
                 super_token: grouped.GroupedRegexToken):
        super().__init__(value=value,
                         start_pos=start_pos,
                         super_token=super_token)

        re_match = self._TOKEN_PATTERN.match(value)
        self._hex_value = re_match.group("hex_value")
        if len(self._hex_value) < 2:
            self._err(f"Incomplete hex value '\\x{self._hex_value}'")

    @property
    def summary(self) -> str:
        return f"Matches character with hex value '\\x{self._hex_value}'"


class LiteralRegexToken(UnboundedRegexToken):
    _TOKEN_PATTERN = re.compile(r".", re.NOFLAG)

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value) -> None:
        self._value = value

    @property
    def summary(self) -> str:
        summary = f"Matches a single character from the list '{self._value}'" \
            if isinstance(self.super_token, grouped.CharSetRegexToken) \
            else f"Matches character string '{self._value}' literally"
        return f"{summary} ({self.case_sensitivity})"


class OctalValueRegexToken(UnboundedRegexToken):
    r"""
    Token type for octal-valued tokens of pattern '\ooo'(where o=0-7).
    """
    _TOKEN_PATTERN = re.compile(r"\\(?P<octal_value>(0[0-7]{0,2}|[0-7]{3}))",
                                re.NOFLAG)

    def __init__(self,
                 value: str,
                 start_pos: int,
                 super_token: grouped.GroupedRegexToken):
        super().__init__(value=value,
                         start_pos=start_pos,
                         super_token=super_token)

        re_match = self._TOKEN_PATTERN.match(value)
        self._octal_value = re_match.group("octal_value")
        if int(self._octal_value, 8) > 255:
            self._err(f"Octal value '\\{self._octal_value}' out of range"
                      f" 0-0o377")

    @property
    def summary(self) -> str:
        return f"Matches character with octal value '\\{self._octal_value}'"


class OrRegexToken(UnboundedRegexToken):
    """
    The '|' token.
    """
    _TOKEN_PATTERN = re.compile(r"\|", re.NOFLAG)

    @property
    def summary(self) -> str:
        return f"Matches expression before or after '{self._value}'"


class QuantifierRegexToken(UnboundedRegexToken):
    """
    The repeat or quantifier token of the forms '*', '+', '?', '{,}', '{m,}',
    '{,n}' and '{m,n}'. This may be followed by lazy '?' or possessive '+'
    mode.
    """
    _TOKEN_PATTERN = re.compile(
        r"(?:"  # non-capturing group
        r"[*+?]"  # char * or + or ?
        r"|"  # or
        r"{"  # literal {
        r"(?P<repeat_count>\d)"  # named group with 1 digit
        r"*"  # group repeats 0 or more times
        r"(?(repeat_count)"  # if named group exists (at least 1 digit present)
        r",?"  # optional ,
        r"|"  # else
        r","  # mandatory ,
        r")"  # end-if
        r"\d*"  # digits appear 0 or more times
        r"}"  # literal }
        r")"  # end of non-capturing group
        r"[?+]?",  # lazy '?' or possessive '+' mode
        re.NOFLAG
    )
    re_parse = re.compile(
        r"(?:(?P<quantifier>[*+?])|"
        r"{(?P<min_times>\d+)(?P<comma>,?)(?P<max_times>\d*)})"
        r"(?P<mode>[?+]?)",
        re.NOFLAG
    )

    def __init__(self,
                 value: str,
                 start_pos: int,
                 super_token: grouped.GroupedRegexToken):
        super().__init__(value=value,
                         start_pos=start_pos,
                         super_token=super_token)

        re_match = self.re_parse.match(value)
        quantifier = re_match.group("quantifier")
        if quantifier == "*":
            self._min_times = 0
            self._max_times = float("inf")
        elif quantifier == "+":
            self._min_times = 1
            self._max_times = float("inf")
        elif quantifier == "?":
            self._min_times = 0
            self._max_times = 1
        else:
            min_times = re_match.group("min_times")
            comma = re_match.group("comma")
            max_times = re_match.group("max_times")
            self._min_times = int(min_times) \
                if min_times \
                else 0
            self._max_times = int(max_times) \
                if comma and max_times \
                else float("inf") \
                if comma \
                else self._min_times

        mode = re_match.group("mode")
        self._mode = "lazy" \
            if mode == "?" \
            else "possessive" \
            if mode == "+" \
            else "greedy"

        self._finalize_token()

    @property
    def flags(self) -> re.RegexFlag | None:
        return None

    def _finalize_token(self) -> None:
        if self._min_times > self._max_times:
            self._err(f"Minimum repeat '{self._min_times}' greater than maximum"
                      f" repeat '{self._max_times}'")

        prev_sibling = self.get_sibling(-1)
        if prev_sibling is None:
            self._err("No preceding token")
        elif isinstance(prev_sibling, self.__class__):
            self._err("Preceding token cannot be a quantifier")

    @property
    def summary(self) -> str:
        if self._min_times > self._max_times:
            summary = "Matches repetitions of the preceding token"
        else:
            if self._min_times == self._max_times:
                summary = (f"Matches preceding token exactly {self._min_times}"
                           f" time(s)")
            else:
                max_times = "unlimited" if self._max_times == float("inf") \
                    else self._max_times
                summary = (f"Matches preceding token between {self._min_times}"
                           f" and {max_times} times")

        suffix = "" \
            if (self._min_times == self._max_times
                and not self._mode == "possessive") \
            else f" ({self._mode})"
        return f"{summary}{suffix}"


class UnicodeNamedCharRegexToken(UnboundedRegexToken):
    r"""
    Token type for \N{UNICODE NAME} tokens.
    Reference: https://www.unicode.org/charts/charindex.html
    Examples: CHECK MARK, HEAVY: ✔
              AIRPLANE: ✈
    """
    _TOKEN_PATTERN = re.compile(r"\\N{(?P<unicode_char_name>.*?)(?<!\\)}",
                                re.NOFLAG)

    def __init__(self,
                 value: str,
                 start_pos: int,
                 super_token: grouped.GroupedRegexToken):
        super().__init__(value=value,
                         start_pos=start_pos,
                         super_token=super_token)

        re_match = self._TOKEN_PATTERN.match(value)
        self._unicode_char_name = re_match.group("unicode_char_name")
        if not self._unicode_char_name:
            self._err("Missing unicode character name")

    @property
    def summary(self) -> str:
        return (f"Matches character with unicode character name"
                f" '{self._unicode_char_name}'")


class UnicodeValueRegexToken(UnboundedRegexToken):
    r"""
    Token type for unicode-valued tokens of pattern '\unnnn'(where n=0-9A-F).
    """
    _TOKEN_PATTERN = re.compile(r"\\u(?P<unicode_value>[0-9A-F]{0,4})",
                                re.IGNORECASE)

    def __init__(self,
                 value: str,
                 start_pos: int,
                 super_token: grouped.GroupedRegexToken):
        super().__init__(value=value,
                         start_pos=start_pos,
                         super_token=super_token)

        re_match = self._TOKEN_PATTERN.match(value)
        self._unicode_value = re_match.group("unicode_value")
        if len(self._unicode_value) < 4:
            self._err(f"Incomplete unicode value '\\u{self._unicode_value}'")

    @property
    def summary(self) -> str:
        return (f"Matches character with unicode value"
                f" '\\u{self._unicode_value}'")


class UnpairedParenthesisRegexToken(UnboundedRegexToken):
    """
    The '.' wildcard token.
    """
    _TOKEN_PATTERN = re.compile(r"\)", re.NOFLAG)

    @property
    def summary(self) -> str:
        return f"Unpaired parenthesis {self._value}"


class WildcardRegexToken(UnboundedRegexToken):
    """
    The '.' wildcard token.
    """
    _TOKEN_PATTERN = re.compile(r"\.", re.NOFLAG)

    @property
    def summary(self) -> str:
        return "Matches any character except line-break"


def _get_box_symbols(indent: str) -> tuple[str, str, str, str, str]:
    """
    :return:
      top_bound, bottom_bound, title_indent, body_indent, sub_token_indent
    """
    return ("  ┌──", "  └──", "──│ ", "  │ ", "  │") \
        if indent \
        else ("┌──", "└──", "│ ", "│ ", "│")
