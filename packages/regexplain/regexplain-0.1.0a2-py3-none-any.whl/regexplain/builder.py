from __future__ import annotations
from collections.abc import Mapping, Sequence
from collections import OrderedDict
from inspect import isfunction, signature
import functools
import re
from typing import Callable, Self

from .builder_bkp import RegexBuilder
from .utils import _FLAGS_RE2STR


def aliases(*alias_names: str):
    """
    This decorator sets attribute '_aliases' within the function it is
    decorating to set of alias names passed to the decorator. The 'aliasable'
    decorator then replicates the function to its aliases.
    """
    def add_aliases_to_func(func: Callable):
        func._aliases = set(alias_names)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    return add_aliases_to_func


def aliasable(aliased_class):
    """
    Replicates all methods of the class it decorates which have '_aliases'
    attribute.
    """
    aliased_methods = [name for name, method in aliased_class.__dict__.items()
                       if isfunction(method) and hasattr(method, "_aliases")]
    for aliased_method in aliased_methods:
        method = getattr(aliased_class, aliased_method)
        method_aliases = getattr(method, '_aliases')
        delattr(method, "_aliases")
        for alias in method_aliases:
            setattr(aliased_class, alias, method)
    return aliased_class


def append_sub_token(func) -> Callable:
    """
    This decorator must be wrapped around a sub-token implemented as a function.
    It appends a tuple of the name of the function it decorates and its
    parameters to _sub_tokens attribute of the instance of RegexBuilder.
    """
    @functools.wraps(func)
    def wrapper(instance: RegexBuilder, *args, **kwargs):
        func_token_name = func.__name__.lstrip("_")
        parms = [[k, v.default]
                 for k, v in signature(func).parameters.items()
                 if not k == "self"]
        for i, parm_v in enumerate(args):
            parms[i][1] = parm_v
        parms = OrderedDict(parms)
        parms.update(kwargs)

        instance._add_sub_token(func_token_name, **parms)  # noqa
        return func(instance, *args, **kwargs)

    return wrapper


@aliasable
class RegexBuilder:
    """Human friendly regex builder.

    This is the main class to be instantiated to build a regex pattern. Just
    put a dot and see all available methods/properties in an IDE and
    """

    def __init__(self,
                 pattern: str | bytes | RegexBuilder = "",
                 *,
                 ascii_: bool = False,
                 ignorecase: bool = False,
                 locale: bool = False,
                 multiline: bool = False,
                 dotall: bool = False,
                 unicode: bool = False,
                 verbose: bool = False,
                 debug: bool = False):
        r"""
        :param ascii_:
            Makes several escapes like ``\w``, ``\b``, ``\s`` and ``\d`` match
            only on ASCII characters with the respective property.
        :param ignorecase:
            Do case-insensitive matches.
        :param locale:
            Do a locale-aware match.
        :param multiline:
            Multi-line matching, affects ``^`` and ``$``.
        :param dotall:
            Make ``.`` match any character, including newlines.
        :param verbose:
            Enable verbose REs, which can be organized more cleanly and
            understandably.
        :param debug:
            Display debug information about compiled expression.
        """
        self._ascii = self._ignorecase = self._locale = self._multiline \
            = self._dotall = self._unicode = self._verbose = self._debug \
            = None

        self._sub_tokens = []
        self._pattern_is_bytes = isinstance(pattern, bytes)
        self.literal(sub_pattern=pattern)

        self.ascii_ = ascii_
        self.ignorecase = ignorecase
        self.locale = locale
        self.multiline = multiline
        self.dotall = dotall
        self.unicode = unicode
        self.verbose = verbose
        self.debug = debug

    def __str__(self):
        return self.pattern

    def __repr__(self):
        return self._sub_tokens.__repr__()

    @property
    def ascii_(self) -> bool:
        return self._ascii

    @ascii_.setter
    def ascii_(self, value: bool) -> None:
        self._ascii = value

    @property
    def ignorecase(self) -> bool:
        return self._ignorecase

    @ignorecase.setter
    def ignorecase(self, value: bool) -> None:
        self._ignorecase = value

    @property
    def locale(self) -> bool:
        return self._locale

    @locale.setter
    def locale(self, value: bool) -> None:
        if value:
            if not self._pattern_is_bytes:
                raise ValueError("cannot use LOCALE flag with a str pattern")
            elif self._ascii:
                raise ValueError("ASCII and LOCALE flags are incompatible")
        self._locale = value

    @property
    def multiline(self) -> bool:
        return self._multiline

    @multiline.setter
    def multiline(self, value: bool) -> None:
        self._multiline = value

    @property
    def dotall(self) -> bool:
        return self._dotall

    @dotall.setter
    def dotall(self, value: bool) -> None:
        self._dotall = value

    @property
    def unicode(self) -> bool:
        return self._unicode

    @unicode.setter
    def unicode(self, value: bool) -> None:
        if value:
            if self._pattern_is_bytes:
                raise ValueError("cannot use UNICODE flag with a bytes pattern")
            elif self._ascii:
                raise ValueError("ASCII and UNICODE flags are incompatible")
        self._unicode = value

    @property
    def verbose(self) -> bool:
        return self._verbose

    @verbose.setter
    def verbose(self, value: bool) -> None:
        self._verbose = value

    @property
    def debug(self) -> bool:
        return self._debug

    @debug.setter
    def debug(self, value: bool) -> None:
        self._debug = value

    @property
    def start_of_line(self) -> Self:
        self._add_sub_token("anchor", sub_pattern="^")
        return self

    @property
    def end_of_line(self) -> Self:
        self._add_sub_token("anchor", sub_pattern="$")
        return self

    @property
    def start_of_str(self) -> Self:
        self._add_sub_token("char_class", sub_pattern=r"\A")
        return self

    @property
    def end_of_str(self) -> Self:
        self._add_sub_token("char_class", sub_pattern=r"\Z")
        return self

    @property
    def empty_str_at_beginning_or_end_of_word(self) -> Self:
        self._add_sub_token("char_class", sub_pattern=r"\b")
        return self

    @property
    def empty_str_not_at_beginning_or_end_of_word(self) -> Self:
        self._add_sub_token("char_class", sub_pattern=r"\B")
        return self

    @property
    def digit(self) -> Self:
        self._add_sub_token("char_class", sub_pattern=r"\d")
        return self

    @property
    def non_digit(self) -> Self:
        self._add_sub_token("char_class", sub_pattern=r"\D")
        return self

    @property
    def word(self) -> Self:
        self._add_sub_token("char_class", sub_pattern=r"\w")
        return self

    @property
    def non_word(self) -> Self:
        self._add_sub_token("char_class", sub_pattern=r"\W")
        return self

    @property
    def whitespace(self) -> Self:
        self._add_sub_token("char_class", sub_pattern=r"\s")
        return self

    @property
    def non_whitespace(self) -> Self:
        self._add_sub_token("char_class", sub_pattern=r"\S")
        return self

    @property
    def caret(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\^")
        return self

    @property
    def dollar(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\$")
        return self

    @property
    def dot(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\.")
        return self

    @property
    def backslash(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\\")
        return self

    @property
    def hyphen(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\-")
        return self

    @property
    def asterisk(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\*")
        return self

    @property
    def plus(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\+")
        return self

    @property
    def question_mark(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\?")
        return self

    @property
    def pipe(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\|")
        return self

    @property
    def escape(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\x1B")
        return self

    @property
    def alert(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\a")
        return self

    @property
    def bell(self) -> Self:
        return self.alert

    @property
    def backspace(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\b")
        return self

    @property
    def tab(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\t")
        return self

    @property
    def vertical_tab(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\v")
        return self

    @property
    def form_feed(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\f")
        return self

    @property
    def line_feed(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\n")
        return self

    @property
    def lf(self) -> Self:
        return self.line_feed

    @property
    def unix_line_break(self) -> Self:
        return self.line_feed

    @property
    def carriage_return(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\r")
        return self

    @property
    def cr(self) -> Self:
        return self.carriage_return

    @property
    def carriage_return_line_feed(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\r\n")
        return self

    @property
    def crlf(self) -> Self:
        return self.carriage_return

    @property
    def windows_line_break(self) -> Self:
        return self.carriage_return

    @property
    def single_quote(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\'")
        return self

    @property
    def double_quote(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r'\"')
        return self

    @property
    def colon(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\:")
        return self

    @property
    def comma(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\,")
        return self

    @property
    def equal(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\=")
        return self

    @property
    def exclamation_mark(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\!")
        return self

    @property
    def opening_parentheses(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\(")
        return self

    @property
    def closing_parentheses(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\)")
        return self

    @property
    def opening_square_bracket(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\[")
        return self

    @property
    def closing_square_bracket(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\]")
        return self

    @property
    def opening_curly_bracket(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\{")
        return self

    @property
    def closing_curly_bracket(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\}")
        return self

    @property
    def opening_angle_bracket(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\<")
        return self

    @property
    def less_than(self) -> Self:
        return self.opening_angle_bracket

    @property
    def closing_angle_bracket(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern=r"\>")
        return self

    @property
    def greater_than(self) -> Self:
        return self.closing_angle_bracket

    @property
    def or_(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern="|")
        return self

    @property
    def line_break(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern="\n")
        return self

    @property
    def lb(self) -> Self:
        return self.line_break

    @property
    def ignore_backslash_newline(self) -> Self:
        self._add_sub_token("escaped_char", sub_pattern="\\\n")
        return self

    @property
    def hex_digit(self) -> Self:
        self._add_sub_token("custom", sub_pattern="[0-9A-Fa-f]")
        return self

    @property
    def non_hex_digit(self) -> Self:
        self._add_sub_token("custom", sub_pattern="[^0-9A-Fa-f]")
        return self

    @property
    def hex_digit_lower(self) -> Self:
        self._add_sub_token("custom", sub_pattern="[0-9a-f]")
        return self

    @property
    def non_hex_digit_lower(self) -> Self:
        self._add_sub_token("custom", sub_pattern="[^0-9a-f]")
        return self

    @property
    def hex_digit_upper(self) -> Self:
        self._add_sub_token("custom", sub_pattern="[0-9A-F]")
        return self

    @property
    def non_hex_digit_upper(self) -> Self:
        self._add_sub_token("custom", sub_pattern="[^0-9A-F]")
        return self

    @property
    def octal_digit(self) -> Self:
        self._add_sub_token("custom", sub_pattern="[0-7]")
        return self

    @property
    def non_octal_digit(self) -> Self:
        self._add_sub_token("custom", sub_pattern="[^0-7]")
        return self

    def flags_as(self,
                 in_flags: re.RegexFlag | Mapping | str | None = None,
                 out_flags_as: str | None = None
                 ) -> re.RegexFlag | dict | str | None:
        """Changes format of flags or updates self

        :param in_flags:
          Can be re.RegexFlag, Mapping (dict) or string.
        :param out_flags_as:
          Must be one of "re", "dict" or "str".
        :return:
          Returns flags in the "out_flags_as" format.
        """
        dict_flags = {}

        if in_flags is None:
            in_flags = self

        for name, abbr in _FLAGS_RE2STR.items():
            dict_flags[name] = (getattr(re, name.strip("_").upper())
                                in in_flags) \
                if isinstance(in_flags, re.RegexFlag) \
                else (name in in_flags and bool(in_flags[name])) \
                if isinstance(in_flags, Mapping) \
                else getattr(in_flags, name) \
                if isinstance(in_flags, type(self)) \
                else (bool(abbr) and abbr in in_flags)

        if out_flags_as == "re":
            out_flags = re.NOFLAG
            for name in _FLAGS_RE2STR.keys():
                if dict_flags[name]:
                    out_flags |= getattr(re, name.strip("_").upper())
        elif out_flags_as == "dict":
            out_flags = dict_flags
        elif out_flags_as == "str":
            out_flags = ""
            for name, abbr in _FLAGS_RE2STR.items():
                if dict_flags[name]:
                    out_flags += abbr
        elif out_flags_as is None:
            for name, bool_value in dict_flags:
                setattr(self, name, bool_value)
            return None
        else:
            raise ValueError("Argument `out_flags_as` must be one of"
                             " 're', 'dict', 'str' or None")

        return out_flags

    @property
    def pattern(self) -> str | bytes:
        return self._pattern()

    def _pattern(self,
                 accum_pattern: str | bytes | None = None,
                 rolling_group_info: dict[str, int | list] | None = None
                 ) -> str | bytes:
        if accum_pattern is None:
            accum_pattern = b"" if self._pattern_is_bytes else ""
        if rolling_group_info is None:
            rolling_group_info = {"last_group_id": 0,
                                  "group_names": []}

        for sub_token in self._sub_tokens:
            call_name = f"_call_{sub_token[0]}"

            parms = sub_token[1].copy()
            for parm_name, parm_value in parms.items():
                if isinstance(parm_value, RegexBuilder):
                    parm_value = parm_value._pattern(
                        rolling_group_info=rolling_group_info
                    )
                    parms[parm_name] = parm_value
            parms["rolling_group_info"] = rolling_group_info
            parms["accum_pattern"] = accum_pattern
            accum_pattern = getattr(self, call_name)(**parms)

        return accum_pattern

    def _add_sub_token(self,
                       sub_token_name: str,
                       **kwargs) -> None:
        self._sub_tokens.append((sub_token_name, kwargs))

    def literal(self, sub_pattern: str | bytes | RegexBuilder) -> Self:
        self._add_sub_token("literal", sub_pattern=sub_pattern)
        return self

    @aliases("_call_anchor", "_call_char_class", "_call_escaped_char")
    def _call_literal(self,
                      sub_pattern: str | bytes | RegexBuilder,
                      accum_pattern: str | bytes | None = None,
                      **kwargs  # noqa
                      ) -> str | bytes:
        if accum_pattern is None:
            accum_pattern = b"" if self._pattern_is_bytes else ""

        if self._pattern_is_bytes:
            if isinstance(sub_pattern, str):
                sub_pattern = str.encode(sub_pattern, encoding="utf-8")
        elif isinstance(sub_pattern, bytes):
            sub_pattern = sub_pattern.decode("utf-8")

        return accum_pattern + sub_pattern

    @append_sub_token
    def _wildcard(self, include_line_breaks: bool = False) -> Self:
        # self._add_sub_token("wildcard",
        #                     include_line_breaks=include_line_breaks)
        return self

    def _call_wildcard(self,
                       include_line_breaks: bool,
                       accum_pattern: str | bytes,
                       **kwargs  # noqa
                       ) -> str | bytes:
        if re.DOTALL in self.flags:
            # '[^\n\r]' = not '\n' and not '\r'
            sub_pattern = "." if include_line_breaks else r"[^\n\r]"
        else:
            # '?s:' temporarily turns on re.DOTALL
            sub_pattern = "(?s:.)" if include_line_breaks else "."
        return accum_pattern + sub_pattern

    @property
    def wildcard_excl_line_breaks(self) -> Self:
        return self._wildcard(include_line_breaks=False)

    @property
    def wildcard_incl_line_breaks(self) -> Self:
        return self._wildcard(include_line_breaks=True)

    @property
    def wildcard(self) -> Self:
        return self.wildcard_incl_line_breaks

    @property
    def any_char_excl_line_breaks(self) -> Self:
        return self.wildcard_excl_line_breaks

    @property
    def any_char_incl_line_breaks(self) -> Self:
        return self.wildcard_incl_line_breaks

    @property
    def any_char(self) -> Self:
        return self.wildcard

    @classmethod
    def char_8bit(cls, char: str) -> str:
        raise NotImplemented

    def _char_set(self, chars: Sequence | str, negate: bool = False) -> Self:
        self._add_sub_token("char_set", chars=chars, negate=negate)
        return self

    @staticmethod
    def _call_char_set(self,  # noqa
                       chars: Sequence | str,
                       negate: bool,
                       accum_pattern: str | bytes,
                       **kwargs  # noqa
    ) -> str | bytes:
        if isinstance(chars, Sequence):
            chars = ''.join(chars)
        return f"{accum_pattern}[{'^' if negate else ''}{chars}]"

    def in_char_set(self, chars: Sequence | str) -> str:
        return self._char_set(chars=chars, negate=False)

    def not_in_char_set(self, chars: Sequence | str) -> str:
        return self._char_set(chars=chars, negate=True)

    @append_sub_token
    def char_with_hex_value(self,
                            hex_value: str  # noqa
                            ) -> Self:
        return self

    @classmethod
    def _call_char_with_hex_value(cls,
                                  hex_value: str,
                                  accum_pattern: str | bytes,
                                  **kwargs  # noqa
                                  ) -> str | bytes:
        hex_value = _ltrim_chars(hex_value, 2, "0")
        if len(hex_value) > 2:
            accum_pattern = cls._call_char_with_unicode_hex_value(
                hex_value=hex_value,
                accum_pattern=accum_pattern
            )
        else:
            accum_pattern = (f"{accum_pattern}"
                             f"\\x{_lfill_chars(hex_value, 2, '0')}")
        return accum_pattern

    @append_sub_token
    def char_with_octal_value(self,
                              octal_value: str  # noqa
                              ) -> Self:
        return self

    @classmethod
    def _call_char_with_octal_value(cls,
                                    octal_value: str,
                                    accum_pattern: str | bytes,
                                    **kwargs  # noqa
                                    ) -> str | bytes:
        return f"{accum_pattern}\\{_lfill_chars(octal_value, 3, '0')}"

    @append_sub_token
    def char_with_unicode_name(self,
                               name: str  # noqa
                               ) -> Self:
        return self

    @classmethod
    def _call_char_with_unicode_name(cls,
                                     name: str,
                                     accum_pattern: str | bytes,
                                     **kwargs  # noqa
                                     ) -> str | bytes:
        return f"{accum_pattern}\\N{{{name}}}"

    @append_sub_token
    def char_with_unicode_hex_value(self,
                                    hex_value: str  # noqa
                                    ) -> Self:
        return self

    @classmethod
    def _call_char_with_unicode_hex_value(cls,
                                          hex_value: str,
                                          accum_pattern: str | bytes,
                                          **kwargs  # noqa
                                          ) -> str | bytes:
        hex_value = _ltrim_chars(hex_value, 4, "0")
        if len(hex_value) <= 4:
            accum_pattern = cls._call_char_with_unicode16_hex_value(
                hex_value=hex_value,
                accum_pattern=accum_pattern
            )
        else:
            accum_pattern = cls._call_char_with_unicode32_hex_value(
                hex_value=hex_value,
                accum_pattern=accum_pattern
            )
        return accum_pattern

    @append_sub_token
    def char_with_unicode16_hex_value(self,
                                      hex_value: str  # noqa
                                      ) -> Self:
        return self

    @classmethod
    def _call_char_with_unicode16_hex_value(cls,
                                            hex_value: str,
                                            accum_pattern: str | bytes,
                                            **kwargs  # noqa
                                            ) -> str | bytes:
        hex_value = _ltrim_chars(hex_value, 4, "0")
        return f"{accum_pattern}\\u{_lfill_chars(hex_value, 4, '0')}"

    @append_sub_token
    def char_with_unicode32_hex_value(self,
                                      hex_value: str  # noqa
                                      ) -> Self:
        return self

    @classmethod
    def _call_char_with_unicode32_hex_value(cls,
                                            hex_value: str,
                                            accum_pattern: str | bytes,
                                            **kwargs  # noqa
                                            ) -> str | bytes:
        hex_value = _ltrim_chars(hex_value, 8, "0")
        return f"{accum_pattern}\\u{_lfill_chars(hex_value, 8, '0')}"

    def comment(self,
                text: str  # noqa
                ) -> Self:
        self._add_sub_token("comment", text=text)
        return self

    def _call_comment(self,
                      text: str,
                      accum_pattern: str | bytes,
                      **kwargs  # noqa
                      ) -> str | bytes:
        return accum_pattern + self._call_literal(sub_pattern=f"(?#{text})")

    @classmethod
    def inline_unset_flags(cls,
                           ignorecase: bool = False,
                           multiline: bool = False,
                           dotall: bool = False,
                           verbose: bool = False) -> str:
        str_unset_flags = ""
        if ignorecase:
            str_unset_flags += _FLAGS_RE2STR["ignorecase"]
        if multiline:
            str_unset_flags += _FLAGS_RE2STR["multiline"]
        if dotall:
            str_unset_flags += _FLAGS_RE2STR["dotall"]
        if verbose:
            str_unset_flags += _FLAGS_RE2STR["verbose"]
        if str_unset_flags:
            str_unset_flags = "-" + str_unset_flags
        return str_unset_flags

    @append_sub_token
    def _group(self,
               sub_pattern: str | bytes | RegexBuilder,  # noqa
               non_capturing: bool = False,
               name: str | None = None,
               atomic: bool = False) -> Self:
        parms_count = 0
        if non_capturing:
            parms_count += 1
        if name:
            parms_count += 1
        if atomic:
            parms_count += 1
        if parms_count > 1:
            raise ValueError("Non-capturing, named and atomic characteristics"
                             " of a group are mutually exclusive")

        return self

    @classmethod
    def _call_group(cls,
                    sub_pattern: str | bytes | RegexBuilder | None,
                    non_capturing: bool,
                    name: str | None,
                    atomic: bool,
                    rolling_group_info: dict[str, int | list],
                    accum_pattern: str | bytes,
                    **kwargs  # noqa
                    ) -> str | bytes:
        if not (non_capturing or atomic):
            rolling_group_info["last_group_id"] += 1
        if name:
            rolling_group_info["group_names"].append(name)

        group_pattern = ("("
                         + ("?:" if non_capturing
                            else f"?P<{name}>" if name
                            else "?>" if atomic else ""))
        if sub_pattern is None:
            group_pattern += accum_pattern
        else:
            group_pattern = accum_pattern + group_pattern + sub_pattern

        return group_pattern + ")"

    def atomic_group(self,
                     sub_pattern: str | bytes | RegexBuilder | None = None
                     ) -> str | bytes:
        return self._group(sub_pattern=sub_pattern, atomic=True)

    def named_group(self,
                    name: str,
                    sub_pattern: str | bytes | RegexBuilder | None = None
                    ) -> str | bytes:
        return self._group(sub_pattern=sub_pattern, name=name)

    def non_capturing_group(
            self,
            sub_pattern: str | bytes | RegexBuilder | None = None
    ) -> str | bytes:
        return self._group(sub_pattern=sub_pattern, non_capturing=True)

    def numbered_group(self,
                       sub_pattern: str | bytes | RegexBuilder | None = None
                       ) -> str | bytes:
        return self._group(sub_pattern=sub_pattern)

    def group(self,
              sub_pattern: str | bytes | RegexBuilder | None = None
              ) -> str | bytes:
        return self.numbered_group(sub_pattern=sub_pattern)

    @append_sub_token
    def backref_group_id(self,
                         group_id: int | str  # noqa
                         ) -> Self:
        return self

    @classmethod
    def _call_backref_group_id(cls,
                               group_id: int | str,
                               accum_pattern: str | bytes,
                               **kwargs  # noqa
                               ) -> str | bytes:
        """Matches the contents of the group of the same number. Groups are
        numbered starting from 1. For example, (.+) \1 matches 'the the' or
        '55 55', but not 'tsetse' (note the space after the group). This
        special sequence can only be used to match one of the first 99 groups.
        If the first digit of number is 0, or number is 3 octal digits long, it
        will not be interpreted as a group match, but as the character with
        octal value number. Inside the '[' and ']' of a character class, all
        numeric escapes are treated as characters."""
        group_id = int(group_id)

        if abs(group_id) > 99:
            raise Exception(f"Only upto 99 group ids can be"
                            f" back-referenced, found {group_id}")
        return f"{accum_pattern}\\{group_id}"

    @append_sub_token
    def backref_group_name(self,
                           group_name: str  # noqa
                           ) -> Self:
        return self

    @classmethod
    def _call_backref_group_name(cls,
                                 group_name: str,
                                 accum_pattern: str | bytes,
                                 **kwargs  # noqa
                                 ) -> str | bytes:
        return f"{accum_pattern}(?P={group_name})"

    @append_sub_token
    def conditional_group(self,
                          group_id_or_name: int | str,  # noqa
                          yes_pattern: str | bytes | RegexBuilder,  # noqa
                          no_pattern: str | bytes | RegexBuilder  # noqa
                          ) -> Self:
        return self

    @classmethod
    def _call_conditional_group(cls,
                                group_id_or_name: int | str,
                                yes_pattern: str,
                                no_pattern: str,
                                accum_pattern: str | bytes,
                                **kwargs  # noqa
                                ) -> str | bytes:
        r"""Will try to match with yes-pattern if the group with given id or
        name exists, and with no-pattern if it doesn’t. no-pattern is optional
        and can be omitted. For example, (<)?(\w+@\w+(?:\.\w+)+)(?(1)>|$) is a
        poor email matching pattern, which will match with '<user@host.com>' as
        well as 'user@host.com', but not with '<user@host.com' nor
        'user@host.com>'.
        """
        return (f"{accum_pattern}"
                f"(?({group_id_or_name}){yes_pattern}|{no_pattern})")

    @classmethod
    def _lookaround(cls,
                    sub_pattern: str,
                    positive: bool,
                    lookahead: bool,
                    accum_pattern: str | bytes,
                    **kwargs  # noqa
    ) -> str | bytes:
        return (accum_pattern
                + "(?"
                + ("" if lookahead else "<")
                + ("=" if positive else "!")
                + sub_pattern
                + ")")

    @append_sub_token
    def negative_lookahead(self,
                           sub_pattern: str | bytes | RegexBuilder  # noqa
                           ) -> Self:
        return self

    @classmethod
    def _call_negative_lookahead(cls,
                                 sub_pattern: str | bytes | RegexBuilder,
                                 accum_pattern: str | bytes,
                                 **kwargs  # noqa
    ) -> str | bytes:
        return cls._lookaround(sub_pattern=sub_pattern,
                               positive=False,
                               lookahead=True,
                               accum_pattern=accum_pattern)

    @append_sub_token
    def negative_lookbehind(self,
                            sub_pattern: str | bytes | RegexBuilder  # noqa
                            ) -> Self:
        return self

    @classmethod
    def _call_negative_lookbehind(cls,
                                  sub_pattern: str | bytes | RegexBuilder,
                                  accum_pattern: str | bytes,
                                  **kwargs  # noqa
                                  ) -> str | bytes:
        return cls._lookaround(sub_pattern=sub_pattern,
                               positive=False,
                               lookahead=False,
                               accum_pattern=accum_pattern)

    @append_sub_token
    def positive_lookahead(self,
                           sub_pattern: str | bytes | RegexBuilder  # noqa
                           ) -> Self:
        return self

    @classmethod
    def _call_positive_lookahead(cls,
                                 sub_pattern: str | bytes | RegexBuilder,
                                 accum_pattern: str | bytes,
                                 **kwargs  # noqa
                                 ) -> str | bytes:
        return cls._lookaround(sub_pattern=sub_pattern,
                               positive=True,
                               lookahead=True,
                               accum_pattern=accum_pattern)

    @append_sub_token
    def positive_lookbehind(self,
                            sub_pattern: str | bytes | RegexBuilder  # noqa
                            ) -> Self:
        return self

    @classmethod
    def _call_positive_lookbehind(cls,
                                  sub_pattern: str | bytes | RegexBuilder,
                                  accum_pattern: str | bytes,
                                  **kwargs  # noqa
                                  ) -> str | bytes:
        return cls._lookaround(sub_pattern=sub_pattern,
                               positive=True,
                               lookahead=False,
                               accum_pattern=accum_pattern)

    @append_sub_token
    def append(self,
               sub_pattern: str | bytes | RegexBuilder  # noqa
               ) -> Self:
        return self

    @classmethod
    def _call_append(cls,
                     sub_pattern: str | bytes | RegexBuilder,
                     accum_pattern: str | bytes) -> str | bytes:
        return accum_pattern + sub_pattern

    @append_sub_token
    def prepend(self,
                sub_pattern: str | bytes | RegexBuilder  # noqa
                ) -> Self:
        return self

    @classmethod
    def _call_prepend(cls,
                      sub_pattern: str | bytes | RegexBuilder,
                      accum_pattern: str | bytes) -> str | bytes:
        return sub_pattern + accum_pattern

    def mode(self,
             sub_pattern: str,
             *,
             ascii_: bool = False,
             ignorecase: bool = False,
             locale: bool = False,
             multiline: bool = False,
             dotall: bool = False,
             verbose: bool = False,
             unset_ignorecase: bool = False,
             unset_multiline: bool = False,
             unset_dotall: bool = False,
             unset_verbose: bool = False) -> str:
        set_str_flags = self.flags_as(
            in_flags={"ascii_": ascii_,
                      "ignorecase": ignorecase,
                      "locale": locale,
                      "multiline": multiline,
                      "dotall": dotall,
                      "verbose": verbose
                      },
            out_flags_as="str")
        unset_str_flags = self.inline_unset_flags(
            ignorecase=unset_ignorecase,
            multiline=unset_multiline,
            dotall=unset_dotall,
            verbose=unset_verbose
        )
        str_flags = f"{set_str_flags}{unset_str_flags}"
        return f"(?{str_flags}:{sub_pattern})" if str_flags else sub_pattern

    @append_sub_token
    def range(self,
              from_: str | bytes,  # noqa
              to: str | bytes  # noqa
              ) -> Self:
        return self

    @classmethod
    def _call_range(cls,
                    from_: str | bytes,
                    to: str | bytes,
                    accum_pattern: str | bytes,
                    **kwargs  # noqa
                    ) -> str | bytes:
        return accum_pattern + f"{from_}-{to}"

    @append_sub_token
    def quantifier(self,
                   exactly: int | None = None,
                   min_times: int | None = None,
                   max_times: int | None = None,
                   lazy: bool = False,
                   possessive: bool = False) -> Self:

        if (exactly is not None
                and not (min_times is None and max_times is None)):
            raise ValueError("'exactly' and  'min_times', 'max_times' are"
                             " mutually exclusive")

        if lazy and possessive:
            raise ValueError("'lazy' and  'possessive' are mutually exclusive")

        return self

    @classmethod
    def _call_quantifier(cls,
                         exactly: int | None,
                         min_times: int | None,
                         max_times: int | None,
                         lazy: bool,
                         possessive: bool,
                         accum_pattern: str | bytes,
                         **kwargs  # noqa
    ) -> str | bytes:
        if exactly:
            min_times = max_times = exactly

        if min_times is None:
            min_times = 0

        if min_times == max_times:
            quantifier_str = f"{{{min_times}}}"
        elif min_times == 0:
            quantifier_str = "*" if max_times is None \
                else "?" if max_times == 1 \
                else f"{{,{max_times}}}"
        elif max_times is None:
            quantifier_str = "+" if min_times == 1 else f"{{{min_times},}}"
        else:
            quantifier_str = f"{{{min_times},{max_times}}}"

        if lazy:
            quantifier_str = f"{quantifier_str}?"
        elif possessive:
            quantifier_str = f"{quantifier_str}+"

        return accum_pattern + quantifier_str

    @property
    def flags(self) -> re.RegexFlag:
        return self.flags_as(out_flags_as="re")

    @flags.setter
    def flags(self, value: re.RegexFlag) -> None:
        self.flags_as(in_flags=value)

    @property
    def inline_flags(self) -> str:
        return self.flags_as(out_flags_as="str")


def _ltrim_chars(text: str, min_length: int, ltrim_char) -> str:
    len_text = len(text)
    while True:
        if len_text > min_length and text[0] == ltrim_char:
            text = text[1:]
            len_text -= 1
        else:
            break
    return text


def _lfill_chars(text: str, min_length: int, lfill_char: str) -> str:
    len_text = len(text)
    lfill_char = lfill_char * (min_length - len_text) \
        if len_text < min_length \
        else ""
    return f"{lfill_char}{text}"
