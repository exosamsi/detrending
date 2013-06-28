from __future__ import division

import numpy as np
from math import factorial

tshape = np.array([-6.2680861549e-05,-7.51147104129e-05,-8.1675212482e-05,-8.59721654205e-05,-8.89860241272e-05,-9.11709806897e-05,-9.2782138234e-05,-9.39787464741e-05,-9.48667894779e-05,-9.5519535689e-05,-9.59885260372e-05,-9.63098635139e-05,-9.6507955222e-05,-9.65977414225e-05,-9.65859539661e-05,-9.64717117351e-05,-9.62464372752e-05,-9.58931166629e-05,-9.53848499962e-05,-9.46823283688e-05,-9.37296157498e-05,-9.24470147773e-05,-9.07184361929e-05,-8.83672876828e-05,-8.51049500242e-05,-8.03996002964e-05,-7.30188174661e-05,-5.12811650369e-05])*6 + 1.0

def savitzky_golay(y, window_size, order, deriv=0, rate=1):
     """Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
     The Savitzky-Golay filter removes high frequency noise from data.
   4     It has the advantage of preserving the original shape and
   5     features of the signal better than other types of filtering
   6     approaches, such as moving averages techniques.
   7     Parameters
   8     ----------
   9     y : array_like, shape (N,)
  10         the values of the time history of the signal.
  11     window_size : int
  12         the length of the window. Must be an odd integer number.
  13     order : int
  14         the order of the polynomial used in the filtering.
  15         Must be less then `window_size` - 1.
  16     deriv: int
  17         the order of the derivative to compute (default = 0 means only smoothing)
  18     Returns
  19     -------
  20     ys : ndarray, shape (N)
  21         the smoothed signal (or it's n-th derivative).
  22     Notes
  23     -----
  24     The Savitzky-Golay is a type of low-pass filter, particularly
  25     suited for smoothing noisy data. The main idea behind this
  26     approach is to make for each point a least-square fit with a
  27     polynomial of high order over a odd-sized window centered at
  28     the point.
  29     Examples
  30     --------
  31     t = np.linspace(-4, 4, 500)
  32     y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
  33     ysg = savitzky_golay(y, window_size=31, order=4)
  34     import matplotlib.pyplot as plt
  35     plt.plot(t, y, label='Noisy signal')
  36     plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
  37     plt.plot(t, ysg, 'r', label='Filtered signal')
  38     plt.legend()
  39     plt.show()
  40     References
  41     ----------
  42     .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
  43        Data by Simplified Least Squares Procedures. Analytical
  44        Chemistry, 1964, 36 (8), pp 1627-1639.
  45     .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
  46        W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
  47        Cambridge University Press ISBN-13: 9780521880688
  48     """
 
     halfbreaksize = 10
     try:
         window_size = np.abs(np.int(window_size))
         order = np.abs(np.int(order))
     except ValueError, msg:
         raise ValueError("window_size and order have to be of type int")
     if window_size % 2 != 1 or window_size < 1:
         raise TypeError("window_size size must be a positive odd number")
     if window_size < order + 2:
         raise TypeError("window_size is too small for the polynomials order")

     order_range = range(order+1)
     half_window = (window_size -1) // 2

     b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
     m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)

     firstvals = 2*(y[1]-y[2]) + 2*y[1] -  y[1:half_window+1][::-1] 
     lastvals =  0*(y[-1]-y[-2]) + 2*y[-1] - y[-half_window-1:-1][::-1]
     y[0] = (firstvals[-1] + y[1])/2.0

     yold = y.copy()
     y = np.concatenate((firstvals, y, lastvals))
     ybest = y.copy()

     fit =  np.convolve( m[::-1], y, mode='valid')
     fitbest = np.convolve( m[::-1], y, mode='valid')
     chi2nopl = np.sum((yold/fitbest-1)**2)

     for j in xrange(yold.size):
           tmin = j
           tmax = j+tshape.size
           v    = y.copy()
           
           if tmin > 0 and tmax == yold.size - 1:
                 v[tmin:tmax] /= tshape

           vold = v[firstvals.size:-firstvals.size].copy()
           fit = np.convolve( m[::-1], v, mode='valid')
           chi2 = np.sum((vold/fit - 1)**2)

           if chi2 < chi2nopl:
                 fitbest = fit.copy()
                 chi2nopl = chi2

     return fitbest
