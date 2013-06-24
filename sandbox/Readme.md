Using different flags on wget, you can download the desired data with the desired directory structure. To download everything use the following:

wget -r http://bbq.dfm.io/~dfm/sandbox1

To remove the http directory structure use the following flags (sandbox1):

wget -r -nH --cut-dirs=1 http://bbq.dfm.io/~dfm/sandbox1

To download only from a specific directory (skygroup27TCE/8012437):

wget -r -np -nH --cut-dirs=1 http://bbq.dfm.io/~dfm/sandbox1/skygroup27TCE/8012437/

Side note: you can specify the target directory, but usually easier to run the wget command while you're in the target dir.

Billy

==================

Other light curves of interest:

-- Tom Barclay's injected light curves (description below):

http://bbq.dfm.io/~mrtommyb/ascii_inj/ascii_inj_gstars.tgz

-- Dan Foreman-Mackey's injected light curves:

http://bbq.dfm.io/~dfm/research/bart/examples/injection/data/

-- Gal's detrended LC using median filter

http://bbq.dfm.io/~dfm/research/bart/examples/injection/data_detrended_mf/


===================
Tom's light curve description:

Hi All,
I have new injected data for y’all. These are all G-type stars with injected planets that are somewhat Earth-like.

The files are in a tar file and can be accessed from 
http://bbq.dfm.io/~mrtommyb/ascii_inj/ascii_inj_gstars.tgz
There are 491 light curves.

The format of the columns is 
time   flux   ferr   quality   quarter

a non-zero quality value may indicate dodgy data.

I’ve also put a tar file in the same directory as the light curves that has the master inputs for the injected planets. The format of these files may be complicated. Ask me if you need help understanding the master inputs
