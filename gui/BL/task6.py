# Exponential cutoff with a shift --> parempi sovitus optimizerilla
from itertools import *
from pylab import *
from scipy import stats as sts
import scipy.optimize as opt


def expcutoff(x, alpha, beta):
    return x**(-alpha) * np.exp(-beta * x)

def plot(ranks, freqs, bookname):
    fig, axs = plt.subplots(1, 2, figsize=(10,5))

    # Estimate parameters
    y_norm = (freqs - min(freqs)) / (max(freqs) - min(freqs)) # min-max normalisation
    fit = opt.curve_fit(expcutoff, ranks, y_norm)
    alpha, beta = fit[0]
    p = expcutoff(ranks, alpha, beta)
    axs[0].set_xlabel("Log rank of token")
    axs[0].set_ylabel("Log frequency of token")

    # Plot loglog
    axs[0].set_title(bookname)
    axs[0].loglog(ranks, freqs, marker=".") # observations
    axs[0].plot(ranks, p * max(freqs), lw=1, color='red') # expcutoff

    # Plot linear
    axs[1].set_title(bookname)
    axs[1].scatter(ranks, freqs, marker=".") # observations
    axs[1].plot(ranks, p * max(freqs), lw=2, color='red') # expcutoff
    axs[1].set_xlim(0, 200)
    axs[1].set_xlabel("Rank of token")
    axs[1].set_ylabel("Frequency of token")

    return(fig)
