import argparse
import platform

def get_current_python():
    major, minor, _ = platform.python_version_tuple()
    return f"{major}.{minor}"

def configure_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument(
        "-project-name", required=True, type=str, help="Name of Project to create"
    )
    parser.add_argument(
        "-desc",
        required=True,
        dest="description",
        type=str,
        help="Short description of the App",
    )
    parser.add_argument(
        '-package-name', required=True, type=str, help="Name of new package to create"
    )
    parser.add_argument('-command-name', required=True, type=str, help="Name of command to create")
    parser.add_argument(
        "-owner-email", required=True, type=str, help="Email of app owner"
    )
    parser.add_argument(
        "--version", default="0.0.1", type=str, help="Version of the newly created App"
    )
    parser.add_argument(
        "--license", default="Proprietary", type=str, help="License to use for the App"
    )
    parser.add_argument(
        "--homepage-url",
        default="https://example.com",
        type=str,
        help="URL for Documentation page of the App",
    )
    parser.add_argument(
        "--repository-url",
        default="https://example.com",
        type=str,
        help="URL for Git Repository of the App",
    )
    parser.add_argument(
        "--python-version",
        default=get_current_python(),
        type=str,
        help="Python version of the App",
    )
    return parser