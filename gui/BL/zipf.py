
import sys
from itertools import *
from pylab import *

from collections import Counter
from scipy import stats
from scipy.stats import t, zipf
from scipy.optimize import curve_fit
from scipy.special import zetac

import scipy.stats as ss
from scipy import special
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
def zipf_plot(bookname, ranks, frequencies, fitted_value, upper_bound_fit, lower_bound_fit, upper_bound_pred, lower_bound_pred,f_ind): #, filtered_words_with_count):

    fig, (ax1) = subplots(1, 1)
    ax1.loglog(ranks, frequencies, '.',     color='grey', label='obs')
    ax1.plot(ranks, exp(fitted_value),      color='black', label='fitted')
    ax1.plot(ranks, exp(upper_bound_fit),   color='red', label='confint')   # Luottamusväli
    ax1.plot(ranks, exp(lower_bound_fit),   color='red')                    # Luottamusväli
    ax1.plot(ranks, exp(upper_bound_pred),  color='blue', label='predint')  # Ennusteväli
    ax1.plot(ranks, exp(lower_bound_pred),  color='blue')                   # Ennusteväli
    ax1.set_ylabel("Absolute frequency of token")
    ax1.set_xlabel("Rank of token")
    ax1.legend()
    ax1.grid(True)
    if f_ind == 1:
        ax1.set_title("Filtered {}".format(bookname))
    else:
        ax1.set_title("Unfiltered {}".format(bookname))
    return(fig)
