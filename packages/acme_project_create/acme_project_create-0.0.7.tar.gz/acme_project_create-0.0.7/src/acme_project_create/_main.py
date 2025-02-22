import argparse
import os
import shutil
import sys
import tempfile

import jinja2


def add_template_args(
    parser: argparse.ArgumentParser, template_dir_path: str
) -> argparse.ArgumentParser:
    """Adds arguments to a parser using template_mani.configure_parser function in template directory.

    Args:
        parser (argparse.ArgumentParser): The argument parser to which template arguments will be added.
        template_dir_path (str): The path to the directory containing the template manifest.

    Returns:
        argparse.ArgumentParser: The parser with the template arguments added.

    Raises:
        ValueError: If `template_manifest.py` is not found in the template directory.
    """
    sys.path.append(template_dir_path)
    try:
        import template_manifest  # type: ignore
    except ImportError:
        raise ValueError("template_manifest.py not found in the template directory.")
    parser = template_manifest.configure_parser(parser)
    return parser


def copy_template_dir(template_dir_path: str) -> tempfile.TemporaryDirectory:
    """Copies the contents of the specified template directory to a temporary directory, excluding 'template_manifest.py' and any `__pycache__` directories.

    Args:
        template_dir_path (str): The path to the template directory to be copied.

    Returns:
        tempfile.TemporaryDirectory: A temporary directory containing the copied contents.

    Raises:
        FileNotFoundError: If the specified template directory does not exist
    """
    # temp dir is used to make sure only contents inside the template need to be scanned
    temp_dir = tempfile.TemporaryDirectory()
    shutil.copytree(template_dir_path, temp_dir.name, dirs_exist_ok=True)
    # Delete template_manifest.py
    template_manifest_path = os.path.join(temp_dir.name, "template_manifest.py")
    os.remove(template_manifest_path)
    # Remove __pycache__ directories if they exist in the target directory
    pycache_path = os.path.join(temp_dir.name, "__pycache__")
    if os.path.exists(pycache_path):
        shutil.rmtree(pycache_path)
    return temp_dir


def render_template_dirs(target_dir, args):
    """Recursively finds and renames directories in the target directory that contain
    variables in their names.

    This function searches through all directories within the specified target
    directory. If a directory name contains variables enclosed in double braces
    (e.g., {{variable}}), it replaces the double braces with single braces and
    formats the name using the provided arguments. The directory is then renamed
    to the new formatted name.

    Args:
        target_dir (str): The root directory to start the search.
        args (object): An object containing the variables to be used for formatting
                       the directory names.
    Raises:
        KeyError: If a variable in the directory name is not found in the provided
                  arguments.
    """
    for root, dirs, _ in os.walk(target_dir, topdown=False):
        for dir_name in dirs:
            if dir_name.startswith("{{") and dir_name.endswith("}}"):
                try:
                    # Preprocess the directory name to replace double braces with single braces
                    new_dir_name = dir_name.replace("{{", "{").replace("}}", "}")
                    new_dir_name = new_dir_name.format(**vars(args))
                except KeyError as e:
                    raise KeyError(
                        f"Missing argument for {e} in directory name formatting."
                    )
                new_dir_path = os.path.join(root, new_dir_name)
                dir_path = os.path.join(root, dir_name)
                os.rename(dir_path, new_dir_path)


def render_template_files(target_dir, args):
    """Renders Jinja2 template files in the target directory.

    This function searches for all files in the specified target directory that have a `.j2template` extension,
    renders them using the provided arguments, and saves the rendered content back to the same location without
    the `.j2template` extension. The original `.j2template` files are removed after rendering.

    Args:
        target_dir (str): The directory to search for `.j2template` files.
        args (Namespace): The arguments to use for rendering the templates. These should be passed as a Namespace
                          object, where the attributes of the Namespace are used as variables in the templates.

    Raises:
        OSError: If there is an error reading or writing files in the target directory.
    """
    for root, _, files in os.walk(target_dir):
        for file_name in files:
            if file_name.endswith(".j2template"):
                file_path = os.path.join(root, file_name)
                with open(file_path, "r") as file:
                    template_content = file.read()
                template = jinja2.Template(template_content)
                try:
                    rendered_template = template.render(**vars(args))
                except jinja2.exceptions.UndefinedError as e:
                    raise KeyError(
                        f"Missing argument for {file_path} in template rendering."
                    ) from e
                except Exception as e:
                    raise OSError(f"Error rendering template {file_path}.") from e
                new_file_path = file_path.replace(".j2template", "")
                with open(new_file_path, "w") as file:
                    file.write(rendered_template)
                os.remove(file_path)


def move_to_target_dir(temp_dir, target_dir):
    """Moves all files and directories inside the temp directory to the target directory"""
    for item in os.listdir(temp_dir):
        source_path = os.path.join(temp_dir, item)
        destination_path = os.path.join(target_dir, item)
        shutil.move(source_path, destination_path)


def main_logic(args):
    temp_dir = copy_template_dir(args.template_dir_path)
    render_template_dirs(temp_dir.name, args)
    render_template_files(temp_dir.name, args)
    move_to_target_dir(temp_dir.name, args.target_dir)
    temp_dir.cleanup()


def get_default_template_dir_path():
    current_file_path = os.path.abspath(__file__)
    current_dir_path = os.path.dirname(current_file_path)
    return os.path.join(current_dir_path, "template")


def parse_args():
    parser = argparse.ArgumentParser(prog="apc", description="Create a new project")

    parser.add_argument(
        "--template-dir-path",
        required=False,
        type=str,
        help="Path to the template directory",
        default=get_default_template_dir_path(),
    )
    parser.add_argument(
        "-target-dir",
        required=True,
        type=str,
        help="Path to the directory where the new project will be created",
    )
    args, _ = parser.parse_known_args()
    parser = add_template_args(parser, args.template_dir_path)
    return parser.parse_args(sys.argv[1:], namespace=args)


def main():
    args = parse_args()
    main_logic(args)


if __name__ == "__main__":
    main()
