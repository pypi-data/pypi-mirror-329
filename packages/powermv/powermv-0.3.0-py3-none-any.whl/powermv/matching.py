import re


class Matcher:
    pass


class RegexMatcher(Matcher):
    def __init__(self, pattern: str):
        """
        A wrapper for matching strings with regular expressions and
        getting match groups out.

        Parameters
        ==========

        pattern
            A regular expression pattern. If the regex contains groups,
            these will be returned in a dictionary from `get_match_tokens(...)`

        partial_match
            If True, regex will match parts of a string. If False, regex must match
            the entire string. Setting partial_match to False will add '^' and '$'
            to the beginning and end of the regex pattern if they are not already
            present.
        """
        self.__pattern = pattern
        self.__regex = re.compile(pattern)

    def get_match_tokens(self, text: str):
        toks = {}
        m = self.__regex.search(text)
        if m:
            unnamed_groups = m.groups()
            named_groups = m.groupdict()

            for k in named_groups:
                val = named_groups[k]
                try:
                    val = int(val)
                except Exception:
                    pass

                toks[k] = val

            for i, val in enumerate(unnamed_groups):
                try:
                    val = int(val)
                except Exception:
                    pass

                toks[f"_{i + 1}"] = val
            toks["_0"] = m.group(0)

        if toks == {}:
            return None

        return toks
