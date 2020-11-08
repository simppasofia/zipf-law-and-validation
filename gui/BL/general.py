from __future__ import division
import sys
from itertools import *
from pylab import *
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from scipy import stats
from scipy.stats import t, zipf
from scipy.optimize import curve_fit
from scipy.special import zetac

from nltk.corpus import reuters
from nltk.corpus import wordnet
import scipy.stats as ss
from scipy import special

def pick_book(filename):
    # Read the file and save the words, stripping punctuation, numbers and such
    open_file = open(filename, 'r', encoding='utf-8')
    file_to_string = open_file.read()
    book_words = re.findall(r'(\b[A-Za-z][a-z]{2,15}\b)', file_to_string)
    return book_words

def sw_filter(book_words):
    stop_words = stopwords.words('english')
    stop_words.append('The')
    filtered_words = [w.lower() for w in book_words if not w.lower() in stop_words]
    ftokens_with_count = Counter(map(str.lower, filtered_words))
    topwords = [t[0] for t in ftokens_with_count.most_common(20)]
    doclen = len(ftokens_with_count)
    return filtered_words, ftokens_with_count, topwords, doclen

def tokenizer(book_words):
    # https://gist.github.com/ajnelson-nist/f93e07fca60d0fb42c5c
    tokens_with_count = Counter(map(str.lower, book_words))
    topwords = [t[0] for t in tokens_with_count.most_common(20)]
    return tokens_with_count

def token_counter(tokens_with_count):

    tokens = sorted([k for k in tokens_with_count.keys()])
    counts = array([tokens_with_count[k] for k in tokens])
    ranks = arange(1, len(counts) + 1)
    indices = argsort(-counts)
    frequencies = counts[indices]
    return ranks, indices, frequencies

def point_count(ranks, frequencies, lower_bound, upper_bound):
    point_count = 0
    exlow = exp(lower_bound)
    exup = exp(upper_bound)

    for i in ranks[1:len(ranks)-1]:
        if exlow[i] < frequencies[i] < exup[i]:
            point_count += 1
    return point_count

def print_point_count(bookname, ranks, frequencies, confidence_levels,f_ind):
    book1_wordcount = []
    for level in confidence_levels:
        alpha = 1 - (1 - level) / 2
        reg_vals = linearRegression.linreg(ranks, frequencies, alpha)
        wordcount = point_count(ranks, frequencies, reg_vals[1], reg_vals[2])
        book1_wordcount.append(wordcount)
    if f_ind == 1:
        print("Filtered:   {} : {}, ({})".format(bookname, book1_wordcount, len(ranks)))
    if f_ind == 0:
        print("Unfiltered: {} : {}, ({})".format(bookname, book1_wordcount, len(ranks)))
