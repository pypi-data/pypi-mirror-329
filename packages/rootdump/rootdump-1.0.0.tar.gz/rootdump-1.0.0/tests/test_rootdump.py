import os
import tempfile
import pathlib
from rootdump import dump_directory
import pytest


def test_dump_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_files = {
            "test1.txt": "Hello World",
            "subdir/test2.txt": "Test content",
            "test3.py": "print('Hello')"
        }

        for path, content in test_files.items():
            file_path = pathlib.Path(temp_dir) / path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)

        output_file = pathlib.Path(temp_dir) / "output.txt"
        dump_directory(temp_dir, str(output_file))

        result = output_file.read_text()

        # ファイル内容の確認
        for path, content in test_files.items():
            assert path in result
            assert content in result

        # ツリー構造の確認
        assert "# Directory structure:" in result
        assert "#     ├── subdir/" in result
        assert "#     │   └── test2.txt" in result


def test_exclude_binary():
    with tempfile.TemporaryDirectory() as temp_dir:
        binary_file = pathlib.Path(temp_dir) / "test.bin"
        binary_file.write_bytes(b'\x00\x01\x02\x03')

        text_file = pathlib.Path(temp_dir) / "test.txt"
        text_file.write_text("Hello")

        output_file = pathlib.Path(temp_dir) / "output.txt"
        dump_directory(temp_dir, str(output_file), exclude_binary=True)

        result = output_file.read_text()

        assert "test.bin" not in result
        assert "test.txt" in result
        assert "Hello" in result


def test_include_extensions():
    with tempfile.TemporaryDirectory() as temp_dir:
        files = {
            "test.txt": "Text content",
            "test.py": "print('Hello')",
            "test.md": "# Markdown"
        }

        for path, content in files.items():
            file_path = pathlib.Path(temp_dir) / path
            file_path.write_text(content)

        output_file = pathlib.Path(temp_dir) / "output.txt"
        dump_directory(
            temp_dir,
            str(output_file),
            include_extensions=[".txt", ".py"]
        )

        result = output_file.read_text()

        assert "test.txt" in result
        assert "test.py" in result
        assert "test.md" not in result


def test_show_tree_option():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_files = {
            "test1.txt": "Content 1",
            "subdir/test2.txt": "Content 2"
        }

        for path, content in test_files.items():
            file_path = pathlib.Path(temp_dir) / path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)

        output_file = pathlib.Path(temp_dir) / "output.txt"
        dump_directory(temp_dir, str(output_file), show_tree=False)

        result = output_file.read_text()

        assert "Directory structure:" not in result
        assert "└── " not in result
        assert "├── " not in result
        assert "test1.txt" in result
        assert "Content 1" in result
        assert "test2.txt" in result
        assert "Content 2" in result


def test_tree_format():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_files = {
            "a.txt": "A",
            "b/b1.txt": "B1",
            "b/b2.txt": "B2",
            "c/c1/c1.txt": "C1"
        }

        for path, content in test_files.items():
            file_path = pathlib.Path(temp_dir) / path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)

        output_file = pathlib.Path(temp_dir) / "output.txt"
        dump_directory(temp_dir, str(output_file))

        result = output_file.read_text()

        assert "# Directory structure:" in result
        assert "# └── ./" in result
        assert "#     ├── b/" in result
        assert "#     │   ├── b1.txt" in result
        assert "#     │   └── b2.txt" in result
        assert "#     ├── c/" in result
        assert "#     │   └── c1/" in result
        assert "#     │       └── c1.txt" in result
