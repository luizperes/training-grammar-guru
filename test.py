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

def get_common(tokens):
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
        op = random.randint(0, 3)
        tk = detect.id_to_token(random.randint(0, len(vocabulary)))
        with detect.synthetic_file(fStr) as f:
            tokens = detect.tokenize_file(f)
        pos = random.randint(0, len(tokens))
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

def test(db, n, iter, reset):
    answers = np.zeros(n)

    if reset:
        print('Extracting files from database...')
        LOAD_FILES_BIN = (*RANDOM_FILE_BIN, db, str(n))
        subprocess.run(LOAD_FILES_BIN, stdout=subprocess.PIPE)
        print("Files extracted.")
    
    lst_files = []
    for _, _, files in os.walk(SOURCE_DIR):
        for filename in files:
            lst_files.append(filename)
    
    for file in lst_files:
        f = open(SOURCE_DIR + '/' + file, 'r')
        fStr = f.read()
        f.close()
        for _ in range(0, iter):
            (mutant, operation) = mutate(fStr)
            print(str(operation))
            #common = get_common(mutant)
            #print("file" + file)
        

    # for each file, random tests
    # calc MRR
    # calc total

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
