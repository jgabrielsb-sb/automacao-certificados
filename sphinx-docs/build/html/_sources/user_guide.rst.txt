User Guide
==========

This section provides detailed information on how to use Automação Certificados.

Overview
--------

The main use case of this system is to:

* Receive a list of certificates that must be downloaded from an external source (PPE API)
* Select the correct workflow to download and extract the document as data models
* Send the information to be registered to an API (Certificado API)
* Send the information and the base file to PPE service (via PPE API)

How It Works
------------

The application runs on a schedule (configured via ``RUN_CRON_TIME`` environment variable).
Each time it runs, it:

1. Fetches certificates that need to be downloaded from the PPE API
2. For each certificate:
   - Determines the appropriate workflow based on CNPJ and document type
   - Downloads the certificate from the appropriate source
   - Extracts relevant information
   - Processes and stores the data
3. Generates a report of the download process

Workflows
---------

The system supports multiple workflows for different certificate sources:

* **Caixa Website** - For certificates from Caixa
* **Maceió Website** - For municipal certificates from Maceió
* **Other sources** - Additional sources as configured

The workflow is automatically selected based on the certificate's CNPJ and document type.

Reports
-------

After each run, the system generates a report in HTML format. Reports are saved in the
``data/certificates_report/`` directory with timestamps.

The report includes:

* List of certificates processed
* Success/failure status for each certificate
* Any errors encountered during processing
* Timestamp of the run

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Issue: Certificates not downloading**

* Check your API keys in the ``.env`` file
* Verify network connectivity
* Check the logs for specific error messages

**Issue: Workflow selection errors**

* Ensure the CNPJ and document type are valid
* Verify that a workflow exists for the given certificate type

**Issue: Scheduled runs not executing**

* Verify the ``RUN_CRON_TIME`` format (HH:MM)
* Check that the application is running continuously
* Review system logs for errors

Getting Help
------------

If you encounter issues not covered here:

* Check the :ref:`development` section for development-related questions
* Review the :ref:`api_reference` for API details
* Consult the project's issue tracker or contact the maintainers


