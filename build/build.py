import json
from pathlib import Path
from typing import Optional

import git

from PyTeX.config.constants import BUILD_INFO_FILENAME

from .utils import BuildInfo, pytex_msg, TexFileToFormat


def build(
        src_dir: Optional[Path] = None,
        build_dir: Optional[Path] = None,
        input_file: Optional[Path] = None,
        author: Optional[str] = None,
        latex_name: str = 'prepend-author',           # name handling
        recursive: bool = False,                      # input control
        include_timestamp: bool = False,              # header
        include_pytex_version: bool = False,          # header
        include_license: bool = False,                # header
        include_git_version: bool = False,            # header
        include_pytex_info_text: bool = False,        # header
        extra_header: Optional[Path] = None,
        allow_dirty: bool = False,                    # versioning
        overwrite_existing_files: bool = False,       # output control
        build_all: bool = False,                      # output control / versioning
        write_build_information: bool = True,         # meta
        ):
    pytex_msg('Getting git repository information...')
    if extra_header:
        if extra_header.exists():
            with open(extra_header, 'r') as f:
                text = f.readlines()
            extra_header = [line.rstrip() for line in text]
        else:
            raise FileNotFoundError('Path to extra header content is invalid.')
    current_build_info = BuildInfo(
        include_timestamp=include_timestamp,
        include_pytex_version=include_pytex_version,
        include_license=include_license,
        include_git_version=include_git_version,
        include_pytex_info_text=include_pytex_info_text,
        extra_header=extra_header,
        author=author,
        pytex_repo=git.Repo(__file__, search_parent_directories=True),
        packages_repo=git.Repo(src_dir, search_parent_directories=True)
    )
    input_dir = src_dir if src_dir else input_file.parent
    output_dir = build_dir if build_dir else input_file.parent

    last_build_info_file = output_dir / BUILD_INFO_FILENAME
    if last_build_info_file.exists():
        with open(output_dir / 'build_info.json', 'r') as f:
            last_build_info = json.load(f)
    else:
        last_build_info = None

    files = []
    if input_file:
        files.append(input_file)
    if src_dir:
        if recursive:
            for file in src_dir.rglob('*.pysty'):
                files.append(file)
            for file in src_dir.rglob('*.pycls'):
                files.append(file)
        else:
            for file in src_dir.glob('*.pysty'):
                files.append(file)
            for file in src_dir.glob('*.pycls'):
                files.append(file)

    sources_to_build = []
    for file in files:
        if last_build_info:
            last_build_info_for_this_file = next(
                (info for info in last_build_info['tex_sources'] if info['source file'] == file.name), {})
        else:
            last_build_info_for_this_file = None
        sources_to_build.append(
            TexFileToFormat(
                src_path=file,
                build_dir=output_dir / file.parent.relative_to(input_dir),
                latex_name=latex_name,
                current_build_info=current_build_info,
                last_build_info=last_build_info_for_this_file,
                allow_dirty=allow_dirty,
                overwrite_existing_files=overwrite_existing_files,
                build_all=build_all
            ))

    info_dict = {
        'build_time': '',
        'source files': {
            'version': current_build_info.packages_version,
            'commit': current_build_info.packages_hash,
            'dirty': current_build_info.package_repo.is_dirty(untracked_files=True)
        },
        'pytex': {
            'version': current_build_info.pytex_version,
            'commit': current_build_info.pytex_hash,
            'dirty': current_build_info.pytex_repo.is_dirty(untracked_files=True)
        },
        'tex_sources': [

        ]
    }

    for source in sources_to_build:
        info = source.format()
        info_dict['tex_sources'].append(info)

    if write_build_information:
        with open(output_dir / 'build_info.json', 'w') as f:
            json.dump(info_dict, f, indent=4)
    pytex_msg('Build done')
