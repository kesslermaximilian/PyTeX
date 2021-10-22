import argparse
import pathlib

from PyTeX.config import FILENAME_TYPE_PREPEND_AUTHOR, FILENAME_TYPE_RAW_NAME

from .build import build


def parse_and_build(arglist: [str]):
    parser = argparse.ArgumentParser(description='Incrementally build LatexPackages with PyTeX')
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '-s', '--source-dir',
        metavar='SRC_DIR',
        help='Relative or absolute path to source directory of .pysty or .pycls files',
        type=pathlib.Path,
        nargs='?',
        default='./src',
        dest='src_dir'
    )
    parser.add_argument(
        '-b', '--build-dir',
        metavar='BUILD_DIR',
        help='Relativ or absolute path to output directory for processed packages and classes',
        type=pathlib.Path,
        nargs='?',
        default='./build',
        dest='build_dir'
    )
    parser.add_argument(
        '-r', '--recursive',
        help='Recursively search subdirectories for files. Default: false',
        action='store_true',
        dest='recursive'
    )
    input_group.add_argument(
        '-i', '--input-file',
        metavar='FILE',
        help='Filename to be built. Can be in valid .pysty or .pycls format',
        type=pathlib.Path,
        dest='input_file'
    )
    parser.add_argument(
        '-n', '--name',
        help='Name of the package / class to be formatted.',
        type=str,
        choices=[FILENAME_TYPE_RAW_NAME, FILENAME_TYPE_PREPEND_AUTHOR],
        default=FILENAME_TYPE_PREPEND_AUTHOR,
        dest='latex_name'
    )
    parser.add_argument(
        '-g', '--git-version',
        help='Insert git version information into build. This assumes your input'
             'files are located in a git repository. Default: false',
        action='store_true',
        dest='include_git_version'
    )
    parser.add_argument(
        '-d', '--allow-dirty',
        help='If git flag is set, allow building of a dirty repo. Default: false',
        action='store_true',
        dest='allow_dirty'
    )
    parser.add_argument(
        '-p',
        '--pytex-version',
        help='Write PyTeX version information into built LaTeX files',
        action='store_true',
        dest='include_pytex_version'
    )
    parser.add_argument(
        '-t', '--build-time',
        help='Insert build time into built LaTeX files',
        action='store_true',
        dest='include_timestamp'
    )
    parser.add_argument(
        '-l', '--license',
        help='Insert MIT license into package header',
        action='store_true',
        dest='include_license'
    )
    parser.add_argument(
        '-a', '--author',
        help='Set author of packages',
        type=str,
        dest='author'
    )
    parser.add_argument(
        '-f', '--force',
        help='Overwrite unknown existing files without confirmation',
        action='store_true',
        dest='overwrite_existing_files'
    )
    parser.add_argument(
        '--pytex-info-text',
        help='Include a PyTeX info text into headers',
        action='store_true',
        dest='include_pytex_info_text'
    )
    parser.add_argument(
        '-e', '--extra-header',
        help='Path to file containing extra text for header of each package',
        type=pathlib.Path,
        dest='extra_header'
    )
    args = vars(parser.parse_args(arglist))
    for arg in args.keys():
        if type(args[arg]) == pathlib.PosixPath:
            args[arg] = args[arg].resolve()
    build(**args)
