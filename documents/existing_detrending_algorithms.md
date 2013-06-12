A list of the existing detrending algorithms
============================================

A lot of people have their own codes for detrending Kepler light curves. Let's
assemble a list here with links and make sure that we can run all of them.

1. MAP-PDC: this is already available in the Kepler data products. U
2. [Untrendy](https://github.com/dfm/untrendy): cubic spline + iteratively
   re-weighted least-squares + variable complexity. Python + C.
3. [TERRA](http://arxiv.org/pdf/1304.0460.pdf): SAP + manual removal of thermal settling
   effects + median filter. + PCA removal of four most significant modes (probably with PyKE). 
   Doesn't appear that the code is online, but reproducable. His transit search algorithm is a fast-folding 
   algorithm available [here](https://github.com/petigura).
4. [PyKE](http://keplergo.arc.nasa.gov/PyKE.shtml): Many people do a simple detrending using this tool, usually by 
   removing ~5 modes and that's it. Possibly should be included as this is common in the community.
5. [CoFiAM](arxiv.org/abs/1301.1853):Cosine Filtering with Autocorrelation Minimization, Kipping et al. Doesn't seem
   to be available online, I'll ping him and see if he can make it available to us.
6. A control algorithm, using a median filter/low-order polynomial fit on chunks of data? This is what Fabrycky+ 
   does in [TTV:IV](http://astro.uchicago.edu/~fabrycky/kepler/ttvconfirm/ttvs_fabrycky.pdf)
7. The method of [Danielski+](http://arxiv.org/pdf/1304.6673v1.pdf): "We have explored here the
possibility of using non-parametric methods to analyse the Simple Aperture Photometry data observed by the Kepler mission. We focused on a sample of stellar
light curves with different effective temperatures and flux modulations, and we
found that Gaussian Processes-based techniques can very effectively correct the
instrumental systematics along with the long-term stellar activity. Our method
can disentangle astrophysical features (events), such as planetary transits, flares
or general sudden variations in the intensity, from the star signal and it is very efficient as it 
requires only a few training iterations of the Gaussian Process model." Doesn't seem to be available online.

8. Others...?
