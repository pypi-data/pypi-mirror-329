PyAwaish
===========

**PyAwaish** is a Flask-based Python framework that simplifies the development of MySQL-powered web applications. It provides a streamlined interface for connecting to a MySQL database, rendering templates, and executing queries dynamically via RESTful APIs.

Features
--------

- **Dynamic MySQL Configuration**: Configure MySQL database settings at runtime via a web interface.
- **Template Rendering**: Built-in support for rendering templates stored in the ``templates`` folder.
- **Query Execution API**: Execute MySQL queries dynamically through POST requests.
- **CRUD Operations**: Perform create, read, update, and delete operations programmatically.
- **RESTful Design**: Leverage Flask to expose endpoints for database interactions.
- **Environment Configuration**: Load sensitive credentials securely using environment variables.

Badges
------

.. image:: https://badge.fury.io/py/PyAwaish.svg
    :target: https://pypi.org/project/PyAwaish/

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT

Endpoints
---------

1. **`/`**: Displays the MySQL configuration page.
2. **`/home`**: Displays the home page.
3. **`/config_mysql`**: Accepts a POST request to configure MySQL connection details dynamically.
4. **`/execute_query`**: Accepts a POST request to execute MySQL queries or perform operations (e.g., insert, delete, update).

Installation
------------

1. Clone the repository:

   .. code-block:: bash

       git clone https://github.com/abuawaish/CRUD_App.git
       cd CRUD_App

2. Install the required dependencies:

   .. code-block:: bash

       pip install -r requirements.txt

3. Install the package:

   .. code-block:: bash

       pip install PyAwaish

4. Set environment variables for database configuration:

   .. code-block:: bash

       export MYSQL_HOST=localhost
       export MYSQL_USER=root
       export MYSQL_PASSWORD=your password
       export MYSQL_DB=mydatabase
       export SECRET_KEY=your_secret_key


Usage
-----

**Running the Application**

To start the Mysql Web Application server, instantiate the ``MysqlApplication`` class and call its ``execute`` method. For example:

.. code-block:: python

    from PyAwaish.MysqlApplication import MysqlApplication

    if __name__ == "__main__":
        # Initialize MysqlApplication with a secret key
        # Options:
        # 1. Pass the full path of the .env file: MysqlApplication(secret_key=r"full_path_to_env")
        # 2. Pass only the file name if it's in the working directory: MysqlApplication(secret_key=".env")
        # 3. Leave it empty: MysqlApplication()
        # 4. Use a custom string as the secret key:
        app = MysqlApplication(secret_key="your_secret_key")

        # Execute the application
        app.execute()


**This will:**

- Start a Flask server on ``http://0.0.0.0:5001``.
- Serve endpoints for configuring and interacting with the MySQL database.

Function Signature:
-------------------

The ``execute()`` function is used to start the Flask server with customizable parameters.

.. code-block:: python

    def execute(self, debug_mode: bool = False, port_number: int = 5001, host_address: str = "0.0.0.0") -> None:

Parameters:
-----------

- ``debug_mode`` (bool, optional): Enables or disables Flask's debug mode. Default is ``False``.
- ``port_number`` (int, optional): The port number on which the application runs. Default is ``5001``.
- ``host_address`` (str, optional): The host address to bind the server. Default is ``"0.0.0.0"`` (accessible on all network interfaces).

Example Usage:
--------------

.. code-block:: python

    app = MysqlApplication()
    app.execute(debug_mode=True, port_number=8080, host_address="127.0.0.1")

This will run the application in debug mode on localhost (``127.0.0.1``) at port ``8080``.

Initializing MysqlApplication with a Secret Key
-----------------------------------------------

The ``MysqlApplication`` class from ``PyAwaish.MysqlApplication`` requires a secret key for initialization.
This secret key is used for configuration, authentication, or security purposes within the application.
You can provide the secret key in different ways:

1. **Using a `.env` file (Full Path)**

   .. code-block:: python

      app = MysqlApplication(secret_key=r"C:\path\to\.env")

   - Provide the full path to a ``.env`` file that contains necessary environment variables.

2. **Using a `.env` file (Relative Path)**

   .. code-block:: python

      app = MysqlApplication(secret_key=".env")

   - If the ``.env`` file is located in the working directory, you can pass just the filename.

3. **Without a Secret Key**

   .. code-block:: python

      app = MysqlApplication()

   - If no secret key is provided, the application may use default settings.

4. **Using a Custom Secret Key String**

   .. code-block:: python

      app = MysqlApplication(secret_key="your_secret_key")

   - You can directly pass a custom string as the secret key.



Setting Up Secret Key with .env File
------------------------------------

**To securely store and use a secret key in your app, follow these steps:**

**1. Create a `.env` file in the root directory of your project.**

**2. Inside the `.env` file, add the following line:**

.. code-block:: bash

   SECRET_KEY = "YOUR_SECRET_KEY"


Executing the Application
-------------------------

After initialization, you can execute the application using:

.. code-block:: python

   app.execute()

**Configuring MySQL**

1. Navigate to the root endpoint (``http://localhost:5001/``) to access the configuration page.
2. Enter the database details (host, username, password, database name) and click on ``Configure Database``.
3. Upon successful configuration, you will be redirected to the home page.

**Executing Queries**

Use the ``/execute_query`` endpoint to run SQL queries or perform operations. Example request:

- **POST Request Example**:

  .. code-block:: json

      {
          "operation": "insert",
          "table_name": "users",
          "columns": "name, email",
          "values": "'John Doe', 'john@example.com'"
      }

- **Supported Operations**:

  - ``insert``: Insert data into a table.
  - ``delete``: Delete data from a table with a condition.
  - ``update``: Update data in a table with a condition.
  - ``fetch_data``: Fetch all data from a table.
  - ``show_tables``: List all tables in the database.

Dependencies
------------

The application requires the following dependencies (listed in ``requirements.txt``):

- ``Flask``: Web framework.
- ``Flask-MySQLdb``: MySQL connector for Flask.
- ``python-dotenv``: It loads environment variables from a .env file into os.environ.

To install them, run:

.. code-block:: bash

    pip install -r requirements.txt

Environment Variables
---------------------

- **MYSQL_HOST**: MySQL server hostname (default: ``localhost``).
- **MYSQL_USER**: MySQL username (default: ``root``).
- **MYSQL_PASSWORD**: MySQL password.
- **MYSQL_DB**: Default MySQL database name.
- **SECRET_KEY**: Flask secret key for session security.

Changelog
---------

Refer to ``CHANGELOG.txt`` for the complete version history of the project.

License
-------

This project is licensed under the MIT License. See ``LICENSE.txt`` for full details.

Contact
-------

For questions or feedback, contact:

- Email: abuawaish7@gmail.com
- GitHub: https://github.com/abuawaish

