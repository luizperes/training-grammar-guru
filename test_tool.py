#!/usr/bin/env python3

import os
import sys
import subprocess
import numpy as np
import random
from collections import namedtuple
import argparse
from pathlib import Path

import detect
from vocabulary import vocabulary

EVAL_DIR = str(detect.THIS_DIRECTORY / 'evaluation')
SOURCE_DIR = 'source'
RANDOM_FILE_BIN = ('python', EVAL_DIR + '/random_file.py')

architecture = str(detect.THIS_DIRECTORY / 'model-architecture.json')
weights_forwards = str(detect.THIS_DIRECTORY / 'javascript-tiny.5.h5')
weights_backwards = str(detect.THIS_DIRECTORY / 'javascript-tiny.backwards.5.h5')

TKOperation = namedtuple('TKOperation',
                        'window old_token position op')

def get_common(tokens, filename):
    file_vector = detect.vectorize_tokens(tokens)
    forwards_model = detect.Model.from_filenames(architecture=architecture,
                                                 weights=weights_forwards,
                                                 backwards=False)
    backwards_model = detect.Model.from_filenames(architecture=architecture,
                                                  weights=weights_backwards,
                                                  backwards=True)

    return detect.Common(forwards_model,
                         backwards_model,
                         file_vector,
                         tokens,
                         filename)

def mutate(fStr):
    valid = True
    tokens = []
    operation = None
    new_str = ''
    while valid:
        # try to create less biased random number
        r = random.sample(range(100, 200), 3)
        op = r[0] % 3
        # ignore /*<start>*/ and /*<end>*/ tokens
        tk = detect.id_to_token((r[1] % (len(vocabulary) - 2)) + 1)
        with detect.synthetic_file(fStr) as f:
            tokens = detect.tokenize_file(f)
        pos = (r[2] % (len(tokens) - 2)) + 1
        operation = TKOperation(tokens[pos-3:pos+3], tokens[pos], pos, op)
        if (op == 0): # insert token
            tokens.insert(pos, tk)
        elif (op == 1): # delete token
            tokens.pop(pos)
        else: # replace token
            tokens[pos] = tk
        new_str = detect.tokens_to_source_code(tokens)
        valid = detect.check_syntax(new_str)

    with detect.synthetic_file(new_str) as f:
        tokens = detect.tokenize_file(f)
    return (tokens, operation)

def predict(common, secret, min_rank):
    # TODO: separate true fix, valid fix and no fix using the secret! :)
    fixes = detect.suggest(common=common, test=True, min_rank=min_rank)
    if not fixes:
        return 0
    else:
        for fix in fixes:
            return fix.rank_score

def test(*, db=None, n=None, reset=None, iter=None, min_rank=None, **kwargs):
    ranks = np.zeros(n)

    if reset:
        print('Extracting files from database...')
        LOAD_FILES_BIN = (*RANDOM_FILE_BIN, db, str(n))
        subprocess.run(LOAD_FILES_BIN, stdout=subprocess.PIPE)
        print("Files extracted.")

    lst_files = []
    for _, _, files in os.walk(SOURCE_DIR):
        for filename in files:
            lst_files.append(filename)

    for idx, file in enumerate(lst_files):
        with open(SOURCE_DIR + '/' + file, 'r') as f:
            fStr = f.read()

        print('Calculating MRR of ' + file + '...')
        ranks_file = []
        for i in range(0, iter):
            (mutant, secret) = mutate(fStr)
            common = get_common(mutant, file)
            ranks_file.append(predict(common, secret, min_rank))
        rank_file = detect.mean_reciprocal_rank2(ranks_file)
        ranks[idx] = rank_file
        print('Rank MRR ' + file + ':', rank_file)
    print(str(ranks))
    print("Final MRR: ", detect.mean_reciprocal_rank2(ranks))

def add_common_args(parser):
    parser.add_argument('db', nargs='?', type=Path,
                        default=Path('/dev/stdin'))
    parser.add_argument('--n-files', type=int,
                        default=1, dest='n')
    parser.add_argument('--iter', type=int,
                        default=5)
    parser.add_argument('--min-rank', type=int,
                        default=3, dest='min_rank')
    parser.add_argument('--reset', type=bool,
                        default=False)

parser = argparse.ArgumentParser()
add_common_args(parser)
parser.set_defaults(func=test)

# argv[1] Database path
# argv[2] number of files
# argv[3] number of iterations
# argv[4] should reset test files
if __name__ == '__main__':
    args = parser.parse_args()
    if args.func:
        args.func(**vars(args))
    else:
        parser.print_usage()
        exit(-1)
