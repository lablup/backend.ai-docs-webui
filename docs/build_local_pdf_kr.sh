\cp -r conf.py conf.original.py
\cp -r conf.local.py conf.py
# make -e SPHINXOPTS="-D language='ko'" latexpdf
make latexpdf
\mv -f conf.original.py conf.py
