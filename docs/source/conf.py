# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Qt-Material'
copyright = '2025, Yeison Cardona'
author = 'Yeison Cardona'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'nbsphinx',
    'dunderlab.docs',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

html_logo = '_static/logo.svg'
html_favicon = '_static/favicon.ico'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

html_theme_options = {
    'caption_font_family': 'Noto Sans',
    'font_family': 'Noto Sans',
    'head_font_family': 'Noto Sans',
    'page_width': '1280px',
    'sidebar_width': '300px',
}

dunderlab_color_links = '#41cd52'
dunderlab_code_reference = True
dunderlab_github_repository = "https://github.com/dunderlab/qt-material"

def setup(app):
    app.add_css_file('custom_qtmaterial.css')