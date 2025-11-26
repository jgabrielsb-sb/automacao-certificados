Development
===========

This section is for developers who want to contribute to or extend the project.

Development Setup
-----------------

1. Follow the :ref:`installation` instructions

2. Install development dependencies:

   .. code-block:: bash

      uv sync

3. Set up your development environment:

   .. code-block:: bash

      cp .env.sample .env
      # Edit .env with your development configuration

Running Tests
-------------

Run all tests:

.. code-block:: bash

   uv run pytest

Run tests with verbose output:

.. code-block:: bash

   uv run pytest -v

Run specific test files:

.. code-block:: bash

   uv run pytest tests/selenium_automations/utils/test_utils.py

Exclude selenium workflow tests (which may require additional setup):

.. code-block:: bash

   uv run pytest -m "not selenium_workflow_tests"

Test Coverage
-------------

To check test coverage (if coverage tools are configured):

.. code-block:: bash

   uv run pytest --cov=src/automacao_certificados

Code Style
----------

The project follows Python best practices. Consider:

* Using type hints where appropriate
* Following PEP 8 style guidelines
* Writing docstrings for public APIs
* Keeping functions focused and testable

Project Structure
-----------------

Understanding the project structure is important for development. See the
:ref:`architecture` section for detailed information about:

* Layer organization
* Component responsibilities
* Design principles

Adding New Features
-------------------

When adding new features:

1. **Define Interfaces**: Start with interfaces in the core layer
2. **Implement Adapters**: Create adapter implementations
3. **Create Use Cases**: Compose adapters into use cases
4. **Write Tests**: Add comprehensive tests
5. **Update Documentation**: Keep documentation current

Debugging
---------

For debugging:

* Use Python's built-in debugger: ``import pdb; pdb.set_trace()``
* Check logs for error messages
* Review the generated reports in ``data/certificates_report/``
* Use pytest's debugging features: ``uv run pytest --pdb``

Next Steps
----------

* Read the :ref:`architecture` section to understand the design
* Check the :ref:`contributing` guidelines
* Review the :ref:`api_reference` for API details


