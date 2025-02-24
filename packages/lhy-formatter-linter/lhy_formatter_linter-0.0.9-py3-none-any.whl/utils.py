import os
import pathlib
import re
import subprocess

DEFAULT_IGNORE_DIRS = ['.git', 'build', '.vscode', '.cache', '.pytest_cache']


def _get_exec_version(exec):
    check_cmd = [exec, '--version']
    try:
        output = subprocess.check_output(check_cmd).decode('utf-8')
        version = re.search(r'(\d+(?:\.\d+)*)', output).group(0)
        return version
    except subprocess.CalledProcessError:
        return None
    except AttributeError:
        return None


def print_exec_info(exec, num_failed, failed_commands):
    print('{} execution finished, {} failed'.format(exec, num_failed))
    if num_failed > 0:
        print('{} failed commands: {}'.format(exec, failed_commands))
    print('--------------------------------------')


def pasre_ignore_dirs(ignore_dirs, root_dir):
    ign_dirs = []
    if ignore_dirs:
        for ign_dir in ignore_dirs:
            abs_ign_dir = pathlib.Path(root_dir, ign_dir)
            if abs_ign_dir.exists():
                ign_dirs.append(abs_ign_dir)
            else:
                print('Warning: ignore dir {} is not valid.'.format(
                    str(abs_ign_dir)))
    return ign_dirs


def read_ignore_paths(file_path, root_dir):
    """
    Reads a text file where each line corresponds to a folder path.
    Returns a list of absolute directories to ignore.

    Args:
        file_path (pathlib.Path): Path to the text file containing
        folder paths.
        root_dir (pathlib.Path): Root directory to resolve relative paths.

    Returns:
        list: List of absolute directories to ignore.
    """
    try:
        with open(file_path, 'r') as file:
            # Read all lines in the file and strip leading/trailing whitespaces
            parsed_paths = [line.strip() for line in file.readlines()]
            parsed_paths = [path for path in parsed_paths if path != '']
            # Resolve relative paths to absolute paths using the root directory
            ignore_paths = [
                pathlib.Path(root_dir, path) for path in parsed_paths
            ]
            return ignore_paths
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []


def get_subfolders_recursive(path):
    """
    Returns a list of all subfolders in the given path, recursively.
    """
    subfolders = []
    for item in path.iterdir():
        if item.is_dir():
            subfolders.append(item)
            subfolders.extend(get_subfolders_recursive(item))
    return subfolders


def exec_on_files(exec_args,
                  root_dir,
                  expressions,
                  ignore_dirs,
                  other_args,
                  verbose=False,
                  dry_run=False):
    """
    Launch exec with given args on filtered files.
    Executable name is given as 1st argument

    Parameters
    ----------
    exec_args: list of string
        executable name and relative args.
    root_dir: string
        root directory pathname from which the search has to be launched.
    expressions: list of strings
        list of expressions defining the files on which executable has
        to be launched.
    ignore_dirs: list os strings
        list of directories in root_dir to exclude from search.
    other_args: list of strings
        list of other arguments to be passed to executable.
    """
    exec = exec_args[0]
    version_num = _get_exec_version(exec)
    if verbose:
        print('{} --version: {}'.format(exec, version_num))
    num_failed = 0
    failed_commands = []
    all_folders = get_subfolders_recursive(root_dir)
    all_folders.append(root_dir)
    filtered_folders = [
        folder for folder in all_folders if not any(
            folder.is_relative_to(ignore_dir) for ignore_dir in ignore_dirs)
    ]
    filtered_folders = list(set(filtered_folders))
    current_dir = os.getcwd()
    os.chdir(root_dir)
    if verbose:
        print('change work directory from {} to {}'.format(
            current_dir, root_dir))
    all_files = []
    for d in filtered_folders:
        for expr in expressions:
            files = list(map(str, d.glob(expr)))
            if files:
                all_files += files
                command_line = ' '.join(
                    map(str, exec_args + files + other_args))
                if verbose:
                    print(command_line)
                if dry_run:
                    print('dry-run: ' + command_line)
                else:
                    ret = subprocess.run(exec_args + files + other_args)
                    if ret.returncode != 0:
                        num_failed += 1
                        failed_commands.append(command_line)

    os.chdir(current_dir)
    if verbose:
        print('change work directory from {} to {}'.format(
            root_dir, current_dir))
    return num_failed, failed_commands
