
import sys
from itertools import *
from pylab import *
from scipy import stats
from scipy.stats import t


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
