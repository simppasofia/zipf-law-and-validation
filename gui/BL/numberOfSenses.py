
import sys
from itertools import *
from pylab import *
from nltk.tokenize import word_tokenize
from collections import Counter
from scipy import stats
from scipy.stats import t, zipf
from nltk.corpus import wordnet
import scipy.stats as ss
from scipy import special
from scipy import stats as sts


def ahat(n, rank):
    return 1 + ( n / sum(log(rank / min(rank) - 0.5) ))

def senses_plot(filttered_word, rank, bookname):
    words = filttered_word
    counts = [(w, words.count(w)) for w in words]

    amb = [(w, c, len(wordnet.synsets(w)))
          for (w, c) in counts if len(wordnet.synsets(w)) > 0]

    numberOfsenses = array([t[2] for t in amb]  )

    amb_p_rank = ss.rankdata([p for (w,c,p) in amb],method='ordinal')
    slope, intercept, _, _, _ = sts.linregress(log(amb_p_rank), log(numberOfsenses))
    y = intercept + log(amb_p_rank) * slope

    fig, (ax1) = subplots(1, 1)
    ax1.loglog(amb_p_rank, numberOfsenses, '.')
    ax1.plot(amb_p_rank, exp(y), lw=1, linestyle="--", color="green") #linear
    ax1.set_ylabel("Number of senses")
    ax1.set_xlabel("Rank of token")
    ax1.set_ylim(10e-2, 10e3)
    ax1.grid(True)

    ax1.set_title(bookname)
    return(fig)
