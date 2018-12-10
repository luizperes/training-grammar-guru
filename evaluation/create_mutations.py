import os
import argparse
from pathlib import Path

import detect
import test_tool
from unvocabularize import unvocabularize
from vocabulary import vocabulary

def predict(common, secret, min_rank):
    fixes = detect.suggest(common=common,
                           mutate=True,
                        min_rank=min_rank)
    s = set()
    if fixes:
        for fix in fixes:
            s = s | { fix.rank_score }
        
    return (None, None)

def convert_file_to_tokens(*, src=None, out=None, iter=None,
                           min_rank=None, max_size=None, **kwargs):
    if not os.path.exists(out):
        os.makedirs(out)

    lst_files = []
    for _, _, files in os.walk(src):
        for filename in files:
            lst_files.append(filename)

    for idx, file in enumerate(lst_files):
        print('file ' + file)
        with open(str(src) + '/' + file, 'r') as f:
            fStr = f.read()
            if (len(fStr) > max_size):
                continue
        
        for i in range(0, iter):
            (mutant, secret) = test_tool.mutate(fStr)
            common = test_tool.get_common(mutant, file)
            (hyps, answers) = predict(common, secret, min_rank)
            if hyps is not None:
                with open(str(out) + '/' + file + '.hyp', 'w+') as p:
                    p.write(hyps)
                with open(str(out) + '/' + file + '.ans', 'w+') as q:
                    q.write(answers)

def add_common_args(parser):
    parser.add_argument('src', nargs='?', type=Path,
                        default=Path('/dev/stdin'))
    parser.add_argument('out', nargs='?', type=Path,
                        default=Path('/dev/stdin'))
    parser.add_argument('--iter', type=int, default=5)
    parser.add_argument('--min-rank', type=int,
                        default=15, dest='min_rank')
    parser.add_argument('--max-size', type=int,
                        default=10000, dest='max_size')

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
