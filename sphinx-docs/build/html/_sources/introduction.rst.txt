Introduction
============

What is Automação Certificados?
--------------------------------

Automação Certificados is a Python-based automation system designed to streamline the process
of managing certificate documents. The system automates:

* **Downloading** PDF certificate documents from multiple sources (Caixa website, Maceió Website, etc.)
* **Extracting** relevant information from those documents
* **Registering** the extracted information in databases via external services
* **Sending** documents and data to the PPE Sebrae service

Key Features
------------

* **Multi-Source Support**: Handles certificates from various sources
* **Automated Workflow**: Automatically selects and executes the appropriate workflow for each certificate
* **Scheduled Execution**: Runs on a configurable schedule
* **Report Generation**: Creates detailed reports of all processing activities
* **Error Handling**: Robust error handling and reporting

Project Architecture
--------------------

This project follows a **layered architecture** with clear separation of concerns:

* **Ports (Interfaces)**: Define the general behavior and contracts that components must follow
* **Adapters**: Implement the interfaces with specific technologies and external services
* **Application**: Orchestration layer where objects are composed to create usable use cases

This architecture promotes:

* **Maintainability**: Clear boundaries between components
* **Testability**: Easy to mock and test individual components
* **Extensibility**: Simple to add new certificate sources or workflows

For more details, see the :ref:`architecture` section.

Main Use Case
-------------

The primary use case of this system is to:

1. **Receive** a list of certificates that must be downloaded from an external source (PPE API)
2. **Select** the correct workflow to download and extract the document based on certificate type
3. **Process** the certificate, extracting relevant information as structured data models
4. **Register** the information via API (Certificado API)
5. **Send** the information and the base file to the PPE service (via PPE API)

The system handles the entire process automatically, requiring minimal manual intervention.

Getting Started
---------------

New to the project? Start here:

1. Read this introduction to understand what the project does
2. Follow the :ref:`installation` guide to set up your environment
3. Configure the application using the :ref:`configuration` guide
4. Run your first execution with the :ref:`quickstart` guide

For detailed usage information, see the :ref:`user_guide`.

For Developers
--------------

If you're looking to contribute or extend the project:

* Review the :ref:`architecture` documentation to understand the design
* Check the :ref:`development` guide for setup and testing
* Read the :ref:`contributing` guidelines before submitting changes
* Explore the :ref:`api_reference` for API documentation