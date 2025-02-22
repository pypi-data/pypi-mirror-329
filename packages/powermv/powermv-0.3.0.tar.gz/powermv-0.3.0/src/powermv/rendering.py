import jinja2

from . import utils


class Renderer:
    pass


class Jinja2Renderer:
    def __init__(self, template):
        self.__env = jinja2.Environment()
        self.__template_text = template

        def pad(input, num):
            return ("{:0" + str(num) + "}").format(input)

        def inc(input, num=1):
            return input + num

        def dec(input, num=1):
            return input - num

        self.__env.filters["pad"] = pad
        self.__env.filters["inc"] = inc
        self.__env.filters["dec"] = dec
        self.__env.filters["CamelCase"] = utils.to_camel_case
        self.__env.filters["camel_case"] = utils.to_camel_case
        self.__env.filters["SnakeCase"] = utils.to_snake_case
        self.__env.filters["snake_case"] = utils.to_snake_case
        self.__env.filters["SpaceCase"] = utils.to_space_case
        self.__env.filters["space_case"] = utils.to_space_case
        self.__template = self.__env.from_string(self.__template_text)

    def render(self, ctx: dict):
        if ctx is None:
            ctx = {}
        return self.__template.render(**ctx)
