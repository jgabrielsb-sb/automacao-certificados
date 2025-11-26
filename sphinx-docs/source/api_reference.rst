API Reference
=============

This section contains the complete API reference for Automação Certificados.

All documentation is automatically generated from docstrings in the source code.
For guidance on writing docstrings, see the :ref:`docstring_guide`.

Core Interfaces
----------------

Base API Requester
~~~~~~~~~~~~~~~~~~

.. autoclass:: automacao_certificados.selenium_automations.core.interfaces.base_api_requester.BaseAPIRequester
   :members:
   :undoc-members:
   :show-inheritance:

Document Downloader Port
~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: automacao_certificados.selenium_automations.core.interfaces.document_downloader.DocumentDownloaderPort
   :members:
   :undoc-members:
   :show-inheritance:

Document Extractor Port
~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: automacao_certificados.selenium_automations.core.interfaces.document_extractor.DocumentExtractorPort
   :members:
   :undoc-members:
   :show-inheritance:

Document Persistence Port
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: automacao_certificados.selenium_automations.core.interfaces.document_persistance.DocumentPersistancePort
   :members:
   :undoc-members:
   :show-inheritance:

Municipio Getter Port
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: automacao_certificados.selenium_automations.core.interfaces.municipio_getter.MunicipioGetterPort
   :members:
   :undoc-members:
   :show-inheritance:

Workflow Port
~~~~~~~~~~~~~

.. autoclass:: automacao_certificados.selenium_automations.core.interfaces.workflow.WorkflowPort
   :members:
   :undoc-members:
   :show-inheritance:

Application Layer
----------------

Use Cases
~~~~~~~~~

Download Certificates Use Case
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: automacao_certificados.selenium_automations.application.use_cases.download_certificates.DownloadCertificatesUseCase
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

Services
~~~~~~~~

Certificado API Service
~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: automacao_certificados.selenium_automations.application.services.api.certificado_api_service.CertificadoAPIService
   :members:
   :undoc-members:
   :show-inheritance:

Workflows
~~~~~~~~~

Workflow
~~~~~~~~

.. autoclass:: automacao_certificados.selenium_automations.application.workflow.workflow.Workflow
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

Workflow Selector
~~~~~~~~~~~~~~~~~

.. autoclass:: automacao_certificados.selenium_automations.application.workflow.workflow_selector.WorkflowSelector
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

Workflow Factories
~~~~~~~~~~~~~~~~~~

Base Workflow Factory
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: automacao_certificados.selenium_automations.application.workflow.factories.base_workflow_factory.WorkflowFactory
   :members:
   :undoc-members:
   :show-inheritance:

Alagoas Workflow Factory
~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: automacao_certificados.selenium_automations.application.workflow.factories.alagoas_workflow_factory.AlagoasWorkflowFactory
   :members:
   :undoc-members:
   :show-inheritance:

Maceio Workflow Factory
~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: automacao_certificados.selenium_automations.application.workflow.factories.maceio_workflow_factory.MaceioWorkflowFactory
   :members:
   :undoc-members:
   :show-inheritance:

Arapiraca Workflow Factory
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: automacao_certificados.selenium_automations.application.workflow.factories.arapiraca_workflow_factory.ArapiracaWorkflowFactory
   :members:
   :undoc-members:
   :show-inheritance:

FGTS Workflow Factory
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: automacao_certificados.selenium_automations.application.workflow.factories.fgts_workflow_factory.FGTSWorkflowFactory
   :members:
   :undoc-members:
   :show-inheritance:

Adapters
--------

The adapters implement the interfaces defined in the core layer. They provide
concrete implementations for various external services and technologies.

API Requesters
~~~~~~~~~~~~~~

.. automodule:: automacao_certificados.selenium_automations.adapters.api_requester
   :members:
   :undoc-members:
   :show-inheritance:
   :imported-members:

Document Downloaders
~~~~~~~~~~~~~~~~~~~~

.. automodule:: automacao_certificados.selenium_automations.adapters.document_downloader
   :members:
   :undoc-members:
   :show-inheritance:
   :imported-members:

Extractors
~~~~~~~~~~

.. automodule:: automacao_certificados.selenium_automations.adapters.extractors
   :members:
   :undoc-members:
   :show-inheritance:
   :imported-members:

Selenium Adapters
~~~~~~~~~~~~~~~~~

.. automodule:: automacao_certificados.selenium_automations.adapters.selenium
   :members:
   :undoc-members:
   :show-inheritance:
   :imported-members:

Core Models
-----------

.. automodule:: automacao_certificados.selenium_automations.core.models
   :members:
   :undoc-members:
   :show-inheritance:

Core Exceptions
---------------

.. automodule:: automacao_certificados.selenium_automations.core.exceptions
   :members:
   :undoc-members:
   :show-inheritance:

Configuration
-------------

.. automodule:: automacao_certificados.config.config
   :members:
   :undoc-members:
   :show-inheritance:

