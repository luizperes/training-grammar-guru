import detect

SOURCE_DIR = str(detect.THIS_DIRECTORY / 'evaluation/source')

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

if __name__ == '__main__':
    common = get_common(detect.SOURCE_DIR + "/0.js")
    print(str(common))