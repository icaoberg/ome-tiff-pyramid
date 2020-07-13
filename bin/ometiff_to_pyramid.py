#!/usr/bin/env python3
from argparse import ArgumentParser
from pathlib import Path
from subprocess import run

from utils import OME_TIFF_PATTERN

BIOFORMATS2RAW_COMMAND_TEMPLATE = [
    '/opt/bioformats2raw/bin/bioformats2raw',
    '{input_file}',
    '{n5_directory}',
    '--tile_width',
    '512',
    '--tile_height',
    '512',
    '--max_workers',
    '{processes}',
]
RAW2OMETIFF_COMMAND_TEMPLATE = [
    '/opt/raw2ometiff/bin/raw2ometiff',
    '{n5_path}',
    '{output_ometiff_file}',
    '--compression=zlib',
]

N5_BASE_DIRECTORY = Path('n5')
PYRAMID_BASE_DIRECTORY = Path('ometiff-pyramids')

def convert(ometiff_file: Path, relative_directory: str, processes: int, rgb: bool):
    m = OME_TIFF_PATTERN.match(ometiff_file.name)
    if not m:
        message = f'Filename did not match OME-TIFF pattern: {ometiff_file.name}'
        raise ValueError(message)
    basename = m.group('basename')
    n5_parent_dir = N5_BASE_DIRECTORY / relative_directory
    n5_parent_dir.mkdir(exist_ok=True, parents=True)
    n5_dir = n5_parent_dir / f'{basename}.n5'

    command = [
        piece.format(
            input_file=ometiff_file,
            n5_directory=n5_dir,
            processes=processes,
        )
        for piece in BIOFORMATS2RAW_COMMAND_TEMPLATE
    ]
    print('Running', ' '.join(command))
    run(command, check=True)

    pyramid_parent_dir = PYRAMID_BASE_DIRECTORY / relative_directory
    pyramid_parent_dir.mkdir(exist_ok=True, parents=True)
    output_ometiff_filename = pyramid_parent_dir / f'{basename}.ome.tif'

    command = [
        piece.format(
            n5_path=n5_dir,
            output_ometiff_file=output_ometiff_filename,
        )
        for piece in RAW2OMETIFF_COMMAND_TEMPLATE
    ]
    if rgb:
        command.append('--rgb')
    print('Running', ' '.join(command))
    run(command, check=True)

if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument('ometiff_file', type=Path)
    p.add_argument('relative_directory')
    p.add_argument('processes', type=int)
    p.add_argument('--rgb', action='store_true')
    args = p.parse_args()

    convert(args.ometiff_file, args.relative_directory, args.processes, args.rgb)
