Installation
============

This project uses `uv <https://github.com/astral-sh/uv>`_ as the Python project manager.

Prerequisites
-------------

* Python 3.9 or higher
* `uv` package manager

Installing uv
-------------

If you don't have ``uv`` installed, you can install it using:

.. code-block:: bash

   curl -LsSf https://astral.sh/uv/install.sh | sh

For other installation methods, see the `uv documentation <https://github.com/astral-sh/uv>`_.

Installing the Project
----------------------

1. Clone the repository:

   .. code-block:: bash

      git clone <repository-url>
      cd automacao-certificados

2. Install dependencies:

   .. code-block:: bash

      uv sync

   This will create a virtual environment and install all required dependencies.

3. Activate the virtual environment (optional, as ``uv run`` handles this automatically):

   .. code-block:: bash

      source venv/bin/activate  # On Linux/Mac
      # or
      venv\Scripts\activate  # On Windows

Verifying Installation
----------------------

To verify that the installation was successful, you can run:

.. code-block:: bash

   uv run python -c "import automacao_certificados; print('Installation successful!')"

Next Steps
----------

After installation, proceed to:

* :ref:`configuration` - Set up your environment variables
* :ref:`quickstart` - Get started with using the project


