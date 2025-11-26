Quickstart
==========

This guide will help you get started with Automação Certificados quickly.

Prerequisites
-------------

Before you begin, make sure you have:

* Completed the :ref:`installation` process
* Set up your :ref:`configuration` (environment variables)

Running in Development
----------------------

To run the project locally in development mode:

1. Ensure you've installed dependencies:

   .. code-block:: bash

      uv sync

2. Set up your environment variables (see :ref:`configuration`):

   .. code-block:: bash

      cp .env.sample .env
      # Edit .env with your configuration

3. Run the main script:

   .. code-block:: bash

      uv run python src/automacao_certificados/main.py

The application will run and execute the certificate download process according to
your scheduled configuration.

Running in Production
---------------------

For production deployments, use Docker:

1. Set the required environment variables in your deployment environment or ``docker-compose.yml``

2. Build and run with Docker Compose:

   .. code-block:: bash

      docker compose up --build

This will start the application in a containerized environment.

Running Tests
-------------

To run the test suite:

.. code-block:: bash

   uv run pytest

To exclude selenium workflow tests (which may require additional setup):

.. code-block:: bash

   uv run pytest -m "not selenium_workflow_tests"

Next Steps
----------

* Read the :ref:`user_guide` for detailed usage information
* Check the :ref:`architecture` section to understand the project structure
* Explore the :ref:`api_reference` for API documentation


