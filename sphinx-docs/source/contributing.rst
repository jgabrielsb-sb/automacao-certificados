Contributing
============

Thank you for your interest in contributing to Automação Certificados!

Getting Started
---------------

1. Fork the repository
2. Clone your fork locally
3. Follow the :ref:`installation` and :ref:`development` setup instructions
4. Create a new branch for your changes

Development Workflow
--------------------

1. **Create a Feature Branch**: Use a descriptive name (e.g., ``feature/add-new-workflow``)

2. **Make Your Changes**: 
   * Follow the project's architecture patterns
   * Write tests for new functionality
   * Update documentation as needed

3. **Run Tests**: Ensure all tests pass

   .. code-block:: bash

      uv run pytest

4. **Check Code Quality**: Ensure your code follows project standards

5. **Commit Changes**: Write clear, descriptive commit messages

6. **Push and Create Pull Request**: Push your branch and open a PR

Code Standards
--------------

* **Type Hints**: Use type hints for function parameters and return values
* **Docstrings**: Document public classes, methods, and functions
* **Testing**: Write tests for new features and bug fixes
* **Naming**: Use descriptive names following Python conventions

Pull Request Guidelines
------------------------

When submitting a pull request:

* **Description**: Clearly describe what the PR does and why
* **Tests**: Include tests for new functionality
* **Documentation**: Update relevant documentation
* **Breaking Changes**: Clearly mark any breaking changes

Testing Requirements
--------------------

* All new features should include tests
* Tests should be in the ``tests/`` directory
* Follow the existing test structure and naming conventions
* Ensure tests pass before submitting a PR

Documentation
-------------

When adding features:

* Update relevant documentation sections
* Add docstrings to new public APIs
* Include usage examples where appropriate
* Update the :ref:`api_reference` if adding new public APIs

Questions?
----------

If you have questions about contributing:

* Check the :ref:`development` section
* Review the :ref:`architecture` documentation
* Open an issue for discussion

Thank you for contributing!


