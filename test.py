import os
import sys
import subprocess
import numpy as np
import random
from collections import namedtuple

import detect
from vocabulary import vocabulary

EVAL_DIR = str(detect.THIS_DIRECTORY / 'evaluation')
SOURCE_DIR = 'source'
RANDOM_FILE_BIN = ('python', EVAL_DIR + '/random_file.py')

architecture = str(detect.THIS_DIRECTORY / 'model-architecture.json')
weights_forwards = str(detect.THIS_DIRECTORY / 'javascript-tiny.5.h5')
weights_backwards = str(detect.THIS_DIRECTORY / 'javascript-tiny.backwards.5.h5')

TKOperation = namedtuple('TKOperation',
                        'old_token position op')

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
        op = random.randint(0, 2)
        tk = detect.id_to_token(random.randint(0, len(vocabulary) - 2))
        with detect.synthetic_file(fStr) as f:
            tokens = detect.tokenize_file(f)
        pos = random.randint(0, len(tokens) - 1)
        operation = TKOperation(tokens[pos], pos, op)
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

def predict(common):
    return 1

def test(db, n, iter, reset):
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
        f = open(SOURCE_DIR + '/' + file, 'r')
        fStr = f.read()
        f.close()
        
        print('Calculating MRR ' + file + '...')
        ranks_file = np.zeros(iter)
        for i in range(0, iter):
            (mutant, operation) = mutate(fStr)
            common = get_common(mutant, file)
            ranks_file[i] = predict(common)
        rank_file = detect.mean_reciprocal_rank(ranks_file)
        ranks[idx] = rank_file
        print('Rank MRR ' + file + ':', rank_file)
    
    print("Final MRR: ", detect.mean_reciprocal_rank(ranks))

# argv[1] Database path
# argv[2] number of files
# argv[3] number of iterations
# argv[4] should reset test files
if __name__ == '__main__':
    db = sys.argv[1]
    n = int(sys.argv[2])
    iter = int(sys.argv[3])
    reset = int(sys.argv[4]) == 1
    test(db, n, iter, reset)