import os
import argparse
from pathlib import Path

import detect
from unvocabularize import unvocabularize
from vocabulary import vocabulary

def convert_file_to_tokens(*, src=None, out=None, **kwargs):
    if not os.path.exists(out):
        os.makedirs(out)

    lst_files = []
    for _, _, files in os.walk(src):
        for filename in files:
            lst_files.append(filename)

    for idx, file in enumerate(lst_files):
        with open(str(src) + '/' + file, 'r') as f:
            tokens = detect.tokenize_file(f)
            vector = detect.vectorize_tokens(tokens)
            v = unvocabularize(vector)
            with open(str(out) + '/' + file + '.tks', 'w+') as p:
                p.write(v)
        print('file ' + file)

def add_common_args(parser):
    parser.add_argument('src', nargs='?', type=Path,
                        default=Path('/dev/stdin'))
    parser.add_argument('out', nargs='?', type=Path,
                        default=Path('/dev/stdin'))

parser = argparse.ArgumentParser()
add_common_args(parser)
parser.set_defaults(func=convert_file_to_tokens)

if __name__ == '__main__':
    args = parser.parse_args()
    if args.func:
        args.func(**vars(args))
    else:
        parser.print_usage()
        exit(-1)
