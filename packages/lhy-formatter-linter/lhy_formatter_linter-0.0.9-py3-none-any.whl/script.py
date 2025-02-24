import argparse
import pathlib
import sys

from format import format_code
from lint import lint_code


def parse_command_line(argv):
    parser = argparse.ArgumentParser(
        description='code formatter and linter.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    subparsers = parser.add_subparsers(dest='function', required=True)

    # Create a subparser for the format function
    format_parser = subparsers.add_parser('format', help='Format code')

    required_args = format_parser.add_argument_group('required arguments')

    required_args.add_argument(
        '-p',
        '--project-root-dir',
        required=True,
        type=pathlib.Path,
        help='Path to your project root directory folder.')

    optional_args = format_parser.add_argument_group('optional arguments')

    optional_args.add_argument('-l',
                               '--languages',
                               choices=['cxx', 'python', 'cmake'],
                               nargs="+",
                               default=['cxx', 'python', 'cmake'],
                               help='Which languages to format')
    optional_args.add_argument(
        '-id',
        '--ignore-dirs',
        nargs="+",
        type=pathlib.Path,
        help='Path of directories where formater ignores')

    optional_args.add_argument(
        '-if',
        '--ignore-file',
        type=pathlib.Path,
        help='Path of directories where formater ignores')

    optional_args.add_argument('-v',
                               '--verbose',
                               action='store_true',
                               help='enable verbose mode')
    optional_args.add_argument('-d',
                               '--dry-run',
                               action='store_true',
                               help='enable dry-run mode')

    cmake_args = format_parser.add_argument_group(
        'optional cmake format arguments')
    cmake_args.add_argument('--cmake-format-config',
                            type=pathlib.Path,
                            help='Path of cmake format custom config file')
    cxx_args = format_parser.add_argument_group(
        'optional c++ format arguments')
    cxx_args.add_argument('--clang-format-config',
                          type=pathlib.Path,
                          help='Path of clang format custom config file')
    python_args = format_parser.add_argument_group(
        'optional python format arguments')
    python_args.add_argument('--yapf-config',
                             type=pathlib.Path,
                             help='Path of yapf custom config file')
    python_args.add_argument('--isort-config',
                             type=pathlib.Path,
                             help='Path of isort custom config file')

    # Create a subparser for the lint function
    lint_parser = subparsers.add_parser('lint', help='Lint code')
    required_args = lint_parser.add_argument_group('required arguments')
    required_args.add_argument(
        '-p',
        '--project-root-dir',
        required=True,
        type=pathlib.Path,
        help='Path to your project root directory folder.')

    optional_args = lint_parser.add_argument_group('optional arguments')

    optional_args.add_argument('-l',
                               '--languages',
                               choices=['cxx', 'python', 'cmake'],
                               nargs="+",
                               default=['cxx', 'python', 'cmake'],
                               help='Which languages to lint')
    optional_args.add_argument(
        '-id',
        '--ignore-dirs',
        nargs="+",
        type=pathlib.Path,
        help='Path of directories where formater ignores')

    optional_args.add_argument(
        '-if',
        '--ignore-file',
        type=pathlib.Path,
        help='Path of directories where formater ignores')

    optional_args.add_argument('-v',
                               '--verbose',
                               action='store_true',
                               help='enable verbose mode')
    optional_args.add_argument('-d',
                               '--dry-run',
                               action='store_true',
                               help='enable dry-run mode')

    cmake_args = lint_parser.add_argument_group(
        'optional cmake lint arguments')
    cmake_args.add_argument('--cmake-lint-config',
                            type=pathlib.Path,
                            help='Path of cmake lint custom config file')
    cxx_args = lint_parser.add_argument_group('optional c++ format arguments')
    cxx_args.add_argument('--clang-tidy-config',
                          type=pathlib.Path,
                          help='Path of clang tidy custom config file')
    python_args = lint_parser.add_argument_group(
        'optional python format arguments')
    python_args.add_argument('--flake8-config',
                             type=pathlib.Path,
                             help='Path of flake8 custom config file')

    return parser.parse_args(argv)


def main():
    args = parse_command_line(sys.argv[1:])
    if args.function == 'format':
        format_code(args)
    elif args.function == 'lint':
        lint_code(args)


if __name__ == '__main__':
    main()
