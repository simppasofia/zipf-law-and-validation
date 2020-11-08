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


def main():
    booklist = ["flatland.txt", "ulysses.txt", "panama.txt"]
    catlist = ["flatlands_multi_category.txt", "ulysses_multi_category.txt", "panama_multi_category.txt"]

    for i in range(0,3):
        print(i)
        book = booklist[i]
        cat = catlist[i]

        doitall(book,cat)


def doitall(bookname,catname):

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
    # print(len(lem_tokens))

    #Read the category
    # catname = "flatlands_multi_category.txt"
    open_file = open(catname, 'r', encoding='utf-8')
    cats = open_file.read()
    cat_tokens = word_tokenize(cats)
    lowercase_cat_tokens = [t.lower() for t in cat_tokens]
    cat_token_list = [t for t in lowercase_cat_tokens]
    # print(len(cat_token_list))
    # print(len(set(cat_token_list)))



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


    #Plot the results
    # fig = plt.figure()
    # ax1 = fig.add_subplot(131)
    # ax2 = fig.add_subplot(132)
    # ax3 = fig.add_subplot(133)
    #
    #
    # ax1.loglog(ranks, frequencies, marker=".")
    # for n in set(logspace(-0.5, log10(len(match_counts)-1), 20).astype(int)):
    #     label = "{}".format(match_tokens[indices[n]])
    #     ax1.annotate(label,
    #                  (ranks[n], frequencies[n]),
    #                  ha='left',
    #                  va='bottom',
    #                  rotation=30)
    # ax1.grid(True)
    # ax1.title.set_text("Zipf plot for category-matched tokens \n in {} on loglog-scale".format(bookname))
    # ax1.set_ylabel("Absolute frequency of token")
    # ax1.set_xlabel("Frequency rank of token")
    #
    # ax2.plot(ranks,frequencies)
    # ax2.grid(True)
    # ax2.title.set_text("Zipf plot for category-matched tokens \n in {} on linear scale".format(bookname))
    # ax2.set_ylabel("Absolute frequency of token")
    # ax2.set_xlabel("Frequency rank of token")
    #
    # sns.regplot(x=log10(ranks), y=log10(frequencies), ax=ax3)
    # ax3.grid(True)
    # ax3.title.set_text("Linear regression for the base-10 logarithms \n of points in {} on linear scale".format(bookname))
    # ax3.set_ylabel("Log10-frequency of token")
    # ax3.set_xlabel("Log10-rank of token")
    # show()



    loglog(ranks, frequencies, marker=".")
    for n in set(logspace(-0.5, log10(len(match_counts)-1), 20).astype(int)):
        label = "{}".format(match_tokens[indices[n]])
        annotate(label,
                     (ranks[n], frequencies[n]),
                     ha='left',
                     va='bottom',
                     rotation=30)
    grid(True)
    title("Zipf plot for category-matched tokens \n in {} on loglog-scale".format(bookname))
    ylabel("Absolute frequency of token")
    xlabel("Frequency rank of token")
    show()

    plot(ranks,frequencies)
    grid(True)
    title("Zipf plot for category-matched tokens \n in {} on linear scale".format(bookname))
    ylabel("Absolute frequency of token")
    xlabel("Frequency rank of token")
    show()

    sns.regplot(x=log10(ranks), y=log10(frequencies))
    grid(True)
    title("Linear regression for the base-10 logarithms \n of points in {} on linear scale".format(bookname))
    ylabel("Log10-frequency of token")
    xlabel("Log10-rank of token")
    show()

if __name__ == "__main__":
    main()