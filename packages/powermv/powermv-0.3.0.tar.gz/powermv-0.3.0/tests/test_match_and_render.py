import re

import jinja2
import pytest

from powermv.matching import RegexMatcher
from powermv.rendering import Jinja2Renderer


def test_jinja2_template_experiments():
    env = jinja2.Environment()

    t = env.from_string("file-{{i}}.txt")
    out = t.render(i=2)

    assert out == "file-2.txt"

    t = env.from_string("file-{{i+1}}.txt")
    out = t.render(i=2)

    assert out == "file-3.txt"

    t = env.from_string("file-{{'{:02}'.format(i+1)}}.txt")
    out = t.render(i=2)

    assert out == "file-03.txt"


def test_re_match_as_jinja2_context():
    env = jinja2.Environment()

    input = "file-1.txt"
    p = r"file-(?P<num>\d).txt"

    m = re.match(p, input)

    assert m

    t = env.from_string("new-{{num}}.txt")
    out = t.render(g=m.groups(), **m.groupdict())

    assert out == "new-1.txt"


def test_regex_matcher():
    matcher = RegexMatcher(r"file-(.*)\.txt")

    ctx = matcher.get_match_tokens("file-xyz.txt")
    assert ctx["_1"] == "xyz"

    ctx = matcher.get_match_tokens("file-012.txt")
    assert ctx["_1"] == 12

    matcher = RegexMatcher(r"file-(?P<num>.*)\.txt")

    ctx = matcher.get_match_tokens("file-xyz.txt")
    assert ctx["_1"] == "xyz"
    assert ctx["num"] == "xyz"

    ctx = matcher.get_match_tokens("file-012.txt")
    assert ctx["_1"] == 12
    assert ctx["num"] == 12


def test_jinja_renderer():
    renderer = Jinja2Renderer("")

    ctx = {"one": 1, "two": 2}
    txt = renderer.render(ctx)
    assert txt == ""

    renderer = Jinja2Renderer("file-{{one}}.txt")
    txt = renderer.render(ctx)
    assert txt == "file-1.txt"
    txt = renderer.render({"one": 11})
    assert txt == "file-11.txt"

    renderer = Jinja2Renderer("file-{{one|pad(3)}}.txt")
    txt = renderer.render(ctx)
    assert txt == "file-001.txt"
    txt = renderer.render({"one": 11})
    assert txt == "file-011.txt"

    renderer = Jinja2Renderer("file-{{one|pad(4)}}.txt")
    txt = renderer.render(ctx)
    assert txt == "file-0001.txt"
    txt = renderer.render({"one": 11})
    assert txt == "file-0011.txt"


def test_python_regexs():
    assert re.match("one", "one and two")
    with pytest.raises(Exception):
        assert re.match("one", "zero and one and two")
    assert re.search("one", "zero and one and two")


def test_match_render_pairings():
    matcher = RegexMatcher(r"file-(.*)\.txt")
    renderer = Jinja2Renderer("{{_1|pad(5)}}-file.txt")

    text = renderer.render(matcher.get_match_tokens("file-5.txt"))

    assert text == "00005-file.txt"

    matcher = RegexMatcher(r"file-(.*)\.txt")
    renderer = Jinja2Renderer("{{_1|inc|pad(5)}}-file.txt")

    text = renderer.render(matcher.get_match_tokens("file-5.txt"))

    assert text == "00006-file.txt"


def test_matching_parts_of_file():
    matcher = RegexMatcher(r"(\d)")

    toks = matcher.get_match_tokens("file-5.txt")
    assert "_0" in toks
    assert toks["_0"] == "5"
    assert "_1" in toks
    assert toks["_1"] == 5
