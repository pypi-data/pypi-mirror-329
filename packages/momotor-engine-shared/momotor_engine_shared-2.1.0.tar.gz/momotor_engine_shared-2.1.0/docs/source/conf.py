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
import datetime
import importlib.metadata
import os
import re
import sys

docs_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(docs_dir, '..', '..')
src_dir = os.path.join(project_dir, 'src')

sys.path.insert(0, src_dir)


# -- Project information -----------------------------------------------------

package_name = 'momotor-engine-shared'
project = 'Momotor Engine Shared'
copyright = '2019-%d, Eindhoven University of Technology' % datetime.datetime.now().year
author = 'E.T.J. Scheffers'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The full version, including alpha/beta/rc tags.
release = importlib.metadata.version(package_name)
# The short X.Y version.
version = re.match(r'\d+\.\d+', release).group(0)


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx_autodoc_typehints',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

rst_epilog = """
.. _Momotor: https://momotor.org/
"""

# -- Options for autodoc -----------------------------------------------------

autodoc_member_order = 'groupwise'

# -- Options for intersphinx -------------------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_copy_source = False

html_theme_options = {
    "light_logo": "logo-text.png",
    "dark_logo": "logo-text-negative.png",
}

html_context = {
    'project_url': 'https://momotor.org/',
    'pypi_url': 'https://pypi.org/project/momotor-engine-shared/',
    'repository_url': 'https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-shared/',
}

html_sidebars = {
    "**": [
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/scroll-start.html",
        "sidebar/navigation.html",
        "sidebar/scroll-end.html",
        "sidebar/variant-selector.html",
        "projectlinks.html",
    ]
}
