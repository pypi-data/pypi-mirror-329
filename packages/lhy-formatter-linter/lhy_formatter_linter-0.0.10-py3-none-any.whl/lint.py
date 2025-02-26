import pathlib

from utils import (DEFAULT_IGNORE_DIRS, exec_on_files, pasre_ignore_dirs,
                   print_exec_info, read_ignore_paths)


def lint_code(args):
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
        cmake_lint_args = [
            '-c', str(pathlib.Path(root_dir, args.cmake_lint_config))
        ] if args.cmake_lint_config else []

        num_failed, failed_commands = exec_on_files(
            ['cmake-lint'],
            root_dir, ['*.cmake', 'CMakeLists.txt'],
            ignore_dirs_list,
            cmake_lint_args,
            verbose=args.verbose,
            dry_run=args.dry_run)
        print_exec_info('cmake-lint', num_failed, failed_commands)
        if num_failed > 0:
            raise Exception('Cmake lint check not passed')

    if 'cxx' in args.languages:
        clang_tidy_args = [
            '--style=file:{}'.format(
                str(pathlib.Path(root_dir, args.clang_tidy_config)))
        ] if args.clang_tidy_config else []

        num_failed, failed_commands = exec_on_files(
            ['clang-tidy'],
            root_dir, ['*.h', '*.hpp', '*.cpp', '*.cu'],
            ignore_dirs_list,
            clang_tidy_args,
            verbose=args.verbose,
            dry_run=args.dry_run)
        print_exec_info('clang-tidy', num_failed, failed_commands)
        if num_failed > 0:
            raise Exception('C++ clang-tidy check not passed')

    if 'python' in args.languages:
        flake8_args = [
            '--style {}'.format(str(pathlib.Path(root_dir,
                                                 args.flake8_config)))
        ] if args.flake8_config else []

        num_failed, failed_commands = exec_on_files(['flake8'],
                                                    root_dir, ['*.py'],
                                                    ignore_dirs_list,
                                                    flake8_args,
                                                    verbose=args.verbose,
                                                    dry_run=args.dry_run)
        print_exec_info('flake8', num_failed, failed_commands)
        if num_failed > 0:
            raise Exception('flake8 check not passed')
