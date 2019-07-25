#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SparseSC documentation build configuration file, created by
# sphinx-quickstart on Thu Sep 27 14:53:55 2018.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
##Allow MarkDown.
##Prerequisite. pip install recommonmark 
import recommonmark
from recommonmark.transform import AutoStructify

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx_markdown_tables']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = ['.rst', '.md']

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'SparseSC'
copyright = '2018, Jason Thorpe, Brian Quistorff, Matt Goldman'
author = 'Jason Thorpe, Brian Quistorff, Matt Goldman'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
from SparseSC import __version__
version = __version__
# The full version, including alpha/beta/rc tags. (For now, keep the same)
release = version

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

html_copy_source=False

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

#Allow capturing output
#Modified (to not capture stderr too) from https://stackoverflow.com/questions/5136611/
import contextlib
@contextlib.contextmanager
def capture():
    import sys
    oldout = sys.stdout
    try:
        if sys.version_info[0] < 3:
            from cStringIO import StringIO
        else:
            from io import StringIO
        out=StringIO()
        sys.stdout = out
        yield out
    finally:
        sys.stdout = oldout
        out = out.getvalue()

#Run apidoc from here rather than separate process (so that we can do Read the Docs easily)
#https://github.com/rtfd/readthedocs.org/issues/1139
def run_apidoc(app):
    from sphinx.apidoc import main as apidoc_main
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    buildapidocdir = os.path.join(app.outdir, "apidoc","SparseSC")
    module = os.path.join(cur_dir,"..","src","SparseSC")
    to_excl = ["cross_validation","fit_ct","fit_fold", "fit_loo","optimizers","optimizers/cd_line_search","tensor","utils/ols_model","utils/penalty_utils","utils/print_progress","utils/sub_matrix_inverse","weights"]
    #Locally could wrap each to_excl with "*" "*" and put in the apidoc cmd and end and works as exclude patterns, but doesn't work on RTD
    #with capture() as out: #doesn't have quiet option
    apidoc_main([None, '-f', '-e', '-o', buildapidocdir, module])
    #rm module file because we don't link to it directly and this silences the warning
    os.remove(os.path.join(buildapidocdir, "modules.rst"))
    for excl in to_excl:
        path = os.path.join(buildapidocdir, "SparseSC."+excl.replace("/",".")+".rst")
        print("removing: "+path)
        os.remove(path)

def skip(app, what, name, obj, skip, options):
    #force showing __init__()'s
    if name == "__init__":
        return False
    
    skip_fns = []
    if what=="class" and '__qualname__' in dir(obj) and obj.__qualname__ in skip_fns:
        return True
    
    # Can't figure out how to get the properties class to skip more targettedly
    skip_prs = []
    if what=="class" and name in skip_prs:
        return True
    
    skip_mds = []
    if what=="module" and name in skip_mds:
        return True
    #helpful debugging line
    #print what, name, obj, dir(obj)
    
    return skip

def setup(app):
    app.connect('builder-inited', run_apidoc)
    
    app.connect("autodoc-skip-member", skip)
    #Allow MarkDown
    app.add_config_value('recommonmark_config', {
            'url_resolver': lambda url: "build/apidoc/" + url,
			'auto_toc_tree_section': ['Contents','Examples'],
            'enable_eval_rst': True,
			#'enable_auto_doc_ref': True,
			'enable_math': True,
			'enable_inline_math': True
            }, True)
    app.add_transform(AutoStructify)


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
#html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
        'donate.html',
    ]
}

##Allow MarkDown.
source_parsers = {'.md': 'recommonmark.parser.CommonMarkParser', }


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'SparseSCdoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'SparseSC.tex', 'SparseSC Documentation',
     'Jason Thorpe, Brian Quistorff, Matt Goldman', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'sparsesc', 'SparseSC Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'SparseSC', 'SparseSC Documentation',
     author, 'SparseSC', 'One line description of project.',
     'Miscellaneous'),
]



