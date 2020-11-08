from __future__ import division
import sys
from itertools import *
from pylab import *
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from scipy import stats
from scipy.stats import t


def main():
    confidence_levels = [0.8, 0.85, 0.9, 0.95]

    bookname1 = 'flatland.txt'
    bookname2 = 'ulysses.txt'
    bookname3 = 'panama.txt'

    # The preambles and postambles added by Gutenberg have been removed from the .txt files

    book1 = pick_book(bookname1)
    book2 = pick_book(bookname2)
    book3 = pick_book(bookname3)

    tokens_with_count1 = tokenizer(book1)
    tokens_with_count2 = tokenizer(book2)
    tokens_with_count3 = tokenizer(book3)
    ranks1, indices1, frequencies1 = token_counter(tokens_with_count1)
    ranks2, indices2, frequencies2 = token_counter(tokens_with_count2)
    ranks3, indices3, frequencies3 = token_counter(tokens_with_count3)
    fitted_value1, lower_bound_fit1, upper_bound_fit1, upper_bound_pred1, lower_bound_pred1, r_squared1, new_r1, ci_level1 = linreg(ranks1, frequencies1, 0.975)
    fitted_value2, lower_bound_fit2, upper_bound_fit2, upper_bound_pred2, lower_bound_pred2, r_squared2, new_r2, ci_level2 = linreg(ranks2, frequencies2, 0.975)
    fitted_value3, lower_bound_fit3, upper_bound_fit3, upper_bound_pred3, lower_bound_pred3, r_squared3, new_r3, ci_level3 = linreg(ranks3, frequencies3, 0.975)

    filtered_words1, ftokens_with_count1, topwords1, doclen1 = sw_filter(book1)
    filtered_words2, ftokens_with_count2, topwords2, doclen2 = sw_filter(book2)
    filtered_words3, ftokens_with_count3, topwords3, doclen3 = sw_filter(book3)
    ranks1f, indices1f, frequencies1f = token_counter(ftokens_with_count1)
    ranks2f, indices2f, frequencies2f = token_counter(ftokens_with_count2)
    ranks3f, indices3f, frequencies3f = token_counter(ftokens_with_count3)
    fitted_value1f, lower_bound_fit1f, upper_bound_fit1f, upper_bound_pred1f, lower_bound_pred1f, r_squared1f, new_r1f, ci_level1f = linreg(ranks1f, frequencies1f, 0.975)
    fitted_value2f, lower_bound_fit2f, upper_bound_fit2f, upper_bound_pred2f, lower_bound_pred2f, r_squared2f, new_r2f, ci_level2f = linreg(ranks2f, frequencies2f, 0.975)
    fitted_value3f, lower_bound_fit3f, upper_bound_fit3f, upper_bound_pred3f, lower_bound_pred3f, r_squared3f, new_r3f, ci_level3f = linreg(ranks3f, frequencies3f, 0.975)




    print("[0.80, 0.85, 0.90, 0.95], (length)")
    print_point_count(bookname1, ranks1, frequencies1, confidence_levels,0)
    print_point_count(bookname1, ranks1f, frequencies1f, confidence_levels,1)
    print_point_count(bookname2, ranks2, frequencies2, confidence_levels,0)
    print_point_count(bookname2, ranks2f, frequencies2f, confidence_levels,1)
    print_point_count(bookname3, ranks3, frequencies3, confidence_levels,0)
    print_point_count(bookname3, ranks3f, frequencies3f, confidence_levels,1)


    print(bookname1, topwords1)
    print(bookname2, topwords2)
    print(bookname3, topwords3)

    zipf_plot(bookname1, ranks1, frequencies1, fitted_value1, upper_bound_fit1, lower_bound_fit1, upper_bound_pred1, lower_bound_pred1,0) #, ftokens_with_count1)
    zipf_plot(bookname2, ranks2, frequencies2, fitted_value2, upper_bound_fit2, lower_bound_fit2, upper_bound_pred2, lower_bound_pred2,0) #, ftokens_with_count2)
    zipf_plot(bookname3, ranks3, frequencies3, fitted_value3, upper_bound_fit3, lower_bound_fit3, upper_bound_pred3, lower_bound_pred3,0) #, ftokens_with_count3)

    zipf_plot(bookname1, ranks1f, frequencies1f, fitted_value1f, upper_bound_fit1f, lower_bound_fit1f, upper_bound_pred1f, lower_bound_pred1f,1)
    zipf_plot(bookname2, ranks2f, frequencies2f, fitted_value2f, upper_bound_fit2f, lower_bound_fit2f, upper_bound_pred2f, lower_bound_pred2f,1)
    zipf_plot(bookname3, ranks3f, frequencies3f, fitted_value3f, upper_bound_fit3f, lower_bound_fit3f, upper_bound_pred3f, lower_bound_pred3f,1)

    hist_plot(ftokens_with_count1,bookname1)
    hist_plot(ftokens_with_count2,bookname2)
    hist_plot(ftokens_with_count3,bookname3)

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
    print("regular: ", topwords)
    return tokens_with_count


def token_counter(tokens_with_count):
    tokens = sorted([k for k in tokens_with_count.keys()])
    counts = array([tokens_with_count[k] for k in tokens])
    ranks = arange(1, len(counts) + 1)
    indices = argsort(-counts)
    frequencies = counts[indices]
    return ranks, indices, frequencies


# 3 - Linear regression
def linreg(ranks, frequencies, ci_level):
    r = log(ranks)
    fr = log(frequencies)

    slope, intercept, r_value, p_value, std_err = stats.linregress(r, fr)
    r_squared = r_value ** 2


    obs_values = fr
    fitted_value = slope * r + intercept
    residuals = obs_values - fitted_value

    n = len(fr)
    sse = sum(residuals ** 2)
    mse = sse / (n - 2)
    t_val = t.ppf(ci_level, n - 2)  # Student's t-distribution with n-2 df.
    S = sqrt(mse)
    SSX = sum((r - mean(r)) ** 2)

    SE_fit = S * sqrt(1 / n + (r - mean(r)) ** 2 / SSX)  # Standard error for the fitted values
    upper_bound_fit = fitted_value + t_val * SE_fit  # Upper confidence interval bound at given confidence level
    lower_bound_fit = fitted_value - t_val * SE_fit  # Lower confidence interval bound at given confidence level

    new_r = arange(min(r), max(r) + 1, 1)  # New data for calculating predicted values
    predicted_values = mean(fr) + slope * (r - mean(r))  # Calculate predicted values for the new data
    SE_pred = S * sqrt(1 + 1 / n + (r - mean(r)) ** 2 / SSX)  # Standard error for predicted values
    upper_bound_pred = predicted_values + t_val * SE_pred  # Confidence bounds for predicted values
    lower_bound_pred = predicted_values - t_val * SE_pred

    return fitted_value, lower_bound_fit, upper_bound_fit, upper_bound_pred, lower_bound_pred, r_squared, new_r, ci_level




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
        reg_vals = linreg(ranks, frequencies, alpha)
        wordcount = point_count(ranks, frequencies, reg_vals[1], reg_vals[2])
        book1_wordcount.append(wordcount)
    if f_ind == 1:
        print("Filtered:   {} : {}, ({})".format(bookname, book1_wordcount, len(ranks)))
    if f_ind == 0:
        print("Unfiltered: {} : {}, ({})".format(bookname, book1_wordcount, len(ranks)))


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
    show()


def hist_plot(filtered_words_with_count,bookname):
    topword_count = [t[1] for t in filtered_words_with_count.most_common(20)]
    topwords = [t[0] for t in filtered_words_with_count.most_common(20)]

    x = arange(1,21)
    fig, ax = subplots(1,1)
    ax.bar(x=x, height=topword_count)
    ax.set_xticks(x)
    ax.set_xticklabels(topwords, rotation='vertical')
    ax.set_title(bookname)
    ax.set_ylabel("Absolute frequency of token")
    show()

if __name__ == "__main__":
    main()
