def to_camel_case(text: str):
    out = []

    new_word = True
    for char in text.replace(" ", "_"):
        if char == "_":
            new_word = True
            continue
        if new_word:
            out.append(char.upper())
            new_word = False
            continue
        out.append(char)

    return "".join(out)


def to_snake_case(text: str):
    out = []

    # its easier to convert to camel case first
    # so that leading and consective '_' and ' ' chars will be merged.
    for char in to_camel_case(text):
        if char.isupper():
            out.append("_")
            out.append(char.lower())
            continue

        out.append(char)

    # the first char will be a '_' since the first char of to_camel_case(text) will be
    # a capital letter. we want to discare it.
    return "".join(out[1:])


def to_space_case(text: str):
    return to_snake_case(text).replace("_", " ")
