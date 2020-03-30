# backend.ai-docs-console

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

To build html documentation, run following command in the `docs` directory.
Built documents will be located under `docs/_build`.

```console
make html
```


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

After translation, run following to build translated html document.

```console
make -e SPHINXOPTS="-D language='ko'" html
```

To see the local html documents:

```console
open _build/html/index.html
```


## References for newcomers

http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html

