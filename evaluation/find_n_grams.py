# ONLY WORKS ON PYTHON 2 BECAUSE OF xrange

import os
import argparse # optparse is deprecated
from itertools import islice # slicing for iterators
import string
import math

parser = argparse.ArgumentParser(description='Get ngrams.')
parser.add_argument('-i', '--input', default='source-tokens', help='input file (default source-tokens)')
parser.add_argument('-n', '--num_sentences', default=None, type=int, help='Number of hypothesis pairs to evaluate')
opts = parser.parse_args()

def sentences():
    lst_files = []
    for _, _, files in os.walk(opts.input):
        for filename in files:
            lst_files.append(filename)
    
    for idx, file in enumerate(lst_files):
        with open(opts.input + '/' + file, 'r') as f:
            for line in f:
                yield [None, None, line.split()]

dictionary = [{} for _ in xrange(1,5)]
for _, _, e in islice(sentences(), opts.num_sentences):
    for n in xrange(1,5):
        for i in xrange(len(e)+1-n):
            tp = tuple(e[i:i+n])
            if tp in dictionary[n-1]:
                dictionary[n-1][tp] += 1.0
            else:
                dictionary[n-1][tp] = 1.0

for n in xrange(1,5):
    for key in dictionary[n-1].keys():
        if n == 1: #unigram
            print ' '.join(key) + ' ||| ' + str(math.log10(dictionary[n-1][key]/len(dictionary[n-1])))
        elif n == 2: #bigram
            print ' '.join(key) + ' ||| ' + str(math.log10(dictionary[n-1][key]/dictionary[n-2][key[:1]]))
        elif n == 3: #trigram
            print ' '.join(key) + ' ||| ' + str(math.log10(dictionary[n-1][key]/dictionary[n-2][key[:2]]))
        else: #4-gram
            print ' '.join(key) + ' ||| ' + str(math.log10(dictionary[n-1][key]/dictionary[n-2][key[:3]]))
