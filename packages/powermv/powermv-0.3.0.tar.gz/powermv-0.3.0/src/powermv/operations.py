import shutil
from pathlib import Path

import networkx


class File(Path):
    pass


class Dir(Path):
    def is_dir(self):
        return True


def make_path(f: str | Path):
    if type(f) is Path:
        # argument is a path.
        # check if the path is a directory,
        # which will only be true if it exists already.
        if f.is_dir():
            return Dir(f)
        # otherwise assume its a file.
        return File(f)

    # argument is a string.
    # check to see if the name ends with a "/" OR
    # if it is a directory that already exists.
    if str(f).endswith("/") or Path(f).is_dir():
        return Dir(f)

    return File(f)


class MoveOp:
    """
    A single move operations. A move operations consists of an input and an output.
    """

    def __init__(self, input: str | Path, output: str):
        self.__input = make_path(input)  # .absolute()
        self.__output = make_path(output)  # .absolute()
        self.__move_input_into_ouput = False
        if self.__input.is_dir() and not self.__output.is_dir():
            raise RuntimeError(
                f"Cannot move a directory ({self.__input}) to a file ({self.__output}). Did you forget a '/' at the end of the output name?"
            )

        if not self.__input.is_dir() and self.__output.is_dir():
            self.__output = self.__output / self.__input.name

    @property
    def input(self):
        return self.__input

    def enable_move_input_into_output(self):
        self.__move_input_into_ouput = True

    def disable_move_input_into_output(self):
        self.__move_input_into_ouput = False

    @property
    def output(self):
        return self.__output

    def __repr__(self):
        return f"MoveOp({self.id})"

    def __str__(self):
        # we can just forward to id for now, but if we every start using
        # something that does not show the file rename for our id, we
        # will need to update this.
        return self.id

    @property
    def id(self):
        return f"{self.input}>>{self.output}"

    def need_to_make_output_parent(self):
        if not self.__output.parent.exists():
            return True
        return False

    def exec(self):
        """
        Execute move.
        """
        if self.need_to_make_output_parent():
            self.__output.parent.mkdir(parents=True)
        if (
            self.__output.is_dir()
            and not self.__output.exists()
            and self.__move_input_into_ouput
        ):
            self.__output.mkdir()

        shutil.move(self.__input, self.__output)


class MoveOpSet:
    def __init__(self):
        self.__ops: list[MoveOp] = list()
        self.__graph = networkx.DiGraph()

    def __len__(self):
        return len(self.__ops)

    @property
    def graph(self):
        return self.__graph

    def add(self, op: MoveOp):
        if op in self.__ops:
            return

        self.__ops.append(op)
        self.__graph.add_node(op)
        # if any operations have in input path that is equal to this operation's output
        # path, then this operation should be executed first and we say that those operations
        # _depend_ on this one.
        for o in self.iter_ops(lambda o: o.input == op.output):
            self.__graph.add_edge(o, op)
        # likewise, this operation will depend on any operations
        # that have an output path equal to its input path.
        for o in self.iter_ops(lambda o: o.output == op.input):
            self.__graph.add_edge(op, o)

    def replace(self, old_op: MoveOp, new_op: MoveOp):
        if old_op in self.__ops:
            idx = self.__ops.index(old_op)
            del self.__ops[idx]
        self.add(new_op)

    def order(self):
        ops = []
        graph = self.graph.copy()
        in_degrees = dict(graph.in_degree)
        graph_size = len(in_degrees)
        while len(in_degrees) > 0:
            for node, degrees in in_degrees.items():
                if degrees == 0:  # this node has no dependencies
                    ops.append(node)
                    graph.remove_node(node)  # prune from graph
            # repeat
            in_degrees = dict(graph.in_degree)
            if len(in_degrees) == graph_size:
                msg = "Could not resolve dependencies. These move operations all have a dependency (the operation input file has the same name as the output file of another operation) on one of the others: "
                msg += ", ".join(sorted([str(n) for n in in_degrees]))

                raise RuntimeError(msg)
            graph_size = len(in_degrees)

        self.__ops = ops

    def exec(self):
        for op in self.iter_ops():
            op.exec()

    def iter_ops(self, cond=lambda op: True):
        """
        Return all move operations. If `cond` is given, only operations
        that return true when passed to `cond` will be returned.
        """
        for op in self.__ops:
            if cond(op):
                yield op

    def iter_ops_with_missing_input(self):
        """
        Return all move operations with an input that does not exist.
        """
        return self.iter_ops(lambda op: not op.input.exists())

    def iter_ops_with_dir_input(self):
        """
        Return all move operations that have a directory input.
        """
        return self.iter_ops(lambda op: op.input.is_dir())

    def iter_ops_with_dir_output(self):
        """
        Return all move operations that have a directory output.
        """
        return self.iter_ops(lambda op: op.output.is_dir())
