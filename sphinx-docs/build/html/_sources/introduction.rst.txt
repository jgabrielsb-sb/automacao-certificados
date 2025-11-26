Introduction
============

.. _what_is_this_project_about:


What is this project about?
-------------

This project is intended to be a system that automates the process of:

* downloading PDF certificate documents from several sources (Caixa website, Maceió Website, etc);
* extracting the relevant information of those documents;
* registering the relevant information of those documents on a database via external services;
* sending the document to PPE Sebrae service;

.. _how_is_this_project_structured:

How is this project structured?
----------

This project follows a separation by layers:

* ports (interfaces): defines the general behavior of some object.
* adapters: defines the implementation of the interfaces.
* application: the orchestration layer where the objects are composed to create usable use cases;

    
.. _the_main_use_case:

What is the main use case?
--------------------------

The main use case of this system is to:

* receive a list of certificates that must be downloaded by some kind of external source (PPE API on this case);
* select the correct workflow to download and extract the document as data models;
* send the information to be registered to an API (on this case, Certificado API);
* send the information and the base file to PPE service (via PPE API);