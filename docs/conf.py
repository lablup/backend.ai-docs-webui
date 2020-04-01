# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Backend.AI Console User Guide'
copyright = '2020, Lablup Inc.'
author = 'Lablup Inc.'
version = '19.09'
release = '19.09'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'recommonmark'
]

# The file extensions of source files.
# Sphinx considers the files with this suffix as sources. The value can be a
# dictionary mapping file extensions to file types
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# The master toctree document.
master_doc = 'index'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'tango'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = ['css/custom.css']


def setup(app):
    app.add_stylesheet('css/custom.css')


# -- Options for LaTeX output ------------------------------------------------
latex_engine = 'xelatex'
latex_use_xindy = False
latex_logo = '_static/backendai_logo.png'
latex_additional_files = ['_static/lablup_logo.png']
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '12pt',
    'extraclassoptions': 'openany,oneside',
    'sphinxsetup': (
        'noteBorderColor={RGB}{106,176,222},'
        'noteborder=2pt,'
        'tipBorderColor={RGB}{106,176,222},'
        'tipborder=2pt,'
        'hintBorderColor={RGB}{106,176,222},'
        'hintborder=2pt,'
        'importantBorderColor={RGB}{171,18,88},'
        'attentionBorderColor={RGB}{106,176,222},'
        'attentionBgColor={RGB}{231,242,250},'
        'cautionBorderColor={RGB}{240,179,126},'
        'cautionBgColor={RGB}{247,229,198},'
        'warningBorderColor={RGB}{240,179,126},'
        'warningBgColor={RGB}{247,229,198},'
        'dangerBorderColor={RGB}{240,179,126},'
        'dangerBgColor={RGB}{247,229,198},'
        'errorBorderColor={RGB}{240,179,126},'
        'errorBgColor={RGB}{247,229,198},'
    ),
    'fontpkg': '',
    'preamble': r'''
        \usepackage{kotex}
        \usepackage{setspace}
        %% \usepackage{bera}
        %% \usepackage{beramono}

        \setcounter{chapter}{-1}
        \doublespacing
    ''',
    'maketitle': r'''
        \makeatletter
        \begin{titlepage}
            \centering
            \vspace*{15mm}  %% * is used to give space from top
            \sphinxlogo
            \textbf{\Huge Backend.AI Console\\User's Guide}\par
            {\LARGE (\version)}\par
            \vspace{25mm}
            \textbf{\LARGE \@author}\par
            \vspace{10mm}
            \includegraphics[scale=0.1]{lablup_logo}
        \end{titlepage}
        \makeatother
    ''',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc,
     'backendaiconsoleuserguide.tex',
     'Backend.AI Console User\'s Guide',
     author, 'manual'),
]



# -- Internationalization ----------------------------------------------------

locale_dirs = ['locale/']
gettext_compact = False
