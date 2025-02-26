import pathlib

from utils import (DEFAULT_IGNORE_DIRS, exec_on_files, pasre_ignore_dirs,
                   print_exec_info, read_ignore_paths)


def format_code(args):
    assert args.project_root_dir.exists(), 'Path {} does not exist.'
    root_dir = args.project_root_dir.absolute()
    if args.verbose:
        print('root_dir:', root_dir)

    ignore_dirs_list = [
        pathlib.Path(root_dir, ign_dir) for ign_dir in DEFAULT_IGNORE_DIRS
    ]
    if args.ignore_dirs:
        assert isinstance(args.ignore_dirs,
                          list), 'invalid param --ignore-dirs: {}'.format(
                              args.ignore_dirs)
        ignore_dirs = pasre_ignore_dirs(args.ignore_dirs, root_dir)
        ignore_dirs_list += ignore_dirs

    if args.ignore_file:
        assert args.ignore_file.exists(
        ), '--ignore-file: {} does not exist'.format(args.ignore_file)
        ignore_dirs_from_file = read_ignore_paths(args.ignore_file, root_dir)
        ignore_dirs_list += ignore_dirs_from_file

    if args.verbose:
        print('ignore dirs: ', ignore_dirs_list)

    if 'cmake' in args.languages:
        cmake_format_args = [
            '-c', str(pathlib.Path(root_dir, args.cmake_format_config))
        ] if args.cmake_format_config else []

        num_failed, failed_commands = exec_on_files(
            ['cmake-format', '-i'],
            root_dir, ['*.cmake', 'CMakeLists.txt'],
            ignore_dirs_list,
            cmake_format_args,
            verbose=args.verbose,
            dry_run=args.dry_run)
        print_exec_info('cmake-format', num_failed, failed_commands)

    if 'cxx' in args.languages:
        clang_format_args = [
            '--style=file:{}'.format(
                str(pathlib.Path(root_dir, args.clang_format_config)))
        ] if args.clang_format_config else []

        num_failed, failed_commands = exec_on_files(
            ['clang-format', '-i'],
            root_dir, ['*.h', '*.hpp', '*.cpp', '*.cu'],
            ignore_dirs_list,
            clang_format_args,
            verbose=args.verbose,
            dry_run=args.dry_run)
        print_exec_info('clang-format', num_failed, failed_commands)

    if 'python' in args.languages:
        yapf_args = [
            '--style {}'.format(str(pathlib.Path(root_dir, args.yapf_config)))
        ] if args.yapf_config else []

        num_failed, failed_commands = exec_on_files(['yapf', '-i'],
                                                    root_dir, ['*.py'],
                                                    ignore_dirs_list,
                                                    yapf_args,
                                                    verbose=args.verbose,
                                                    dry_run=args.dry_run)
        print_exec_info('yapf', num_failed, failed_commands)

        isort_args = [
            '--settings-path {}'.format(
                str(pathlib.Path(root_dir, args.isort_config)))
        ] if args.isort_config else []

        num_failed, failed_commands = exec_on_files(['isort'],
                                                    root_dir, ['*.py'],
                                                    ignore_dirs_list,
                                                    isort_args,
                                                    verbose=args.verbose,
                                                    dry_run=args.dry_run)
        print_exec_info('isort', num_failed, failed_commands)
