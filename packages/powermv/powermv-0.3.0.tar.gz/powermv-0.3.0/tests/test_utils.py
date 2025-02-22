from powermv.utils import to_camel_case, to_snake_case, to_space_case


def test_to_camel_case():
    assert to_camel_case("one_two") == "OneTwo"
    assert to_camel_case("one_two_three") == "OneTwoThree"
    assert to_camel_case("one_two_three_") == "OneTwoThree"
    assert to_camel_case("_one_two_three_") == "OneTwoThree"
    assert to_camel_case("_one__two__three_") == "OneTwoThree"
    assert to_camel_case("one two") == "OneTwo"
    assert to_camel_case("OneTwo") == "OneTwo"


def test_to_snake_case():
    assert to_snake_case("OneTwo") == "one_two"
    assert to_snake_case("OneTwoThree") == "one_two_three"
    assert to_snake_case("_one_two_three_") == "one_two_three"
    assert to_snake_case("one two three") == "one_two_three"


def test_to_space_case():
    assert to_space_case("OneTwo") == "one two"
    assert to_space_case("OneTwoThree") == "one two three"
    assert to_space_case("_one_two_three_") == "one two three"
    assert to_space_case("one two three") == "one two three"
