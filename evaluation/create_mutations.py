import os
import argparse
from pathlib import Path

import detect
import test_tool
from unvocabularize import unvocabularize
from vocabulary import vocabulary
import itertools

def bestOperation(f1, f2, secret):
    f1Ins = type(f1) is detect.Insert
    f1Del = type(f1) is detect.Remove
    f1Sub = type(f1) is detect.Substitute
    f1Tk  = f1.token.value == secret.old_token.value
    f1Pos = f1.pos == secret.pos
    f2Ins = type(f2) is detect.Insert
    f2Del = type(f2) is detect.Remove
    f2Sub = type(f2) is detect.Substitute
    f2Tk  = f2.token.value == secret.old_token.value
    f2Pos = f2.pos == secret.pos
    scIns = secret.op == 0
    scDel = secret.op == 1
    scSub = secret.op == 2

    if f1Tk and f1Pos and not f2Tk:
        return 1
    elif f2Tk and f2Pos and not f1Tk:
        return -1
    elif f1Pos and not f2Pos:
        return 1
    elif f2Pos and not f1Pos:
        return -1
    elif f1Ins and scDel and not f2Ins:
        return 1
    elif f2Ins and scDel and not f1Ins:
        return -1
    elif f1Del and scIns and not f2Del:
        return 1
    elif f2Del and scIns and not f1Del:
        return -1
    elif f1Sub and scSub and not f2Sub:
        return 1
    elif f2Sub and scSub and not f1Sub:
        return -1

    return 0

def predict(common, secret, min_rank):
    fixes = detect.suggest(common=common,
                           mutate=True,
                        min_rank=min_rank)

    h1h2ref = None
    values  = None
    if fixes and len(fixes) > 1:
        h1h2ref = ''
        values  = '' 
        all_combinations = list(itertools.combinations(fixes, 2))
        for (f1, f2) in all_combinations:
            hyp1 = detect.tokens_to_source_code(f1.tokens[f1.pos-3:f1.pos+3])
            hyp2 = detect.tokens_to_source_code(f2.tokens[f2.pos-3:f2.pos+3])
            ref  = detect.tokens_to_source_code(secret.window)
            h1h2ref += hyp1 + ' ||| ' + hyp2 + ' ||| ' + ref + '\n'
            values += str(bestOperation(f1, f2, secret)) + '\n'

    return (h1h2ref, values)

def convert_file_to_tokens(*, src=None, out=None, iter=None,
                           min_rank=None, max_size=None, **kwargs):
    if not os.path.exists(out):
        os.makedirs(out)

    lst_files = []
    for _, _, files in os.walk(src):
        for filename in files:
            lst_files.append(filename)

    for idx, file in enumerate(lst_files):
        print('idx ' + str(idx))
        with open(str(src) + '/' + file, 'r') as f:
            fStr = f.read()
            if (len(fStr) > max_size):
                continue
        
        for i in range(0, iter):
            (mutant, secret) = test_tool.mutate(fStr)
            common = test_tool.get_common(mutant, file)
            (hyps, answers) = predict(common, secret, min_rank)
            if hyps is not None:
                with open(str(out) + '/' + file + '.hyp', 'a+') as p:
                    p.write(hyps)
                with open(str(out) + '/' + file + '.ans', 'a+') as q:
                    q.write(answers)

def add_common_args(parser):
    parser.add_argument('src', nargs='?', type=Path,
                        default=Path('/dev/stdin'))
    parser.add_argument('out', nargs='?', type=Path,
                        default=Path('/dev/stdin'))
    parser.add_argument('--iter', type=int, default=10)
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
