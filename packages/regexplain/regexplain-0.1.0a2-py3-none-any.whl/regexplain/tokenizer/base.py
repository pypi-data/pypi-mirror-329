"""
Token classes to assist in tokenizing regex patterns for human-friendly
explanation.

Implements the following tokens:
  BaseRegexToken
  ├── GroupedRegexToken
  │   │── CapturingGroupRegexToken
  │   │   └── NamedGroupRegexToken
  │   │── NonCapturingGroupRegexToken
  │   │   ├── AtomicGroupRegexToken
  │   │   ├── ConditionalGroupRegexToken
  │   │   ├── FlagModifierRegexToken
  │   │   ├── GlobalFlagsRegexToken
  │   │   └── LookaroundGroupRegexToken
  │   └── MiscGroupRegexToken
  │       ├── CharSetRegexToken
  │       ├── RegexTokenizer
  │       └── UnknownGroupRegexToken
  └── NonGroupedRegexToken
      ├── BoundedRegexToken
      │   ├── CommentRegexToken
      │   └── GroupNameBackrefRegexToken
      └── UnboundedRegexToken
          ├── AnchorRegexToken
          ├── CharClassRegexToken
          ├── EscapedCharRegexToken
          ├── GroupIdBackrefRegexToken
          ├── HexValueRegexToken
          ├── LiteralRegexToken
          ├── OctalValueRegexToken
          ├── OrRegexToken
          ├── QuantifierRegexToken
          ├── RangeRegexToken
          ├── UnicodeNamedCharRegexToken
          ├── UnicodeValueRegexToken
          ├── UnpairedParenthesisRegexToken
          └── WildcardRegexToken
"""

from __future__ import annotations
from abc import abstractmethod
import re
from typing import Self
from . import grouped, root


class BaseRegexToken:
    """
    Base class for all regex tokens.

    This class implements most commonly used attributes and methods by all
    derived tokens. It is not meant to be instantiated directly, as additional
    functionality is usually required.

    Some methods may check for the instance being of a derived class, as
    putting those checks in those derived classes may unnecessarily complicate
    code.
    """
    _DISABLED = False
    _TOKEN_PATTERN = None
    _LABEL_PATTERN = re.compile(r"[A-Z].*?(?=[A-Z]|$)")
    _REPLACE_LABEL_WORDS = {
        "Backref": "Backreference",
        "Char": "Character"
    }

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._friendly_type = ' '.join(
            [cls._REPLACE_LABEL_WORDS[word]
             if word in cls._REPLACE_LABEL_WORDS
             else word for word
             in cls._LABEL_PATTERN.findall(cls.__name__)[:-2]]
        )
        instance._ascii = None
        instance._ignorecase = None
        instance._locale = None
        instance._multiline = None
        instance._dotall = None
        instance._verbose = None
        instance._debug = None
        return instance

    def __init__(self, start_pos: int, super_token):
        # Collection of messages as they are generated during parsing or end of
        # parsing of a token.
        self._messages = {"i": [], "w": [], "e": []}

        self._start_pos = start_pos
        if not (super_token is None
                or isinstance(super_token, grouped.GroupedRegexToken)):
            raise ValueError("Super token must be a GroupedRegexToken")
        self._super_token = super_token

        self._auto_post_init()

    @property
    def case_sensitivity(self) -> str:
        return "case-insensitive" if self.ignorecase else "case-sensitive"

    @property
    def ascii_(self) -> bool:
        """
        Complementary of re.UNICODE flag.
        Simplified boolean representation of re.RegexFlag at token level. It is
        not set (i.e. is None) by default for each token. It can be overwritten
        by the following chain:
        1) If FlagModifierRegexToken appears in its hierarchical chain and this
           flag is set (True or False)
        2) If (1) is still None, then if GlobalFlagsRegexToken is the first
           token in the root token and this flag is set (True or False)
        3) If (2) is still None, then this flag as set in the root token (False
           by default, unless root token was initialized with this flag, then
           True).
        """
        ascii_ = self._ascii
        if (ascii_ is None
                and self.level == 1
                and self.index > 0):
            sibling_0 = self.get_sibling(0)
            if isinstance(sibling_0, grouped.GlobalFlagsRegexToken):
                ascii_ = sibling_0.ascii_

        return self.super_token.ascii_ \
            if ascii_ is None \
            else ascii_

    @property
    def ignorecase(self) -> bool:
        """
        Simplified boolean representation of re.RegexFlag at token level. It is
        not set (i.e. is None) by default for each token. It can be overwritten
        by the following chain:
        1) If FlagModifierRegexToken appears in its hierarchical chain and this
           flag is set (True or False)
        2) If (1) is still None, then if GlobalFlagsRegexToken is the first
           token in the root token and this flag is set (True or False)
        3) If (2) is still None, then this flag as set in the root token (False
           by default, unless root token was initialized with this flag, then
           True).
        """
        ignorecase = self._ignorecase
        if (ignorecase is None
                and self.level == 1
                and self.index > 0):
            sibling_0 = self.get_sibling(0)
            if isinstance(sibling_0, grouped.GlobalFlagsRegexToken):
                ignorecase = sibling_0.ignorecase

        return self.super_token.ignorecase \
            if ignorecase is None \
            else ignorecase

    @property
    def locale(self) -> bool:
        """
        Simplified boolean representation of re.RegexFlag at token level. It is
        not set (i.e. is None) by default for each token, and is set only
        in the root token.
        """
        return self.root_token.locale \
            if self._locale is None \
            else self._locale

    @property
    def multiline(self) -> bool:
        """
        Simplified boolean representation of re.RegexFlag at token level. It is
        not set (i.e. is None) by default for each token. It can be overwritten
        by the following chain:
        1) If FlagModifierRegexToken appears in its hierarchical chain and this
           flag is set (True or False)
        2) If (1) is still None, then if GlobalFlagsRegexToken is the first
           token in the root token and this flag is set (True or False)
        3) If (2) is still None, then this flag as set in the root token (False
           by default, unless root token was initialized with this flag, then
           True).
        """
        multiline = self._multiline
        if (multiline is None
                and self.level == 1
                and self.index > 0):
            sibling_0 = self.get_sibling(0)
            if isinstance(sibling_0, grouped.GlobalFlagsRegexToken):
                multiline = sibling_0.multiline

        return self.super_token.multiline \
            if multiline is None \
            else multiline

    @property
    def dotall(self) -> bool:
        """
        Simplified boolean representation of re.RegexFlag at token level. It is
        not set (i.e. is None) by default for each token. It can be overwritten
        by the following chain:
        1) If FlagModifierRegexToken appears in its hierarchical chain and this
           flag is set (True or False)
        2) If (1) is still None, then if GlobalFlagsRegexToken is the first
           token in the root token and this flag is set (True or False)
        3) If (2) is still None, then this flag as set in the root token (False
           by default, unless root token was initialized with this flag, then
           True).
        """
        dotall = self._dotall
        if (dotall is None
                and self.level == 1
                and self.index > 0):
            sibling_0 = self.get_sibling(0)
            if isinstance(sibling_0, grouped.GlobalFlagsRegexToken):
                dotall = sibling_0.dotall

        return self.super_token.dotall \
            if dotall is None \
            else dotall

    @property
    def verbose(self) -> bool:
        """
        Simplified boolean representation of re.RegexFlag at token level. It is
        not set (i.e. is None) by default for each token. It can be overwritten
        by the following chain:
        1) If FlagModifierRegexToken appears in its hierarchical chain and this
           flag is set (True or False)
        2) If (1) is still None, then if GlobalFlagsRegexToken is the first
           token in the root token and this flag is set (True or False)
        3) If (2) is still None, then this flag as set in the root token (False
           by default, unless root token was initialized with this flag, then
           True).
        """
        verbose = self._verbose
        if (verbose is None
                and self.level == 1
                and self.index > 0):
            sibling_0 = self.get_sibling(0)
            if isinstance(sibling_0, grouped.GlobalFlagsRegexToken):
                verbose = sibling_0.verbose

        return self.super_token.verbose \
            if verbose is None \
            else verbose

    @property
    def debug(self) -> bool:
        """
        Simplified boolean representation of re.RegexFlag at token level. It is
        not set (i.e. is None) by default for each token, and is set only
        in the root token.
        """
        return self.root_token.debug \
            if self._debug is None \
            else self._debug

    @property
    def backref_groups(self) -> str:
        """
        The group-ids that can be back-referenced by this token.
        """
        walk_down_tokens = self.root_token.walk_down_token(
            stop_at_token=self,
            skip_stop_token_lineage=True,
            skip_start_token=True,
            skip_stop_token=True
        )[0]

        backref_groups = []
        for token in walk_down_tokens:
            if not isinstance(token, grouped.CapturingGroupRegexToken):
                continue
            backref_group = str(token.group_id)
            if isinstance(token, grouped.NamedGroupRegexToken):
                backref_group += f" ('{token.group_name}')"
            backref_groups.append(backref_group)

        return ", ".join(backref_groups) or None

    @property
    def backref_group_ids(self) -> list:
        """
        The group-ids that can be back-referenced by this token.
        """
        walk_down_tokens = self.root_token.walk_down_token(
            stop_at_token=self,
            skip_stop_token_lineage=True,
            skip_start_token=True,
            skip_stop_token=True
        )[0]

        return [token.group_id
                for token in walk_down_tokens
                if isinstance(token, grouped.CapturingGroupRegexToken)]

    @property
    def backref_group_names(self) -> list:
        """
        The group-names that can be back-referenced by this token.
        """
        walk_down_tokens = self.root_token.walk_down_token(
            stop_at_token=self,
            skip_stop_token_lineage=True,
            skip_start_token=True,
            skip_stop_token=True
        )[0]

        return [token.group_name
                for token in walk_down_tokens
                if isinstance(token, grouped.NamedGroupRegexToken)]

    @property
    def warnings(self) -> list[str]:
        return self._messages["w"]

    @property
    def errors(self) -> list[str]:
        return self._messages["e"]

    @property
    def flags(self) -> re.RegexFlag | None:
        flags = re.NOFLAG
        if self.ascii_:
            flags |= re.ASCII
        if self.ignorecase:
            flags |= re.IGNORECASE
        if self.locale:
            flags |= re.LOCALE
        if self.multiline:
            flags |= re.MULTILINE
        if self.dotall:
            flags |= re.DOTALL
        if self.verbose:
            flags |= re.VERBOSE
        if self.debug:
            flags |= re.DEBUG
        return flags

    @property
    def id(self) -> int | None:
        return len(self.root_token.walk_down_token(
            stop_at_token=self,
            skip_stop_token_lineage=False,
            skip_start_token=True,
            skip_stop_token=True)[0])

    @property
    def index(self) -> int | None:
        """
        The sequence/order number of a sub_token in its super token, e.g.
          super_token:
          ├── sub_token (seq number 0)
          └── sub_token (seq number 1)
              ├── sub_sub_token (seq number 0)
              └── sub_sub_token (seq number 1)
        """
        seq_num = None
        for i, sub_token in enumerate(self.super_token.sub_tokens):
            if id(sub_token) == id(self):
                seq_num = i
                break
        return seq_num

    @property
    def is_last_sibling(self) -> bool | None:
        return self.index == len(self.super_token.sub_tokens) - 1

    @property
    def label(self) -> str:
        return self._friendly_type

    @property
    def length(self) -> int:
        return len(str(self))

    @property
    def level(self) -> int:
        """
        How deep is the token from the root token. This is useful in indenting
        the output.
        """
        return self.super_token.level + 1

    @property
    def root_token(self) -> root.RegexTokenizer:
        """
        Recursively go up the hierarchy until the root token is reached. The
        root token forms the baseline for a number of things, viz. level,
        group-id, etc.
        """
        return self.super_token.root_token

    @property
    def span(self) -> tuple[int, int]:
        """
        Tuple of start and end position of the token. The end position number is
        one more than the index of the last character of the token, much like
        Python range(start, end).
        """
        return (self.start_pos,
                self.start_pos + self.length)

    @property
    def start_pos(self) -> int:
        return self._start_pos

    @property
    def super_token(self) -> grouped.GroupedRegexToken:
        return self._super_token

    @property
    def summary(self) -> str:
        return ""

    @property
    @abstractmethod
    def value(self) -> str:
        ...

    @classmethod
    def is_disabled(cls):
        return cls._DISABLED

    @classmethod
    def new(cls,
            pattern: str,
            start_pos: int,
            super_token: grouped.GroupedRegexToken) -> Self:
        re_match = cls._TOKEN_PATTERN.match(pattern, start_pos)

        if re_match:
            kwargs = {
                "start_pos": start_pos,
                "super_token": super_token
            }
            if issubclass(cls, grouped.GroupedRegexToken):
                kwargs["opening"] = re_match.group(0)
            else:
                kwargs["value"] = re_match.group(0)
            return cls(**kwargs)
        else:
            return None

    def explain(self,
                show_span: bool = True,
                show_group_pattern: bool = False,
                show_flags: bool = True,
                show_backreferences: bool = False,
                show_group_close_annotation: bool = True) -> None:
        pattern_type = "Full Pattern" \
            if isinstance(self, root.RegexTokenizer) else \
            "Part of Pattern"
        print(f"Explaining {pattern_type}: {str(self)}")

        self._explain(show_span=show_span,
                      show_group_pattern=show_group_pattern,
                      show_flags=show_flags,
                      show_backreferences=show_backreferences,
                      show_group_close_annotation=show_group_close_annotation)

    def get_sibling(self, index: int | str) -> type[Self] | None:
        """
        Returns the sibling relative to the current sub token from the super
        token.
        """
        sibling = None
        index_int = int(index)

        if ((isinstance(index, str) and index[0] == "+")
                or index_int < 0):
            index_int = self.index + index_int
        if 0 <= index_int < len(self.super_token.sub_tokens):
            sibling = self.super_token.sub_tokens[index_int]

        return sibling

    def _inf(self, message: str):
        self._messages["i"].append(message)

    def _wrn(self, message: str):
        self._messages["w"].append(message)

    def _err(self, message: str):
        self._messages["e"].append(message)

    def _auto_post_init(self):
        if self._super_token is not None:
            self._super_token.append_sub_tokens(self)

    def _explain(self,
                 show_span: bool,
                 show_flags: bool,
                 show_group_pattern: bool,
                 show_backreferences: bool,
                 show_group_close_annotation: bool,
                 indent: str = "") -> None:
        (top_bound, bottom_bound, title_indent, body_indent, sub_token_indent) \
            = _get_box_symbols(indent)
        self_is_group = isinstance(self, grouped.GroupedRegexToken)
        self_is_root = isinstance(self, root.RegexTokenizer)
        token_opening_info = []

        print(f"{indent}{top_bound}")

        main_content = self._opening if self_is_group else self.value  # noqa
        if main_content:
            token_opening_info.append(main_content)

        summary = self.summary
        if summary:
            token_opening_info.append(f"  [#{self.id}:{self.label}] {summary}")

        if show_group_pattern:
            group_content = str(self) \
                if (self_is_group and not self_is_root) \
                else ""
            if group_content:
                token_opening_info.append(f"  [Group Pattern] {group_content}")

        if show_span:
            token_opening_info.append(f"  [Span, Length]"
                                      f" {self.span}, {self.length}")

        if show_flags and self.flags is not None:
            token_opening_info.append(f"  [Flags] {str(self.flags)}")

        if show_backreferences and not self_is_root:
            token_opening_info.append(f"  [Back-referencable Groups]"
                                      f" {self.backref_groups}")

        for i, info_line in enumerate(token_opening_info):
            print(f"{indent}"
                  f"{title_indent if i == 0 else body_indent}"
                  f"{info_line}")

        if self.errors:
            for error in self.errors:
                print(f"{indent}{body_indent}  [Error] {error}")
        if self.warnings:
            for warning in self.warnings:
                print(f"{indent}{body_indent}  [Warning] {warning}")

        if self_is_group:
            for sub_token in self._sub_tokens:  # NOQA
                sub_token._explain(  # NOQA
                    show_span=show_span,
                    show_group_pattern=show_group_pattern,
                    show_flags=show_flags,
                    show_backreferences=show_backreferences,
                    show_group_close_annotation=show_group_close_annotation,
                    indent=f"{indent}{sub_token_indent}"
                )
            if self._closing:  # NOQA
                print(f"{indent}{body_indent}{self._closing}")  # NOQA
                if show_group_close_annotation:
                    print(f"{indent}{body_indent}  [#{self.id}:Close Group] ")

        print(f"{indent}{bottom_bound}")


def _get_box_symbols(indent: str) -> tuple[str, str, str, str, str]:
    """
    :return:
      top_bound, bottom_bound, title_indent, body_indent, sub_token_indent
    """
    return ("  ┌──", "  └──", "──│ ", "  │ ", "  │") \
        if indent \
        else ("┌──", "└──", "│ ", "│ ", "│")
