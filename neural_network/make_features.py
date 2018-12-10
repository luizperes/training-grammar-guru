#!/usr/bin/env python
import argparse # optparse is deprecated
from itertools import islice # slicing for iterators
import numpy as np
from itertools import chain
import string
#import nltk
import sys
import csv

# parser = argparse.ArgumentParser(description='Evaluate translation hypotheses.')
# parser.add_argument('-i', '--input', default='./source-hyps/h1h2ref.hyp', help='input file (default data/hyp1-hyp2-ref)')
# parser.add_argument('-r', '--truth', default='./source-hyps/h1h2ref.ans', help='input file (default data/hyp1-hyp2-ref)')
# parser.add_argument('-m', '--model', default='./ngrams/ngrams', help='input file (model)')
# parser.add_argument('-n', '--num_sentences', default=None, type=int, help='Number of hypothesis pairs to evaluate')
# parser.add_argument('-a', '--alpha', default=0.1, type=float, help='Number of hypothesis pairs to evaluate')
# parser.add_argument('-b', '--beta', default=3.0, type=float, help='Number of hypothesis pairs to evaluate')
# parser.add_argument('-g', '--gamma', default=0.5, type=float, help='Number of hypothesis pairs to evaluate')
# opts = parser.parse_args()

cachedStopWords = ['$anyIdentifier', '/*any-number*/0', '"any-string"', '/any-regexp/']
ngram_dict = {}

def matches(h, e):
    r = 0.0
    p = 0.0
    m = 0.0001
    for w in h:
        if w in e:
            m += 1
    r = float(m)/float(len(e)) if e else 0.0001
    p = float(m)/float(len(h)) if h else 0.0001 
    f = 2 * p * r / (p + r)
    return p, r, f

def sentences():
    with open('./source-hyps/h1h2ref.hyp') as f:
        for pair in f:
            value = [[],[],[]]
            for i,sentence in enumerate(pair.split(' ||| ')):
                value[i] = sentence
                #print value[i]
            yield value

def get_model():
    with open('./ngrams/ngrams') as f:
        for pair in f:
            yield tuple(pair.split(' ||| '))

def score_ngram(ngram):
    if ngram in ngram_dict:
        return ngram_dict[ngram]
    else:
        return 5

def get_ngrams(reference, cand1, cand2, vc1, vc2, long):
    score_cand1 = 0
    score_cand2 = 0
    for n in range(1,5):
        e_ngrams  = [tuple(reference[i:i+n]) for i in range(len(reference)+1-n)]
        h1_ngrams = [tuple(cand1[i:i+n]) for i in range(len(cand1)+1-n)]
        h2_ngrams = [tuple(cand2[i:i+n]) for i in range(len(cand2)+1-n)]

        if long:
            for i in range(len(cand1)+1-n):
                score_cand1 += score_ngram(tuple(cand1[i:i+n]))
            for i in range(len(cand2)+1-n):
                score_cand2 += score_ngram(tuple(cand2[i:i+n]))

        # save precison, score and f1 for ngrams
        (vc1[n-1], vc1[n+3], vc1[n+7]) = matches(h1_ngrams, e_ngrams)
        (vc2[n-1], vc2[n+3], vc2[n+7]) = matches(h2_ngrams, e_ngrams)

    # average of ngrams
    vc1[12] = (vc1[0]+vc1[1]+vc1[2]+vc1[3])/4
    vc2[12] = (vc2[0]+vc2[1]+vc2[2]+vc2[3])/4

    if long:
        vc1[13] = score_cand1/100
        vc2[13] = score_cand2/100

    return (vc1, vc2)

# remove stop words
def rsw(h):
    return [word for word in h if word not in cachedStopWords]

for words, count in get_model():
    tp = tuple(words.split())
    ngram_dict[tp] = float(count)

wt = [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.5, 0.5, 0.5, 0.5, 0.5, 0.1,
       0.275, 0.275, 0.275, 0.275, 0.275, 0.275, 0.275, 0.275, 0.275, 0.275, 0.275, 0.275, 0.275]

# mat = np.zeros(shape=(149, 28))

# header = ['f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
#           'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19',
#           'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'truth']

# truth=[]
# with open('./source-hyps/h1h2ref.ans') as ref:
#     for t in ref:
#         truth.append(int(t.strip()))
# print(len(truth))
# for n, (h1, h2, e) in enumerate(islice(sentences(), None)):
#     if n%500 == 0:
#         sys.stderr.write(str(n/500)+' percent\n')
#     vc1, vc2  = [0] * 14, [0] * 14 # feature vector h1
#     sw1, sw2 = [0] * 13, [0] * 13
#     (vc1, vc2) = get_ngrams(e, h1, h2, vc1, vc2, True) 
#     (sw1, sw2) = get_ngrams(rsw(e), rsw(h1), rsw(h2), sw1, sw2, False)
#     vc1.extend(sw1)
#     vc2.extend(sw2)
#     diff = list(np.subtract(vc1, vc2))
#     diff.append(truth[n])
#     mat[n]=diff

# with open('feature_values.csv', 'wb') as f:
#     writer = csv.writer(f)
#     writer.writerow(header)
#     writer.writerows(mat)
