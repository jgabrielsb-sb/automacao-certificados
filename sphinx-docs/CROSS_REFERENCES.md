# Cross-References in Sphinx Documentation

## Overview

Cross-references allow users to click on type names, classes, and functions in your documentation to navigate to their definitions. This makes documentation much more useful and navigable.

## What I've Added

### 1. Model Documentation in API Reference

Added detailed documentation for core models:
- `DocumentDownloaderInput` - Input model for document downloaders
- `DocumentDownloaderOutput` - Output model for document downloaders
- Other interface models (persistence, workflow, etc.)
- Application models (use cases, workflow selector)
- Data transfer objects (documents, suppliers, document types)

### 2. Cross-Reference Roles in Docstrings

Updated docstrings to use Sphinx cross-reference roles:

**Before:**
```python
def run(self, input: DocumentDownloaderInput) -> DocumentDownloaderOutput:
    """
    :param input: The input parameters.
    :type input: DocumentDownloaderInput
    :rtype: DocumentDownloaderOutput
    """
```

**After:**
```python
def run(self, input: DocumentDownloaderInput) -> DocumentDownloaderOutput:
    """
    Args:
        input: See :class:`DocumentDownloaderInput` for details.
    
    Returns:
        See :class:`DocumentDownloaderOutput` for the structure.
    """
```

### 3. Automatic Type Hint Cross-Referencing

Enabled `autodoc_typehints = 'description'` in `conf.py`, which automatically creates cross-references from type hints in function signatures.

## How Cross-References Work

### Using Roles in Docstrings

Sphinx provides several roles for creating cross-references:

- **`:class:`** - Link to a class
  ```python
  See :class:`DocumentDownloaderOutput` for details.
  ```

- **`:exc:`** - Link to an exception
  ```python
  Raises:
      :exc:`DocumentDownloaderException`: If download fails.
  ```

- **`:func:`** - Link to a function
  ```python
  Uses :func:`validate_cnpj` to validate the CNPJ.
  ```

- **`:mod:`** - Link to a module
  ```python
  See :mod:`automacao_certificados.selenium_automations.core.models`.
  ```

- **`:attr:`** - Link to an attribute
  ```python
  The :attr:`DocumentDownloaderOutput.base64_pdf` attribute.
  ```

- **`:meth:`** - Link to a method
  ```python
  Call :meth:`DocumentDownloaderPort.run` to download.
  ```

### Full vs Short Names

You can use either:

```python
# Full path (always works, but verbose)
:class:`automacao_certificados.selenium_automations.core.models.interfaces.dto_document_downloader.DocumentDownloaderOutput`

# Short name (works if imported in current module)
:class:`DocumentDownloaderOutput`
```

**Best Practice:** Use short names when the class is imported in the current module.

## Example

Here's a complete example with cross-references:

```python
class DocumentDownloaderPort(ABC):
    """
    Interface for downloading certificate documents.
    
    This interface uses :class:`DocumentDownloaderInput` for input parameters
    and returns :class:`DocumentDownloaderOutput` with the extracted data.
    """
    
    def run(
        self, 
        input: DocumentDownloaderInput
    ) -> DocumentDownloaderOutput:
        """
        Download a certificate document.
        
        Args:
            input: See :class:`DocumentDownloaderInput` for details.
        
        Returns:
            See :class:`DocumentDownloaderOutput` for the structure.
        
        Raises:
            :exc:`DocumentDownloaderException`: If download fails.
        """
        pass
```

## Benefits

1. **Clickable Links** - Users can click on type names to see their definitions
2. **Better Navigation** - Easy to explore related classes and functions
3. **Self-Documenting** - Documentation becomes a web of interconnected information
4. **Type Safety** - Sphinx validates that referenced objects exist

## Testing

After rebuilding your documentation:

```bash
cd sphinx-docs
make html
```

Open the generated HTML and check that:
- Type names in docstrings are clickable links
- Links navigate to the correct class/function definitions
- All referenced objects are properly documented

## Next Steps

1. Add cross-references to other docstrings throughout your codebase
2. Add docstrings to model classes that don't have them yet
3. Use cross-references consistently for better documentation navigation

For more details, see the `docstring_guide.rst` section in your documentation.

