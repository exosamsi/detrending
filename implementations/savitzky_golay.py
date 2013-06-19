import numpy as np
import matplotlib.pyplot as plt
from math import factorial
import sys
import numpy.random as r

# Savitzky Golay running polynomial filter. With a hole in the middle to not include the transit in the fit.

def clippedMeanStdev(dataList, sigmaCut = 3.0, maxIterations = 10.0): 
      """Calculates the clipped mean and stdev of a list of numbers. 
       
      @type dataList: list 
      @param dataList: input data, one dimensional list of numbers 
      @type sigmaCut: float 
      @param sigmaCut: clipping in Gaussian sigma to apply 
      @type maxIterations: int 
      @param maxIterations: maximum number of iterations 
      @rtype: dictionary 
      @return: format {'clippedMean', 'clippedStdev', 'numPoints'} 
       
      """ 
       
      listCopy=[] 
      for d in dataList: 
          listCopy.append(d) 
      listCopy=np.array(listCopy) 
       
      iterations=0 
      while iterations < maxIterations and len(listCopy) > 4: 
           
          m=listCopy.mean() 
          s=listCopy.std() 
           
          listCopy=listCopy[np.less(abs(listCopy), abs(m+sigmaCut*s))] 
           
          iterations=iterations+1 
       
      return {'clippedMean': m, 'clippedStdev': s, 'numPoints': listCopy.shape[0]} 

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
     import numpy as np
     from math import factorial
 
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
     # precompute coefficients
     b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])

     m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
#     m[half_window-halfbreaksize:half_window+halfbreaksize+1] = 0
#     m /= np.sum(m)

     # pad the signal at the extremes with
     # values taken from the signal itself
 #    firstvals = y[0]*0.0 + (np.abs( y[1:half_window+1][::-1] - y[0])*0.0 + np.median(y) + r.normal(0, np.std(y), size=half_window))
    
#     lastvals = y[-1]*0.0 + (np.abs(y[-half_window-1:-1][::-1] - y[-1])*0.0 + np.median(y) + r.normal(0, np.std(y), size=half_window))
     firstvals = 2*(y[1]-y[2]) + 2*y[1] -  y[1:half_window+1][::-1] 
     lastvals =  0*(y[-1]-y[-2]) + 2*y[-1] - y[-half_window-1:-1][::-1]
     y[0] = (firstvals[-1] + y[1])/2.0
     yold = y + 0.0
     y = np.concatenate((firstvals, y, lastvals))
  #   plt.plot(y, '.')
  #   plt.show()
   #  print np.convolve( m[::-1], y, mode='valid')
    # sys.exit()
  #   print yold/np.convolve( m[::-1], y, mode='valid')
     return np.convolve( m[::-1], y, mode='valid')
  
fin = 'inputs/' + sys.argv[1] + '/KIC_' + sys.argv[1].zfill(9) + '_sap.dat'
a = np.loadtxt(fin, delimiter=',')

time = a[:,0]
flux = a[:,1]

#plt.plot(time, flux, '.')
#plt.show()
#sys.exit()

nans = np.isnan(flux)
wnans = np.where(nans == 1)[0]
print wnans
print nans
for i in xrange(len(wnans)):
      if np.isnan(flux[wnans[i]-1]) == 0 and np.isnan(flux[wnans[i]+1]) == 0:
            flux[wnans[i]] = (flux[wnans[i]-1] + flux[wnans[i]+1])/2.0

nans = np.isnan(flux)
time = np.delete(time, nans)
flux = np.delete(flux, nans)


gaps = np.where(np.diff(time) > 0.08)[0]

tooshort = np.where(np.diff(gaps) < 30)[0]



#print tooshort
#print len(gaps)
#print len(tooshort)
gaps = np.delete(gaps, tooshort)
gaps = np.append(gaps, len(flux))
#print len(gaps)
#print gaps



gaps += 1
leng = 75
ordr = 3

err = np.zeros(len(time))
fit = np.zeros(len(time))

for i in xrange(len(gaps)):

    if i == 0:
    
    #    plt.plot(time[0:gaps[i]], flux[0:gaps[i]], '.')

    #    plt.show()


        fit[0:gaps[i]] = savitzky_golay(flux[0:gaps[i]], leng, ordr)
        a = clippedMeanStdev((flux[0:gaps[i]])/(fit[0:gaps[i]]), 3.0, 10.0)
        err[0:gaps[i]] = a['clippedStdev']
 #       plt.plot(time[0:gaps[i]], flux[0:gaps[i]], '.')
 #       plt.plot(time[0:gaps[i]], fix, 'r')
 #       plt.show()
 #       flux[0:gaps[i]] /= fix

    #    plt.plot(time[0:gaps[i]], flux[0:gaps[i]], '.')

    #    plt.show()

        
    else:
       # print time[gaps[i]]

        fit[gaps[i-1]:gaps[i]] = savitzky_golay(flux[gaps[i-1]:gaps[i]], leng, ordr)                 
      #  err[gaps[i-1]:gaps[i]] = clippedMeanStdev
        a = clippedMeanStdev((flux[gaps[i-1]:gaps[i]])/(fit[gaps[i-1]:gaps[i]]), 3.0, 10.0)
        err[gaps[i-1]:gaps[i]] = a['clippedStdev']

 #       plt.plot(time[gaps[i-1]:gaps[i]], flux[gaps[i-1]:gaps[i]], '.')
 #       plt.plot(time[gaps[i-1]:gaps[i]], fit[gaps[i-1]:gaps[i]], 'r')
 #       plt.show()


#plt.plot(time, flux, '.')
#plt.plot(time, fit, 'r')
#plt.show()


#plt.plot(time, flux/fit, '.')
#plt.errorbar(time, flux/fit, fmt='.', yerr=err)
#plt.show()

fout = 'outputs/' +sys.argv[1] + '/KIC_' + sys.argv[1].zfill(9) + '_poly_hole.dat'

np.savetxt(fout, np.array([time, flux, flux/fit, err]).transpose(), delimiter=', ')

b = np.loadtxt('inputs/' +sys.argv[1] + '/truth.txt', skiprows=1, delimiter=',')

#plt.plot(np.mod(time-b[4]+100, b[3])-100.0, flux/fit, '.')
#plt.title(sys.argv[1])
#plt.show()
