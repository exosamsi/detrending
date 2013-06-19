Using different flags on wget, you can download the desired data with the desired directory structure. To download everything use the following:

wget -r http://bbq.dfm.io/~dfm/sandbox1

To remove the http directory structure use the following flags (sandbox1):

wget -r -nH --cut-dirs=1 http://bbq.dfm.io/~dfm/sandbox1

To download only from a specific directory (skygroup27TCE/8012437):

wget -r -np -nH --cut-dirs=1 http://bbq.dfm.io/~dfm/sandbox1/skygroup27TCE/8012437/

Side note: you can specify the target directory, but usually easier to run the wget command while you're in the target dir.

Billy
