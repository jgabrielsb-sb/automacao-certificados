Configuration
=============

The project uses environment variables for configuration. This allows you to configure
the application without modifying code.

Environment Variables
---------------------

Create a ``.env`` file in the project root directory. You can start by copying the
``.env.sample`` file:

.. code-block:: bash

   cp .env.sample .env

Then edit the ``.env`` file with your specific configuration values.

Required Configuration
----------------------

The following environment variables are typically required:

* ``PPE_API_KEY`` - API key for the PPE service
* ``RUN_CRON_TIME`` - Time to run the scheduled task (format: HH:MM)

For a complete list of available configuration options, check the ``.env.sample`` file
in the project root.

Production Configuration
------------------------

For production deployments, set the environment variables in your deployment environment
(e.g., Docker, Kubernetes, or your hosting platform). The application will automatically
read these variables at runtime.

Docker Configuration
--------------------

When using Docker, you can set environment variables in your ``docker-compose.yml`` file
or pass them directly to the container. See the :ref:`quickstart` section for Docker usage.


