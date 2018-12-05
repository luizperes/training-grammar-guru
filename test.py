import os
import sys
import subprocess
import numpy as np
import detect

EVAL_DIR = str(detect.THIS_DIRECTORY / 'evaluation')
SOURCE_DIR = 'source'
RANDOM_FILE_BIN = ('python', EVAL_DIR + '/random_file.py')

architecture = str(detect.THIS_DIRECTORY / 'model-architecture.json')
weights_forwards = str(detect.THIS_DIRECTORY / 'javascript-tiny.5.h5')
weights_backwards = str(detect.THIS_DIRECTORY / 'javascript-tiny.backwards.5.h5')

def get_common(filename):
    with detect.synthetic_file(filename) as f:
        tokens = detect.tokenize_file(f)

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
            print(fStr)
            common = get_common(fStr)
            print("file" + file)
        

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
