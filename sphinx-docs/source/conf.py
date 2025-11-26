# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
project = 'Automação Certificados'
copyright = '2025, João Gabriel Sampaio de Barros'
author = 'João Gabriel Sampaio de Barros'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',  # For Google/NumPy style docstrings
]


templates_path = ['_templates']
exclude_patterns = []

# Napoleon settings for docstring parsing
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# Path setup for autodoc
import sys
import os
sys.path.insert(0, os.path.abspath('../../src'))



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# Using Furo theme - modern, clean, and simple
# Install with: pip install furo
html_theme = 'furo'
html_static_path = ['_static']

# Furo theme options
html_title = 'Automação Certificados'
html_logo = None  # Add path to logo if you have one
html_favicon = None  # Add path to favicon if you have one

# Theme-specific options
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#0066cc",
        "color-brand-content": "#0066cc",
    },
    "dark_css_variables": {
        "color-brand-primary": "#4da6ff",
        "color-brand-content": "#4da6ff",
    },
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
}
