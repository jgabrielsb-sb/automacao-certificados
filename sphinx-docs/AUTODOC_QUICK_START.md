# Quick Start: Autodocumenting Your API with Sphinx

## Overview

Your Sphinx documentation is configured to automatically generate API documentation from docstrings in your Python code. This guide explains the essentials.

## How It Works

1. **Write docstrings** in your Python code using Google-style format
2. **Sphinx autodoc** reads the docstrings and generates documentation
3. **API Reference** is automatically updated when you rebuild docs

## Docstring Format (Google Style)

### Class Example

```python
class MyClass:
    """
    Brief description of the class.
    
    Longer description if needed.
    
    Attributes:
        attr1 (type): Description of attribute.
    """
    pass
```

### Function/Method Example

```python
def my_function(param1: str, param2: int) -> bool:
    """
    Brief description of what the function does.
    
    Args:
        param1: Description of the first parameter.
        param2: Description of the second parameter.
    
    Returns:
        Description of what is returned.
    
    Raises:
        ValueError: When param1 is empty.
    """
    pass
```

## Key Sphinx Directives

In `api_reference.rst`, we use these directives:

- **`.. autoclass::`** - Documents a class and its methods
- **`.. automodule::`** - Documents an entire module
- **`.. autofunction::`** - Documents a single function

### Common Options

- `:members:` - Include all members (methods, attributes)
- `:undoc-members:` - Include members without docstrings
- `:show-inheritance:` - Show inheritance diagram
- `:special-members: __init__` - Include special methods like `__init__`

## Current API Reference Structure

The `api_reference.rst` file is organized by:

1. **Core Interfaces** - Using `autoclass` for each interface
2. **Application Layer** - Use cases, services, workflows
3. **Adapters** - Using `automodule` for adapter packages
4. **Core Models** - Data models
5. **Exceptions** - Custom exceptions
6. **Configuration** - Settings

## Adding New Classes to Documentation

To document a new class:

1. Add a docstring to your class
2. Add an `autoclass` directive in `api_reference.rst`:

```rst
My New Class
~~~~~~~~~~~~

.. autoclass:: automacao_certificados.path.to.module.MyNewClass
   :members:
   :undoc-members:
   :show-inheritance:
```

## Building Documentation

```bash
cd sphinx-docs
make html
```

The generated HTML will be in `sphinx-docs/build/html/`

## Best Practices

1. ✅ Always write a brief description (first line)
2. ✅ Document all parameters in `Args:` section
3. ✅ Document return values in `Returns:` section
4. ✅ List exceptions in `Raises:` section
5. ✅ Use type hints (they're automatically documented)
6. ✅ Keep docstrings up to date with code changes

## Full Guide

See `docstring_guide.rst` in the documentation for comprehensive examples and best practices.

