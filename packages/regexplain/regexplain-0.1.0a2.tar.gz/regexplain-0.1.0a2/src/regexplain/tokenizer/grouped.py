from __future__ import annotations
import re
from typing import Self
from . import base, non_grouped
from ..utils import _FLAGS_STR2RE


class GroupedRegexToken(base.BaseRegexToken):
    """
    This is one of the foundational token types. This is the only token that
    helps build a token hierarchy. Any token that needs sub tokens, must be
    subclassed from this class, as the checks throughout the code is done on
    this.

    A grouped token has 3 main parts:
      sub-tokens: other tokens (may or may not be grouped tokens). These
                  sub-tokens are available in raw text form with the 'value'
                  property.
      opening: text that represents the starting of a group token, viz. 'C' for
               a simple capturing group, or '(?P<name>' for a named group, etc.
      closing: text that represents the ending of a group token, viz. ')'.
    """
    _OPEN_CLOSE_PAIRS = {
        "": "",
        "(": ")",
        "[": "]"
    }

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._parse_for_tokens = [
            non_grouped.AnchorRegexToken,
            AtomicGroupRegexToken,
            CapturingGroupRegexToken,
            non_grouped.CharClassRegexToken,
            CharSetRegexToken,
            non_grouped.CommentRegexToken,
            ConditionalGroupRegexToken,
            non_grouped.EscapedCharRegexToken,
            FlagModifierRegexToken,
            GlobalFlagsRegexToken,
            non_grouped.GroupIdBackrefRegexToken,
            non_grouped.GroupNameBackrefRegexToken,
            non_grouped.HexValueRegexToken,
            non_grouped.OctalValueRegexToken,
            non_grouped.OrRegexToken,
            non_grouped.QuantifierRegexToken,
            LookaroundGroupRegexToken,
            NamedGroupRegexToken,
            NonCapturingGroupRegexToken,
            non_grouped.UnicodeNamedCharRegexToken,
            non_grouped.UnicodeValueRegexToken,
            non_grouped.WildcardRegexToken,
            UnknownGroupRegexToken,
            non_grouped.LiteralRegexToken
        ]
        return instance

    def __init__(self,
                 opening: str,
                 start_pos: int,
                 super_token: GroupedRegexToken | None):
        super().__init__(start_pos=start_pos,
                         super_token=super_token)
        self._pre_messages = {"x": [], "i": [], "w": [], "e": []}

        self._sub_tokens = ()
        self._opening = opening
        self._closing = ""
        self._close_with = self._OPEN_CLOSE_PAIRS[self._opening[0:1]]
        self._closed = not opening

        self._parse_pattern()

    def __str__(self) -> str:
        return f"{self._opening}{self.value}{self._closing}"

    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def inner_length(self) -> int:
        return self.length - len(self._opening) - len(self._closing)

    @property
    def inner_start_pos(self) -> int:
        return self._start_pos + len(self._opening)

    @property
    def inner_span(self) -> tuple[int, int]:
        return (self.inner_start_pos,
                self.inner_start_pos + self.inner_length)

    @property
    def sub_tokens(self) -> tuple:
        return self._sub_tokens

    @property
    def tokens(self) -> list[base.BaseRegexToken]:
        return self.walk_down_token(
            stop_at_token=None,
            skip_stop_token_lineage=False,
            skip_start_token=True,
            skip_stop_token=True)[0]

    @property
    def summary(self) -> str:
        return "Grouped token"

    @property
    def value(self) -> str:
        sub_tokens_to_str = ""
        for sub_token in self._sub_tokens:
            sub_tokens_to_str += str(sub_token)
        return sub_tokens_to_str

    def append_sub_tokens(self, *tokens: type[Self]) -> None:
        for token in tokens:
            if not id(token._super_token) == id(self):
                token._super_token = self
            self._sub_tokens = self._sub_tokens + (token,)

    def walk_down_token(
            self,
            stop_at_token: int | type[Self] | None = None,
            skip_stop_token_lineage: bool = False,
            skip_start_token: bool = False,
            skip_stop_token: bool = True
    ) -> tuple[list, bool]:
        """
        Walks down the token and collects all sub_tokens (including itself).
        Example:
          self:
          ├── sub_token_0
          ├── sub_token_1
          │   ├── sub_token10
          │   ├── sub_token11
          │   └── sub_token12
          └── sub_token_2
              └── sub_token20

          * root_token.walk_down_token(None, False|True) retrieves:
            [root_token, sub_token0, sub_token1, sub_token10, sub_token11,
             sub_token12, sub_token2, sub_token20]
          * root_token.walk_down_token(sub_token11, False) retrieves:
            [root_token, sub_token0, sub_token1, sub_token10]
          * root_token.walk_down_token(sub_token11, True) retrieves:
            [sub_token0, sub_token10]
        """
        tokens_list = []
        stop_token_reached = False

        stop_at_token_id = id(stop_at_token) \
            if isinstance(stop_at_token, base.BaseRegexToken) \
            else stop_at_token

        if id(self) == stop_at_token_id:
            stop_token_reached = True
            if not skip_stop_token:
                tokens_list.append(self)
        else:
            for sub_token in self.sub_tokens:
                if id(sub_token) == stop_at_token_id:
                    stop_token_reached = True
                    if not skip_stop_token:
                        tokens_list.append(sub_token)
                    break

                if isinstance(sub_token, GroupedRegexToken):
                    sub_tokens_list, stop_token_reached = \
                        sub_token.walk_down_token(
                            stop_at_token=stop_at_token,
                            skip_stop_token_lineage=skip_stop_token_lineage,
                            skip_start_token=False,
                            skip_stop_token=skip_stop_token)
                    tokens_list.extend(sub_tokens_list)
                    if stop_token_reached:
                        break
                else:
                    tokens_list.append(sub_token)

            if not ((stop_token_reached and skip_stop_token_lineage)
                    or skip_start_token):
                tokens_list.insert(0, self)

        return (tokens_list,
                stop_token_reached)

    def _count_sub_token_of_type(
            self,
            sub_token_type: type[base.BaseRegexToken]
    ) -> int:
        count = 0
        for sub_token in self._sub_tokens:
            if isinstance(sub_token, sub_token_type):
                count += 1
        return count

    def _merge_sub_tokens(self, sub_token_pos: int = 0) -> None:
        """
        Merges consecutive LiteralRegexToken sub_tokens if the next token is not
        QuantifierRegexToken.
        """
        total_sub_tokens = len(self._sub_tokens)
        remaining_sub_tokens = total_sub_tokens - sub_token_pos

        if remaining_sub_tokens >= 2:
            merge_to_char_0_1 = False
            sub_token_0 = self._sub_tokens[sub_token_pos]
            sub_token_1 = self._sub_tokens[sub_token_pos + 1]
            if (isinstance(sub_token_0, non_grouped.LiteralRegexToken)
                    and isinstance(sub_token_1, non_grouped.LiteralRegexToken)):
                if remaining_sub_tokens == 2:
                    merge_to_char_0_1 = True
                else:
                    sub_token_2 = self._sub_tokens[sub_token_pos + 2]
                    if not isinstance(sub_token_2,
                                      non_grouped.QuantifierRegexToken):
                        merge_to_char_0_1 = True

            if merge_to_char_0_1:
                sub_token_0.value += sub_token_1.value
                self._sub_tokens = (self._sub_tokens[:sub_token_pos + 1]
                                    + self._sub_tokens[sub_token_pos + 2:])
            else:
                sub_token_pos += 1
            self._merge_sub_tokens(sub_token_pos)

    def _parse_pattern(self) -> None:
        start_pos = self._start_pos + len(self._opening)
        pattern = self.root_token.pattern
        len_pattern = len(pattern)

        while start_pos < len_pattern:
            if pattern[start_pos] == self._close_with:
                self._closing = self._close_with
                self._closed = True
                break

            tokenized = False
            for token_type in self._parse_for_tokens:
                if token_type.is_disabled():
                    continue

                new_token = token_type.new(
                    pattern=pattern,
                    start_pos=start_pos,
                    super_token=self
                )
                if new_token:
                    start_pos += new_token.length
                    tokenized = True
                    break
            if not tokenized:
                raise Exception(f"Tokenization failed for pattern starting at"
                                f" position {start_pos}, actual content at this"
                                f" position: "
                                f" '{pattern[start_pos:start_pos + 16]}...'")

        self._merge_sub_tokens()

        if not self._closed:
            self._err('Group not closed')


class CapturingGroupRegexToken(GroupedRegexToken):
    """
    This is a class to differentiate derived classes from generic grouped tokens
    and capturing group token.
    """
    _TOKEN_PATTERN = re.compile(r"\((?!\?)", re.NOFLAG)

    def __init__(self,
                 opening: str,
                 start_pos: int,
                 super_token: GroupedRegexToken | None):
        super().__init__(opening=opening,
                         start_pos=start_pos,
                         super_token=super_token)

        self._group_id = self._calc_group_id()

    @property
    def group_id(self) -> int:
        return self._group_id

    @property
    def label(self) -> str:
        return f"{self._friendly_type} #{self._group_id}"

    @property
    def summary(self) -> str:
        return (f"Groups multiple tokens together and creates a capturing"
                f" group #{self._group_id} for using as a backreference")

    def _calc_group_id(self) -> int:
        walk_down_tokens = self.root_token.walk_down_token(
            stop_at_token=self,
            skip_stop_token_lineage=False,
            skip_start_token=True,
            skip_stop_token=False
        )[0]

        group_id = 0
        for token in walk_down_tokens:
            if isinstance(token, CapturingGroupRegexToken):
                group_id += 1
        return group_id


class NonCapturingGroupRegexToken(GroupedRegexToken):
    """
    This is a place-holder class to differentiate derived classes from generic
    grouped tokens and non-capturing group token.
    """
    _TOKEN_PATTERN = re.compile(r"\(\?:", re.NOFLAG)

    @property
    def summary(self) -> str:
        return ("Groups multiple tokens together without creating a capturing"
                " group")


class MiscGroupRegexToken(GroupedRegexToken):
    """
    Groups that don't fall under capturing or non-capturing fall under this
    category of token, e.g. CharSetRegexToken and RegexTokenizer. There is no
    technical reason for this token to exist, it just places various tokens
    under categories for clear understanding.
    """
    pass


class AtomicGroupRegexToken(NonCapturingGroupRegexToken):
    """
    Usually the Regex engine will backtrack on text, including text matched in
    groups, in case matches down the pattern are not found. However, the engine
    will not backtrack on an atomic group once consumed. Another way of
    accomplishing the same thing is using the possessive '+' quantifier.

    Atomic groups are supported in Python since v3.11.
    """
    _TOKEN_PATTERN = re.compile(r"\(\?>", re.NOFLAG)

    @property
    def summary(self) -> str:
        return (f"Non-capturing group that discards backtracking position once"
                f" matched")


class CharSetRegexToken(MiscGroupRegexToken):
    _TOKEN_PATTERN = re.compile(r"\[(?P<not_>\^?)", re.NOFLAG)

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        instance._parse_for_tokens = [
            non_grouped.CharClassRegexToken,
            non_grouped.EscapedCharRegexToken,
            non_grouped.HexValueRegexToken,
            non_grouped.OctalValueRegexToken,
            non_grouped.UnicodeNamedCharRegexToken,
            non_grouped.UnicodeValueRegexToken,
            non_grouped.LiteralRegexToken
        ]
        return instance

    def __init__(self,
                 opening: str,
                 start_pos: int,
                 super_token: GroupedRegexToken):
        super().__init__(opening=opening,
                         start_pos=start_pos,
                         super_token=super_token)

        re_match = self._TOKEN_PATTERN.match(opening)
        self._not = re_match.group("not_") == "^"

    @property
    def summary(self) -> str:
        return f"Matches any character {'not ' if self._not else ''}in the set"

    def _merge_sub_tokens(self, sub_token_pos: int = 0) -> None:
        """
        Merges CharRegexTokens sub_tokens.
        """
        total_sub_tokens = len(self._sub_tokens)
        remaining_sub_tokens = total_sub_tokens - sub_token_pos

        if remaining_sub_tokens >= 2:
            merge_to_char_0_1 = False
            merge_to_range_0_1_2 = False
            sub_token_0 = self._sub_tokens[sub_token_pos]
            sub_token_0_is_lit = isinstance(sub_token_0,
                                            non_grouped.LiteralRegexToken)
            sub_token_1 = self._sub_tokens[sub_token_pos + 1]
            sub_token_1_is_lit = isinstance(sub_token_1,
                                            non_grouped.LiteralRegexToken)
            sub_token_2 = None

            if remaining_sub_tokens == 2:
                if (sub_token_0_is_lit
                        and sub_token_1_is_lit):
                    merge_to_char_0_1 = True
            else:
                sub_token_2 = self._sub_tokens[sub_token_pos + 2]
                sub_token_2_is_lit = isinstance(sub_token_2,
                                                non_grouped.LiteralRegexToken)
                if (sub_token_1_is_lit
                        and sub_token_1.value == "-"):
                    merge_to_range_0_1_2 = True
                elif (sub_token_0_is_lit
                      and sub_token_1_is_lit
                      and not (sub_token_2_is_lit
                               and sub_token_2.value == "-")):
                    merge_to_char_0_1 = True

            if merge_to_char_0_1:
                sub_token_0.value += sub_token_1.value
                self._sub_tokens = (self._sub_tokens[:sub_token_pos + 1]
                                    + self._sub_tokens[sub_token_pos + 2:])
            elif merge_to_range_0_1_2:
                range_token = non_grouped.RangeRegexToken(
                    super_token=self,
                    from_token=sub_token_0,
                    hyphen_token=sub_token_1,
                    to_token=sub_token_2
                )
                self._sub_tokens = (self._sub_tokens[:sub_token_pos]
                                    + (range_token,)
                                    + self._sub_tokens[sub_token_pos + 3:-1])
                sub_token_pos += 1
            else:
                sub_token_pos += 1

            self._merge_sub_tokens(sub_token_pos)


class ConditionalGroupRegexToken(NonCapturingGroupRegexToken):
    _TOKEN_PATTERN = re.compile(
        r"\(\?\((?P<backref_group_id_name>.*?)(?<!\\)\)",
        re.NOFLAG
    )

    def __init__(self,
                 opening: str,
                 start_pos: int,
                 super_token: GroupedRegexToken | None):
        super().__init__(opening=opening,
                         start_pos=start_pos,
                         super_token=super_token)

        re_match = self._TOKEN_PATTERN.match(opening)
        backref_group_id_name = re_match.group("backref_group_id_name")
        self._group_id = None
        self._group_name = None
        if backref_group_id_name:
            try:
                self._group_id = int(backref_group_id_name)
            except ValueError:
                self._group_name = backref_group_id_name

        if (self._group_id
                and self._group_id not in self.backref_group_ids):
            self._err(f"Invalid group reference '{self._group_id}'")
        if (self._group_name
                and self._group_name not in self.backref_group_names):
            self._err(f"Unknown group reference '{self._group_name}'")
        if self._count_sub_token_of_type(non_grouped.OrRegexToken) > 1:
            self._err(f"Conditional group with more than 2 branches")

    @property
    def summary(self) -> str:
        return (f"Conditionally matches one of two options based on whether"
                f" group '{self._group_id or self._group_name}' matched")


class LookaroundGroupRegexToken(NonCapturingGroupRegexToken):
    """
    A non-capturing positive or negative lookahead or lookbehind group token.
    """
    _TOKEN_PATTERN = re.compile(
        r"\(\?(?P<look_direction><?)(?P<pos_neg>[=!])",
        re.NOFLAG
    )
    _LOOKAROUND_DESCRIPTION = {
        "=": ("Positive Lookahead",
              "Matches this group after the previous token; this group is not"
              " included in the result"),
        "<=": ("Positive Lookbehind",
               "Matches this group before the next token; this group is not"
               " included in the result"),
        "!": ("Negative Lookahead",
              "Specifies this group cannot match after the previous token; this"
              " group is not included in the result"),
        "<!": ("Negative Lookbehind",
               "Specifies this group cannot match before the next token; this"
               " group is not included in the result")
    }

    def __init__(self,
                 opening: str,
                 start_pos: int,
                 super_token: GroupedRegexToken):
        super().__init__(opening=opening,
                         start_pos=start_pos,
                         super_token=super_token)

        re_match = self._TOKEN_PATTERN.match(opening)
        self._look_direction_char = re_match.group("look_direction")
        self._pos_neg_char = re_match.group("pos_neg")
        self._lookaround_class = self._LOOKAROUND_DESCRIPTION[
            f"{self._look_direction_char}{self._pos_neg_char}"
        ][0]

    @property
    def label(self) -> str:
        return f"{self._friendly_type}:{self._lookaround_class}"

    @property
    def summary(self) -> str:
        return self._LOOKAROUND_DESCRIPTION[
            f"{self._look_direction_char}{self._pos_neg_char}"
        ][1]


class NamedGroupRegexToken(CapturingGroupRegexToken):
    _TOKEN_PATTERN = re.compile(r"\(\?P<(?P<group_name>.*?)>", re.NOFLAG)

    def __init__(self,
                 opening: str,
                 start_pos: int,
                 super_token: GroupedRegexToken):
        super().__init__(opening=opening,
                         start_pos=start_pos,
                         super_token=super_token)

        re_match = self._TOKEN_PATTERN.match(opening)
        self._group_name = re_match.group("group_name")

    @property
    def group_name(self):
        return self._group_name

    @property
    def label(self) -> str:
        return f"{self._friendly_type} '{self._group_name}'"

    @property
    def summary(self) -> str:
        return (f"Creates a capturing group named '{self._group_name}' (also"
                f" back-referencable with group-id #{self.group_id})")


class FlagModifierRegexToken(NonCapturingGroupRegexToken):
    _TOKEN_PATTERN = re.compile(r"\(\?[-aiLmsux][^)]*?:", re.NOFLAG)
    re_parse = re.compile(r"\(\?(?P<set_flags>[^-]*)"
                          r"(?P<hyphen>-?)"
                          r"(?P<unset_flags>.*):", re.IGNORECASE)

    def __init__(self,
                 opening: str,
                 start_pos: int,
                 super_token: GroupedRegexToken):
        super().__init__(opening=opening,
                         start_pos=start_pos,
                         super_token=super_token)

        re_match = self.re_parse.match(opening)
        self._set_flags = re_match.group("set_flags")
        self._unset_flags = re_match.group("unset_flags")
        hyphen = re_match.group("hyphen")

        valid_flags_list = list(_FLAGS_STR2RE.keys())
        valid_set_flags_list = []
        valid_unset_flags_list = []

        for flag in self._set_flags:
            if flag not in valid_flags_list:
                self._err(f"Unknown flag '{flag}'")
                continue
            if flag == "L":
                self._err("Cannot use 'L' (re.LOCALE) flag with string pattern")
                continue
            if flag == "a" and "u" in self._set_flags:
                self._err("Flags 'a' (re.ASCII) and 'u' (re.UNICODE) cannot be"
                          " set simultaneously")
                continue
            valid_set_flags_list.append(flag)

        if hyphen and not self._unset_flags:
            self._err(f"Missing unset flag(s)'")

        for flag in self._unset_flags:
            if flag not in valid_flags_list:
                self._err(f"Unknown flag '{flag}'")
                continue
            re_flag = f"re.{_FLAGS_STR2RE[flag].strip('_').upper()}"
            if flag in ["a", "L", "u"]:
                self._err(f"Cannot turn off flag '{flag}' ({re_flag})")
                continue
            if flag in valid_set_flags_list:
                self._err(f"Flag '{flag}' ({re_flag}) turned on and off")
                valid_set_flags_list.remove(flag)
                continue
            valid_unset_flags_list.append(flag)

        self._valid_set_flags = "".join(valid_set_flags_list)
        self._valid_unset_flags = "".join(valid_unset_flags_list)

        self._ascii = True if "a" in self._valid_set_flags \
            else False if "u" in self._valid_set_flags \
            else None
        self._ignorecase = True if "i" in self._valid_set_flags \
            else False if "i" in self._valid_unset_flags \
            else None
        self._multiline = True if "m" in self._valid_set_flags \
            else False if "m" in self._valid_unset_flags \
            else None
        self._dotall = True if "s" in self._valid_set_flags \
            else False if "s" in self._valid_unset_flags \
            else None
        self._verbose = True if "x" in self._valid_set_flags \
            else False if "x" in self._valid_unset_flags \
            else None

    @property
    def _partial_summary(self) -> str:
        if self._valid_set_flags and self._valid_unset_flags:
            summary = (f"Enables '{self._valid_set_flags}' and disables"
                       f" '{self._valid_unset_flags}'")
        elif self._valid_set_flags:
            summary = f"Enables '{self._valid_set_flags}'"
        elif self._valid_unset_flags:
            summary = f"Disables '{self._valid_unset_flags}'"
        else:
            summary = "Enables and/or disables"
        return summary

    @property
    def summary(self) -> str:
        return (f"{self._partial_summary} flag(s) for tokens within this"
                f" non-capturing group")


class GlobalFlagsRegexToken(FlagModifierRegexToken):
    _TOKEN_PATTERN = re.compile(r"\(\?[-aiLmsux](.*?(?<!\\)(?=\)))", re.NOFLAG)
    re_parse = re.compile(r"\(\?(?P<set_flags>[^-]*)"
                          r"(?P<hyphen>-?)"
                          r"(?P<unset_flags>.*)", re.IGNORECASE)

    def __init__(self,
                 opening: str,
                 start_pos: int,
                 super_token: GroupedRegexToken):
        super().__init__(opening=opening,
                         start_pos=start_pos,
                         super_token=super_token)

        if not self.id == 0:
            self._err(f"Global flags can be set only at the very beginning of"
                      f" the expression")
            self._ascii = self._ignorecase = self._multiline = self._dotall = \
                self._verbose = None

    @property
    def summary(self) -> str:
        return f"{self._partial_summary} flag(s) for the whole pattern"


class UnknownGroupRegexToken(MiscGroupRegexToken):
    _TOKEN_PATTERN = re.compile(r"\(\?\\?.?", re.NOFLAG)

    def __init__(self,
                 opening: str,
                 start_pos: int,
                 super_token: GroupedRegexToken | None):
        super().__init__(opening=opening,
                         start_pos=start_pos,
                         super_token=super_token)
        self._err("Invalid group")

    @property
    def summary(self) -> str:
        return "Unrecognized grouping attempt"
