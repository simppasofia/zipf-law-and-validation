from itertools import *
from pylab import *
from scipy import stats
from scipy.special import zetac
import scipy.stats as ss
from scipy import special

def hist_plot(filtered_words_with_count,bookname):
    topword_count = [t[1] for t in filtered_words_with_count.most_common(20)]
    topwords = [t[0] for t in filtered_words_with_count.most_common(20)]

    x = arange(1,21)
    fig, ax = subplots(1,1, constrained_layout=True)
    ax.bar(x=x, height=topword_count)
    ax.set_xticks(x)
    ax.set_xticklabels(topwords, rotation='vertical')
    ax.set_title(bookname)
    ax.set_ylabel("Absolute frequency of token")

    return fig
