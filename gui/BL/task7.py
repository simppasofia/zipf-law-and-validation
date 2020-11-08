import pandas as pd
from pylab import *
from collections import Counter
from itertools import *
import os

from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt



def histogram(cat_name):
    fig, axs = plt.subplots(3, figsize=(10,15), constrained_layout=True)
    i = 0

    for b in books.index:
        axs[i].set_title("20 most frequent words in " + b + " by GI category " + cat_name)
        axs[i].bar(cat_match[b][0:n-1], cat_freqs[b][0:n-1])
        axs[i].set_xticklabels(cat_match[b][0:n-1], rotation='vertical')

        i = i+1
    plt.show()

def cat(bookname,catname):

    #Read the book
    # bookname = "flatland.txt"
    open_file = open(bookname, 'r', encoding='utf-8')
    book = open_file.read()
    tokens = re.findall(r'(\b[A-Za-z][a-z]{2,15}\b)', book)
    lowercase_tokens = [t.lower() for t in tokens]
    alphabets = [t for t in lowercase_tokens if t.isalpha()]
    words = stopwords.words("english")
    stopwords_removed = [t for t in alphabets if t not in words]
    lemmatizer = WordNetLemmatizer()
    lem_tokens = [lemmatizer.lemmatize(t) for t in stopwords_removed]

    open_file = open(catname, 'r', encoding='utf-8')
    cats = open_file.read()
    cat_tokens = word_tokenize(cats)
    lowercase_cat_tokens = [t.lower() for t in cat_tokens]
    cat_token_list = [t for t in lowercase_cat_tokens]

    #Get matches
    matches = [(w, lem_tokens.count(w)) for w in set(lem_tokens) if w in set(cat_token_list)]
    # print(matches)
    def second_element(elem):
        return elem[1]
    matches_sorted = sorted(matches,key=second_element,reverse=True)
    match_tokens = ([t for t,c in matches_sorted])
    match_counts = array([c for t,c in matches_sorted])


    #Get freqs and ranks
    ranks = arange(1, len(match_counts) + 1)
    indices = argsort(-match_counts)
    frequencies = match_counts[indices]

    fig, axs = subplots(1, 2, figsize=(10,5))
    axs[0].loglog(ranks, frequencies, marker=".")
    for n in set(logspace(-0.5, log10(len(match_counts)-1), 20).astype(int)):
        label = "{}".format(match_tokens[indices[n]])
        annotate(label,
                     (ranks[n], frequencies[n]),
                     ha='left',
                     va='bottom',
                     rotation=30)
    axs[0].set_ylabel("Absolute frequency of token")
    axs[0].title.set_text("Zipf plot for category-matched tokens \n in {} on loglog-scale".format(bookname))
    axs[0].set_xlabel("Rank of token")
    axs[0].grid(True)

    sns.regplot(x=log10(ranks), y=log10(frequencies), ax=axs[1])
    axs[1].grid(True)
    axs[1].title.set_text("Linear regression for the base-10 logarithms \n of points in {} on linear scale".format(bookname))
    axs[1].set_ylabel("Log10-frequency of token")
    axs[1].set_xlabel("Log10-rank of token")

    return(fig)
