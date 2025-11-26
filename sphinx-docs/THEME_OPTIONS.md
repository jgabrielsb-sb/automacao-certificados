# Sphinx Theme Options

## Current Theme: Furo

We're using **Furo**, a modern, clean theme that's excellent for technical documentation.

### Why Furo?

- ✅ **Clean and simple** - Focuses on readability
- ✅ **Dark mode support** - Automatic light/dark theme switching
- ✅ **Mobile responsive** - Works great on all devices
- ✅ **Fast navigation** - Sidebar navigation with search
- ✅ **Modern design** - Professional and polished
- ✅ **Well maintained** - Actively developed

### Installation

Furo needs to be installed as a dependency:

```bash
# Using pip
pip install furo

# Or using uv (recommended for this project)
uv add furo
```

### Configuration

The theme is configured in `source/conf.py`. You can customize:

- Colors (brand colors, links, etc.)
- Logo and favicon
- Sidebar behavior
- Navigation options

## Alternative Themes

If you want to try other themes, here are good options:

### 1. Read the Docs Theme

Classic, widely-used theme:

```python
html_theme = 'sphinx_rtd_theme'
```

Install: `pip install sphinx-rtd-theme`

### 2. PyData Sphinx Theme

Great for technical documentation:

```python
html_theme = 'pydata_sphinx_theme'
```

Install: `pip install pydata-sphinx-theme`

### 3. Sphinx Book Theme

Modern, book-like layout:

```python
html_theme = 'sphinx_book_theme'
```

Install: `pip install sphinx-book-theme`

### 4. Material Theme

Material Design style:

```python
html_theme = 'sphinx_material'
```

Install: `pip install sphinx-material`

## Switching Themes

To switch themes:

1. Install the theme package
2. Update `html_theme` in `conf.py`
3. Adjust `html_theme_options` if needed
4. Rebuild: `make html`

## Customization

All themes support customization through `html_theme_options` in `conf.py`.
Check each theme's documentation for available options.

