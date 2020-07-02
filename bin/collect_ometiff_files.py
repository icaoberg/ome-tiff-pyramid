#!/usr/bin/env python3
from argparse import ArgumentParser
import json
from os import fspath, walk
from pathlib import Path
from typing import Iterable

from utils import OME_TIFF_PATTERN

OUTPUT_FILENAME = Path('ometiffs.json')

def find_ometiff_files(input_dir: Path) -> Iterable[Path]:
    for dirpath_str, _, filenames in walk(input_dir):
        dirpath = Path(dirpath_str)
        for filename in filenames:
            if OME_TIFF_PATTERN.match(filename):
                filepath = dirpath / filename
                print('Found', filepath)
                yield filepath

def write_ometiff_json(input_dir: Path):
    bundles = []
    for ometiff_file in find_ometiff_files(input_dir):
        bundles.append(
            {
                'class': 'File',
                'path': fspath(ometiff_file),
            }
        )
    print('Writing OME-TIFF JSON bundles to', OUTPUT_FILENAME)
    with open(OUTPUT_FILENAME, 'w') as f:
        json.dump(bundles, f)

if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument('input_dir', type=Path)
    args = p.parse_args()

    write_ometiff_json(args.input_dir)
