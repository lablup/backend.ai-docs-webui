# backend.ai-docs-webui

User's guide for Backend.AI GUI Console.


## Setup build environment

We use [poetry](https://github.com/python-poetry/poetry) to manage dependencies
and packaging. Poetry can be installed by the following command.

```console
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
source ~/.poetry/env  # == export PATH="$HOME/.poetry/bin:$PATH"
```

We recommend to use virtualenv. After virtualenv setup, run following command to
install dependent packages.

```console
poetry install
```


## Build documents

To build html documentation, run following command in the `docs` directory. All
commands should be executed under poetry's virtual environment. For example, you
can run `poetry shell` to enter a command shell with virtualenv.

```console
make html
```

Built documents will be located under `docs/_build`.


## Translation

When English document is updated, extract translatable messages into `.pot`
files. Go to `docs` directory and run following command.

```console
make gettext
``````

From those `.pot` files, `.po` message catalogs can be generated:

```console
sphinx-intl update -p _build/gettext -l ko
```

Now, `.po` files are generated in `locale/ko/LC_MESSAGES/`. Translate messages
with them. For eaiser `.po` translation, you may use GUI apps like
[POEDIT](https://poedit.net/).

Note that a Korean character should not be followed by two backticks(\``)
**WITHOUT A SPACE**, since that will raise compilation errors.

After translation, run following to build translated html document.

```console
make -e SPHINXOPTS="-D language='ko'" html
```

To see the local html documents:

```console
open _build/html/index.html
```

## Build PDF document

To build a pdf document, just replace `html` to `latexpdf`. Note, however, that
your local machine should be prepared with latex generation environment, such as
MacTex, to make pdf file. The following is a brief preparation steps in Mac:


* Install MacTex.
* Register the path to `texbin`: `export PATH="$PATH:/Library/Tex/texbin"`.
* Install fonts on the mac for PDF generation. Fonts can be found at `docs/_static/fonts`.

If prepration is done, execute the following command to generate a pdf document.

```console
cd docs
./build_local_pdf_kr.sh
```

The generated PDF is located under `_build/latexpdf/`.


## References for newcomers

http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html

