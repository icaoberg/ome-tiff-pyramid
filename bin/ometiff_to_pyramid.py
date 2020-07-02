#!/usr/bin/env python3
from argparse import ArgumentParser
from pathlib import Path
import re
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

def convert(ometiff_file: Path, processes: int, rgb: bool):
    m = OME_TIFF_PATTERN.match(ometiff_file.name)
    if not m:
        message = f'Filename did not match OME-TIFF pattern: {ometiff_file.name}'
        raise ValueError(message)
    basename = m.group('basename')
    n5_dir = f'{basename}.n5'

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

    output_ometiff_filename = f'{basename}.ome.tif'

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
    p.add_argument('processes', type=int)
    p.add_argument('--rgb', action='store_true')
    args = p.parse_args()

    convert(args.ometiff_file, args.processes, args.rgb)
