import os
import pathlib
from typing import List, Optional
import mimetypes
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern


def read_exclude_patterns(exclude_file: str) -> PathSpec:
    """
    Read exclude patterns from a file and create a PathSpec object.

    Args:
        exclude_file (str): Path to the exclude patterns file

    Returns:
        PathSpec: PathSpec object for pattern matching
    """
    try:
        with open(exclude_file, 'r') as f:
            # Filter out empty lines and comments
            patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return PathSpec.from_lines(GitWildMatchPattern, patterns)
    except FileNotFoundError:
        return PathSpec.from_lines(GitWildMatchPattern, [])


def is_binary_file(file_path: str) -> bool:
    """
    Determine if a file is binary.
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        return True
    return not mime_type.startswith('text/')


def generate_tree(
    root_path: pathlib.Path,
    prefix: str = "",
    is_last: bool = True,
    exclude_binary: bool = True,
    include_extensions: Optional[List[str]] = None,
    exclude_patterns: Optional[PathSpec] = None,
) -> str:
    """
    Generate a tree-style representation of the directory structure.

    Args:
        root_path (pathlib.Path): The root directory path
        prefix (str): Prefix for the current line (used for recursion)
        is_last (bool): Whether this is the last item in the current directory
        exclude_binary (bool): Whether to exclude binary files
        include_extensions (List[str], optional): List of extensions to include
        exclude_patterns (PathSpec, optional): PathSpec object for pattern matching

    Returns:
        str: Tree-style representation of the directory
    """
    if not root_path.exists():
        return ""

    # Get relative path for pattern matching
    if prefix == "":  # root level
        relative_path = "."
    else:
        try:
            relative_path = str(root_path.relative_to(root_path.parent))
        except ValueError:
            return ""

    # Check if this path should be excluded
    # Always check against the root path first
    abs_root_path = root_path if prefix == "" else root_path.parent
    try:
        root_relative_path = str(root_path.relative_to(abs_root_path))
        if exclude_patterns and exclude_patterns.match_file(root_relative_path):
            return ""
    except ValueError:
        pass

    # Determine the marker and next prefix
    marker = "└── " if is_last else "├── "
    next_prefix = prefix + ("    " if is_last else "│   ")

    # Get the name of the current path
    name = "." if prefix == "" else root_path.name

    # Start with the current directory/file
    tree = prefix + marker + name

    # If it's a directory, process its contents
    if root_path.is_dir():
        tree += "/\n"  # Add slash for directories

        # Get and sort the contents
        contents = list(root_path.iterdir())
        contents.sort(key=lambda x: (not x.is_dir(), x.name.lower()))

        # Filter contents based on criteria
        filtered_contents = []
        for item in contents:
            # Get the relative path from the root directory for pattern matching
            try:
                relative_item_path = str(item.relative_to(abs_root_path))
                if exclude_patterns and exclude_patterns.match_file(relative_item_path):
                    continue
            except ValueError:
                continue

            if item.is_dir():
                filtered_contents.append(item)
            elif item.is_file():
                if include_extensions and item.suffix not in include_extensions:
                    continue
                if exclude_binary and is_binary_file(str(item)):
                    continue
                filtered_contents.append(item)

        # Generate tree for each item
        for i, item in enumerate(filtered_contents):
            is_last_item = i == len(filtered_contents) - 1
            tree += generate_tree(
                item,
                next_prefix,
                is_last_item,
                exclude_binary,
                include_extensions,
                exclude_patterns
            )
    else:
        tree += "\n"

    return tree


def dump_directory(
    root_path: str,
    output_path: str,
    exclude_binary: bool = True,
    include_extensions: Optional[List[str]] = None,
    show_tree: bool = True,
    show_line_numbers: bool = True,
    exclude_file: Optional[str] = None,
) -> None:
    """
    Dump the contents of a directory into a single file, including a tree structure.

    Args:
        root_path (str): Root directory path to start exploration
        output_path (str): Output file path
        exclude_binary (bool): Whether to exclude binary files
        include_extensions (List[str], optional): List of extensions to include
        show_tree (bool): Whether to show the directory tree structure
        show_line_numbers (bool): Whether to show line numbers
        exclude_file (str, optional): Path to file containing exclude patterns

    Returns:
        None
    """
    root_path = pathlib.Path(root_path).resolve()
    exclude_patterns = read_exclude_patterns(exclude_file) if exclude_file else None

    with open(output_path, 'w', encoding='utf-8') as f:
        # Add the tree structure if requested
        if show_tree:
            tree = generate_tree(
                root_path,
                exclude_binary=exclude_binary,
                include_extensions=include_extensions,
                exclude_patterns=exclude_patterns
            )
            f.write("# Directory structure:\n")
            for line in tree.split('\n'):
                if line:
                    f.write(f"# {line}\n")
            f.write("\n")

        # Then write the file contents
        for path in root_path.rglob('*'):
            if not path.is_file():
                continue

            try:
                relative_path = str(path.relative_to(root_path))
            except ValueError:
                continue

            if exclude_patterns and exclude_patterns.match_file(relative_path):
                continue

            if include_extensions and path.suffix not in include_extensions:
                continue

            if exclude_binary and is_binary_file(str(path)):
                continue

            try:
                # Skip the output file itself
                if relative_path == os.path.basename(output_path):
                    continue

                # Check if file is empty
                if os.path.getsize(path) == 0:
                    continue

                # Read file contents
                with open(path, 'r', encoding='utf-8') as content_file:
                    # Read first chunk to check if file actually has content
                    content = content_file.read(4096)  # Read first 4KB
                    if not content.strip():
                        continue

                    # File has content, write header
                    f.write(f"\n## {relative_path}\n\n")

                    # Write the first chunk we read
                    if show_line_numbers:
                        for line_num, line in enumerate(content.splitlines(True), 1):
                            f.write(f"{line_num} | {line}")
                    else:
                        f.write(content)

                    # Continue reading and writing the rest of the file
                    while True:
                        content = content_file.read(4096)
                        if not content:
                            break
                        if show_line_numbers:
                            for line_num, line in enumerate(content.splitlines(True), line_num + 1):
                                f.write(f"{line_num} | {line}")
                        else:
                            f.write(content)

            except (UnicodeDecodeError, PermissionError):
                continue


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Dump directory contents to a file')
    parser.add_argument('root_path', help='Root directory to dump')
    parser.add_argument('output_path', help='Output file path')
    parser.add_argument('--exclude-binary', action='store_true', help='Exclude binary files')
    parser.add_argument('--extensions', nargs='+', help='Include only specific extensions')
    parser.add_argument('--no-tree', action='store_true', help='Do not include directory tree structure')
    parser.add_argument('--no-line-numbers', action='store_false', dest='show_line_numbers', help='Do not include line numbers')
    parser.add_argument('--ignore-file', help='Path to file containing ignore patterns')
    parser.set_defaults(show_line_numbers=True)

    args = parser.parse_args()
    dump_directory(
        args.root_path,
        args.output_path,
        exclude_binary=args.exclude_binary,
        include_extensions=args.extensions,
        show_tree=not args.no_tree,
        show_line_numbers=args.show_line_numbers,
        exclude_file=args.ignore_file
    )


if __name__ == '__main__':
    main()
