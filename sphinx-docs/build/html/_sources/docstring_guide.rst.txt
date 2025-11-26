Docstring Guide
================

This guide explains how to write docstrings for your code so they are properly
documented in the API Reference using Sphinx autodoc.

Docstring Format
-----------------

This project uses **Google-style docstrings** with Napoleon extension support.
This format is clean, readable, and works well with Sphinx autodoc.

Basic Structure
---------------

Class Docstring
~~~~~~~~~~~~~~~

.. code-block:: python

   class MyClass:
       """
       Brief description of the class.
       
       Longer description can go here if needed. This can span multiple
       lines and explain what the class does, its purpose, and any important
       design decisions.
       
       Attributes:
           attr1 (type): Description of attribute.
           attr2 (type): Description of another attribute.
       """
       pass

Function/Method Docstring
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def my_function(param1: str, param2: int) -> bool:
       """
       Brief description of what the function does.
       
       Longer description explaining the function's behavior, any important
       details, or usage examples.
       
       Args:
           param1: Description of the first parameter.
           param2: Description of the second parameter.
       
       Returns:
           Description of what is returned.
       
       Raises:
           ValueError: When param1 is empty.
           TypeError: When param2 is not an integer.
       
       Example:
           >>> result = my_function("test", 42)
           >>> print(result)
           True
       """
       pass

Constructor Docstring
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def __init__(self, param1: str, param2: int):
       """
       Initialize the class instance.
       
       Args:
           param1: Description of the first parameter.
           param2: Description of the second parameter.
       
       Raises:
           ValueError: When param1 is invalid.
       """
       pass

Real Examples from This Project
--------------------------------

Use Case Example
~~~~~~~~~~~~~~~~

.. code-block:: python

   class DownloadCertificatesUseCase:
       """
       Use case for downloading certificates from multiple sources.
       
       This use case orchestrates the process of:
       
       * Fetching certificates that need to be downloaded from PPE API
       * Selecting the appropriate workflow for each certificate
       * Executing the workflow to download and process certificates
       * Returning results with success/error information
       
       Attributes:
           ppe_api_requester (PPEAPIRequester): Client for PPE API.
           workflow_selector (WorkflowSelector): Selects workflows by certificate type.
       """
       
       def run(self) -> list[DownloadCertificatesUseCaseOutput]:
           """
           Execute the certificate download process.
           
           This is the main entry point. It fetches certificates to download,
           processes each one through the appropriate workflow, and returns
           the results.
           
           Returns:
               List of download results, one for each certificate processed.
           
           Raises:
               DownloadCertificatesUseCaseException: If the process fails.
           """
           pass

Interface Example
~~~~~~~~~~~~~~~~~

.. code-block:: python

   class DocumentDownloaderPort(ABC):
       """
       Interface for downloading certificate documents.
       
       This interface defines the contract for classes that download
       certificate documents from various sources and extract information
       from them.
       """
       
       @abstractmethod
       def run(self, input: DocumentDownloaderInput) -> DocumentDownloaderOutput:
           """
           Download a certificate document.
           
           Args:
               input: Contains the CNPJ and other parameters needed for download.
           
           Returns:
               Output containing the extracted document data and base64 PDF.
           
           Raises:
               DocumentDownloaderException: If download fails.
           """
           pass

Service Example
~~~~~~~~~~~~~~~

.. code-block:: python

   class CertificadoAPIService:
       """
       Service for interacting with the Certificado API.
       
       Handles supplier and document registration, including checking
       if suppliers already exist before creating new ones.
       """
       
       def register_document(
           self,
           document: dto_document.DocumentExtracted
       ) -> dto_document.DocumentResponse:
           """
           Register a document in the Certificado API.
           
           This method handles the complete registration process:
           
           1. Checks if the supplier exists, creates it if not
           2. Gets or creates the document type
           3. Registers the document with all required information
           
           Args:
               document: The extracted document data to register.
           
           Returns:
               The registered document response from the API.
           
           Raises:
               NotFoundError: If document type cannot be found.
               ConflictAPIError: If document already exists.
           """
           pass

Best Practices
--------------

1. **Always include a brief description** - The first line should be a concise summary.

2. **Use type hints** - Type hints in function signatures are automatically
   documented, but you can still describe parameters in docstrings.

3. **Document all public methods** - Private methods (starting with ``_``) are
   optional but recommended for complex logic.

4. **Be specific about exceptions** - List all exceptions that can be raised
   and when they occur.

5. **Include examples for complex functions** - Use the ``Example:`` section
   for functions that might be confusing.

6. **Document attributes** - For classes with important instance variables,
   document them in the class docstring.

7. **Keep it up to date** - Update docstrings when you change function behavior.

Common Patterns
---------------

Async Functions
~~~~~~~~~~~~~~~

.. code-block:: python

   async def fetch_data(self, url: str) -> dict:
       """
       Fetch data from a URL asynchronously.
       
       Args:
           url: The URL to fetch data from.
       
       Returns:
           Dictionary containing the fetched data.
       """
       pass

Properties
~~~~~~~~~~

.. code-block:: python

   @property
   def name(self) -> str:
       """
       Get the name of the object.
       
       Returns:
           The name string.
       """
       return self._name

Abstract Methods
~~~~~~~~~~~~~~~~

.. code-block:: python

   @abstractmethod
   def process(self, data: Any) -> Any:
       """
       Process the given data.
       
       This method must be implemented by subclasses.
       
       Args:
           data: The data to process.
       
       Returns:
           The processed data.
       """
       pass

What Gets Documented
--------------------

Sphinx autodoc will automatically document:

* **Classes** - With their docstrings, methods, and attributes
* **Functions** - With parameters, return types, and docstrings
* **Methods** - Including public and private (if configured)
* **Properties** - With their getters and setters
* **Exceptions** - Listed in Raises sections
* **Type hints** - Automatically extracted from function signatures

The API Reference uses these docstrings to generate comprehensive documentation
automatically, so writing good docstrings is essential!

