import nltk
import pandas as pd
import numpy as np
import re
from collections import Counter
from itertools import *
from pylab import *

import seaborn as sns # poista?
from scipy import stats as sts # zipf, linreg, powerlaw
from scipy.stats import t
from scipy.optimize import curve_fit

def ahat(n, rank):
    return 1 + ( n / sum(log(rank / min(rank) - 0.5) ))

def zipfcurve(bookname,ranks, frequencies, fitted_value, upper_bound_fit, lower_bound_fit, upper_bound_pred, lower_bound_pred):
    # for b in books:
        # Estimate alpha
    alpha = ahat(len(ranks), ranks)

    # Zipf pmf
    p = sts.zipf.pmf(ranks, alpha)

    # Fit curve
    fig, (ax1) = subplots(1, 1)
    total = sum(frequencies)
    ax1.set_title(str(bookname) + " (alpha = " + str(alpha) + ")")
    ax1.scatter(ranks, frequencies)
    ax1.plot(ranks, (1 / ranks) * total, lw=1, color='green')
    ax1.plot(ranks, p * total, lw=1, color='red')
    ax1.set_ylabel("Frequency")
    ax1.set_xlabel("Rank")
    ax1.set_xlim(0, 70) # limit y and x-axis to better see the fit
    ax1.set_ylim(0, max(p * total + 0.005 * total))
    red_patch = matplotlib.patches.Patch(color='red', label='alpha = ' + str(alpha))
    green_patch = matplotlib.patches.Patch(color='green', label='alpha = 1')
    ax1.legend(handles=[red_patch, green_patch])

    return fig
