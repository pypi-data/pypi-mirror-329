Command Line Interface
======================

This package offers a unified command line interface to Yeedu's `RESTful-API <https://docs.yeedu.io/restapi/swagger-docs>`__.

Getting Started
---------------

-  `Requirements <#requirements>`__
-  `Installation <#installation>`__
-  `Configuration <#configuration>`__
-  `Environment Variables <#environment-variables>`__
-  `Credentials File <#credentials-file>`__
-  `Yeedu Session Token <#yeedu-session-token>`__
-  `Basic Commands <#basic-commands>`__

Requirements
~~~~~~~~~~~~

The yeedu-cli package works on Python version:

-  3.8.x and greater

Installation
~~~~~~~~~~~~

Installation of the Yeedu CLI and its dependencies use a range of packaging features provided by `pip` and `setuptools`. To ensure smooth installation, it's recommended to use:

-  pip: `20.0.2` or greater
-  setuptools: `59.6.0` or greater

.. code-block:: bash

    python3 -m pip install yeedu-cli

Configuration
~~~~~~~~~~~~~

Before using the Yeedu CLI, you need to configure your credentials. You can do this in several ways:

-  Environment Variables
-  Credentials file

`Note`: Environment variables are given priority.

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Below mentioned values are the default values of Environment Variables 
   YEEDU_RESTAPI_URL="http://localhost:8080"
   YEEDU_CLI_LOG_DIR="/.yeedu/cli/logs/"
   YEEDU_USERNAME=USER
   YEEDU_PASSWORD=PASS
   YEEDU_RESTAPI_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFiY2RlZiIsImlkIjoiMSIsImlhdCI6MTY2NzgwOTYwMX0.HwhdTHBttnR0NFtmUDjcxTLMSLfyNuBs7t7GO9zOf08
   YEEDU_RESTAPI_TOKEN_FILE_PATH="/home/user/yeedu_cli.config"
   YEEDU_CLI_VERIFY_SSL=true

   # Provide the YEEDU_SSL_CERT_FILE path if YEEDU_CLI_VERIFY_SSL is set to true. 
   YEEDU_SSL_CERT_FILE="/home/user/crt"

Credentials File
~~~~~~~~~~~~~~~~

The `yeedu_credentials.config` file needs to be created inside the directory `home/user/.yeedu/` and should contain JSON formatted as shown below:

.. code-block:: json

   {
     "YEEDU_USERNAME": "USER",
     "YEEDU_PASSWORD": "PASS"
   }

Yeedu Session Token
~~~~~~~~~~~~~~~~~~~

If the user already has the Yeedu Session Token, they can save the token at any location and provide the file path in the environment variable `YEEDU_RESTAPI_TOKEN_FILE_PATH`.

For example:

.. code-block:: bash

    YEEDU_RESTAPI_TOKEN_FILE_PATH="/home/user/{FileName}"

-  The format for storing the token is shown below:

.. code-block:: json

   {
     "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJpYXQiOjE2ODg3MjA0MjIsImV4cCI6MTY4ODg5MzIyMn0.EfxuXKPBISQB4ep-sPQbo6R7tg2irlnAC_krqnuXJ5Q"
   }

Basic Commands
~~~~~~~~~~~~~~

Yeedu CLI command has the following structure:

.. code-block:: bash

   yeedu <command> <subcommand> [options and parameters]

For example, to list clusters, the command would be:

.. code-block:: bash

   yeedu cluster list

To view help documentation, use one of the following:

.. code-block:: bash

   yeedu --help
   yeedu <command> --help
   yeedu <command> <subcommand> --help

You can read more information on the `Yeedu CLI Commands <https://docs.yeedu.io/cli/commands>`__.