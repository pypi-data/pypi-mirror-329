nuvolos - The database connectivity library for Nuvolos
=======================================================

Installation
============

.. code:: bash

    $ pip install --upgrade nuvolos

Connecting to Snowflake with Nuvolos Connector
==============================================

1. Using SQLAlchemy with Username/Password
------------------------------------------

.. code-block:: python

    from nuvolos import get_connection
    from sqlalchemy import text

    # Connect using username and password
    conn = get_connection(
        username="your_username",
        password="your_password",
        dbname="YOUR_DB",
        schemaname="YOUR_SCHEMA"
    )

    try:
        # Execute a query
        result = conn.execute(text("SELECT * FROM YOUR_TABLE"))
        for row in result:
            print(row)
    finally:
        conn.close()

2. Using SQLAlchemy with RSA Key
--------------------------------

.. code-block:: python

    import os
    from nuvolos import get_connection
    from sqlalchemy import text
    
    # Set environment variables for RSA authentication
    os.environ["SNOWFLAKE_RSA_KEY"] = "/path/to/rsa_key.p8"
    os.environ["SNOWFLAKE_RSA_KEY_PASSPHRASE"] = "your_key_passphrase"  # Optional

    # Connect using RSA key authentication
    conn = get_connection(
        username="YOUR_USERNAME",
        dbname="YOUR_DB",
        schemaname="YOUR_SCHEMA"
    )

    try:
        # Execute a query
        result = conn.execute(text("SELECT * FROM YOUR_TABLE"))
        for row in result:
            print(row)
    finally:
        conn.close()

3. Using Raw Connector with Username/Password
---------------------------------------------

.. code-block:: python

    from nuvolos import get_raw_connection

    # Connect using username and password
    conn = get_raw_connection(
        username="your_username",
        password="your_password",
        dbname="YOUR_DB",
        schemaname="YOUR_SCHEMA"
    )

4. Using Raw Connector with RSA Key
-----------------------------------

.. code-block:: python

    import os
    from nuvolos import get_raw_connection

    # Set environment variables for RSA authentication
    os.environ["SNOWFLAKE_RSA_KEY"] = "/path/to/rsa_key.p8"
    os.environ["SNOWFLAKE_RSA_KEY_PASSPHRASE"] = "your_key_passphrase"  # Optional

    # Connect using RSA key authentication
    conn = get_raw_connection(
        username="YOUR_USERNAME",
        dbname="YOUR_DB",
        schemaname="YOUR_SCHEMA"
    )

Documentation and examples available at: https://docs.nuvolos.cloud/data/access-data-from-applications#connecting-with-python