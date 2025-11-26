Architecture
============

This document describes the architecture and design of the Automação Certificados project.

Project Structure
-----------------

The project follows a layered architecture with clear separation of concerns:

* **Ports (Interfaces)**: Define the general behavior and contracts
* **Adapters**: Implement the interfaces with specific technologies
* **Application**: Orchestration layer where objects are composed to create usable use cases

Layer Overview
--------------

Ports (Interfaces)
~~~~~~~~~~~~~~~~~~

Located in ``src/automacao_certificados/selenium_automations/core/interfaces/``

These define the contracts that adapters must implement. They specify:

* What operations are available
* Expected inputs and outputs
* Behavior contracts

Adapters
~~~~~~~~

Located in ``src/automacao_certificados/selenium_automations/adapters/``

Adapters implement the interfaces defined in ports. They handle:

* **API Requesters**: Communication with external APIs (PPE API, Certificado API, etc.)
* **Document Downloaders**: Downloading certificates from various sources
* **Extractors**: Extracting information from downloaded documents
* **Selenium**: Web automation for certificate sources
* **Persistence**: Storing and retrieving data
* **Report Generators**: Creating reports from processed data

Application Layer
~~~~~~~~~~~~~~~~~

Located in ``src/automacao_certificados/selenium_automations/application/``

This layer orchestrates the adapters to create use cases:

* **Use Cases**: High-level business logic (e.g., ``DownloadCertificatesUseCase``)
* **Services**: Reusable business logic components
* **Workflows**: Step-by-step processes for specific certificate types

Core Components
---------------

Models
~~~~~~

Located in ``src/automacao_certificados/selenium_automations/core/models/``

Data models representing:

* Certificates
* Workflow inputs/outputs
* API request/response structures

Exceptions
~~~~~~~~~~

Located in ``src/automacao_certificados/selenium_automations/core/exceptions/``

Custom exceptions for error handling throughout the application.

Main Use Case Flow
------------------

The main use case (``DownloadCertificatesUseCase``) follows this flow:

1. **Fetch Certificates**: Get list of certificates to download from PPE API
2. **Select Workflow**: For each certificate, determine the appropriate workflow
3. **Execute Workflow**: Run the workflow to download and process the certificate
4. **Handle Results**: Collect outputs and handle any errors
5. **Generate Report**: Create a report of the entire process

Workflow Selection
------------------

The ``WorkflowSelector`` determines which workflow to use based on:

* **CNPJ**: The company's CNPJ number
* **Document Type**: The type of certificate needed

This allows the system to route different certificate types to their appropriate
processing workflows.

Design Principles
-----------------

* **Separation of Concerns**: Clear boundaries between layers
* **Dependency Inversion**: High-level modules depend on abstractions (interfaces)
* **Single Responsibility**: Each component has a focused purpose
* **Open/Closed**: Open for extension, closed for modification

Extensibility
-------------

To add support for a new certificate source:

1. Create a new workflow in the application layer
2. Implement any required adapters
3. Update the workflow selector to route to the new workflow
4. Add tests for the new components


