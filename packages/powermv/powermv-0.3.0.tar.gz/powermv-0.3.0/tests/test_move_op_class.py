import pathlib

import pytest
from unittest_utils import working_dir

from powermv.operations import MoveOp


def test_construct(tmp_path):
    with working_dir(tmp_path):
        m1 = MoveOp("file-1.txt", "file-2.txt")
        m2 = MoveOp("file-1.log", "file-2.log")

        assert m1.id == "file-1.txt>>file-2.txt"
        assert m2.id == "file-1.log>>file-2.log"

        assert not m1.input.exists()
        assert not m1.output.exists()
        assert not m2.input.exists()
        assert not m2.output.exists()

        m1.input.write_text("HI")
        m2.input.write_text("HI")

        assert m1.input.exists()
        assert not m1.output.exists()
        assert m2.input.exists()
        assert not m2.output.exists()

        m1.exec()

        assert not m1.input.exists()
        assert m1.output.exists()
        assert m2.input.exists()
        assert not m2.output.exists()

        m2.exec()

        assert not m1.input.exists()
        assert m1.output.exists()
        assert not m2.input.exists()
        assert m2.output.exists()


def test_move_file_to_file(tmp_path):
    with working_dir(tmp_path):
        pathlib.Path("file-1.txt").write_text("HI")
        move = MoveOp("file-1.txt", "file-2.txt")

        assert not pathlib.Path("file-2.txt").exists()
        assert not move.need_to_make_output_parent()
        move.exec()
        assert pathlib.Path("file-2.txt").exists()
        assert pathlib.Path("file-2.txt").read_text() == "HI"


def test_move_file_to_dir(tmp_path):
    with working_dir(tmp_path):
        pathlib.Path("file-1.txt").write_text("HI")
        pathlib.Path("dir").mkdir()
        move = MoveOp("file-1.txt", "dir")

        assert move.output == pathlib.Path() / "dir/file-1.txt"

        assert pathlib.Path("dir").exists()
        assert not pathlib.Path("dir/file-1.txt").exists()
        assert not move.need_to_make_output_parent()
        move.exec()
        assert pathlib.Path("dir/file-1.txt").exists()
        assert pathlib.Path("dir/file-1.txt").read_text() == "HI"


def test_move_file_to_missing_dir(tmp_path):
    with working_dir(tmp_path):
        pathlib.Path("file-1.txt").write_text("HI")
        move = MoveOp("file-1.txt", "dir/")

        assert move.output == pathlib.Path("dir/file-1.txt")

        assert not pathlib.Path("dir").exists()
        assert not pathlib.Path("dir/file-1.txt").exists()
        assert move.need_to_make_output_parent()
        move.exec()
        assert pathlib.Path("dir").exists()
        assert pathlib.Path("dir/file-1.txt").exists()
        assert pathlib.Path("dir/file-1.txt").read_text() == "HI"


def test_move_dir_to_dir(tmp_path):
    with working_dir(tmp_path):
        pathlib.Path("dir1").mkdir()
        pathlib.Path("dir2").mkdir()
        pathlib.Path("dir1/file-1.txt").write_text("HI")

        move = MoveOp("dir1", "dir2")

        assert pathlib.Path("dir1").exists()
        assert pathlib.Path("dir2").exists()
        assert not pathlib.Path("dir2/dir1").exists()
        assert not move.need_to_make_output_parent()
        move.exec()
        assert not pathlib.Path("dir1").exists()
        assert pathlib.Path("dir2").exists()
        assert pathlib.Path("dir2/dir1").exists()
        assert pathlib.Path("dir2/dir1/file-1.txt").exists()


def test_move_dir_to_missing_dir(tmp_path):
    with working_dir(tmp_path):
        pathlib.Path("dir1").mkdir()
        pathlib.Path("dir1/file-1.txt").write_text("HI")

        move = MoveOp("dir1/", "dir2/")

        assert pathlib.Path("dir1").exists()
        assert not pathlib.Path("dir2").exists()
        assert not pathlib.Path("dir2/file-1.txt").exists()
        assert not move.need_to_make_output_parent()
        move.exec()
        assert not pathlib.Path("dir1").exists()
        assert pathlib.Path("dir2").exists()
        assert pathlib.Path("dir2/file-1.txt").exists()
    pass


def test_move_dir_to_file(tmp_path):
    with working_dir(tmp_path):
        with pytest.raises(RuntimeError) as e:
            m1 = MoveOp("dir/", "file.txt")
            m1.exec()

        assert "Did you forget a '/' at the end of the output name?" in str(e)
