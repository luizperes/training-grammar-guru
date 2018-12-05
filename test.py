import sys
import subprocess
import numpy as np
import detect

EVAL_DIR = str(detect.THIS_DIRECTORY / 'evaluation')
SOURCE_DIR = EVAL_DIR + '/source'
RANDOM_FILE_BIN = ('python', EVAL_DIR + '/random_file.py')

architecture = str(detect.THIS_DIRECTORY / 'model-architecture.json')
weights_forwards = str(detect.THIS_DIRECTORY / 'javascript-tiny.5.h5')
weights_backwards = str(detect.THIS_DIRECTORY / 'javascript-tiny.backwards.5.h5')

def get_common(filename):
    with open(str(filename), 'rt', encoding='UTF-8') as script:
        tokens = detect.tokenize_file(script)

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

def test(db, n):
    answers = np.zeros(n)

    print('Extracting files from database...')
    LOAD_FILES_BIN = (*RANDOM_FILE_BIN, db, str(n))
    subprocess.run(LOAD_FILES_BIN, stdout=subprocess.PIPE)
    print("Files extracted.")
    
    # load files in memory
    # for each file, random tests
    # calc MRR
    # calc total

# argv[1] Database path
# argv[2] number of files
if __name__ == '__main__':
    test(sys.argv[1], int(sys.argv[2]))
