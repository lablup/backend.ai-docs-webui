#!/bin/bash

usage() {
    echo "Usage: $0 <language_code>"
    echo "Example: $0 en"
    exit 1
}

if [ $# -ne 1 ]; then
    usage
fi

LANG_CODE=$1

cd "$(dirname "$0")"
make -e SPHINXOPTS="-D language='$LANG_CODE'" latexpdf
\cp -p ./_build/latex/backendaiwebuiuserguide.pdf "./_build/Backend.AI Web-UI User Guide ($LANG_CODE).pdf"

echo "Build completed for language: $LANG_CODE"
echo "Output file: _build/Backend.AI Web-UI User Guide ($LANG_CODE).pdf"
