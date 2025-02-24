Regolith System Template
========================

A Python package that powers the `System Template Regolith Filter <https://system-template-docs.readthedocs.io/en/stable/>`_ and provides a command line tool for creating projects based on the templates defined using the System Template syntax.

Installation
-------------

.. code-block:: bash

   pip install regolith-system-template


Command Line Tool
-----------------

You can access the commandline tool by running following commoand:

.. code-block:: bash

   system-template <template-name>

This will create a new system based on the template named :code:`<template-name>`.

Before using the command line tool, you should set the :code:`REGOLITH_SYSTEM_TEMPLATE` environment variable to select the path where you can store your systems. The systems should be in subfolders of that directory stored in the same format as the one used by the Regolith filter.

Alternatively you can use :code:`--systems-path` flag to specify the path in the command.

The :code:`--scope-path` lets you specify the path to the file that contains the scope for the execution of the template. This is useful if you want to execute a template from a Regolith project. In that case, use this to specify the path to the project's global Regolith scope.

The :code:`--scope` variable lets you specify an additional scope in JSON format. This takes place of the :code:`scope` configuration option in :code:`config.json` of the Regolith project.

By default the app doesn't work in non-empty directories. It can be changed using the 
:code:`--allow-non-empty` flag.

For more help use the :code:`--help` flag.

Unlike the Regolith filter, the command line tool doesn't limit you to exporing only to :code:`RP/`, :code:`BP/` and :code:`data/` directories.

