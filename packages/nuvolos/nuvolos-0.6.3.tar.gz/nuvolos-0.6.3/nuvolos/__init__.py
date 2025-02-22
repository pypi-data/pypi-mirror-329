import getpass
import logging
import os
import re
from urllib.parse import quote

import keyring
import snowflake.connector
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from .version import __version__
from .sql_utils import to_sql


logger = logging.getLogger(__name__)

__NUVOLOS_KEY_PATH = "/secrets/snowflake_rsa_private_key"
__NUVOLOS_PATH = "/secrets"


def load_env_var(env_var_name, description, print_value=False):
    var = os.getenv(env_var_name)
    if var is None:
        logger.debug(f"Could not find {description} in env var {env_var_name}")
    else:
        if print_value:
            logger.debug(f"Found {description} {var} in env var {env_var_name}")
        else:
            logger.debug(f"Found {description} in env var {env_var_name}")
    return var


def credd_from_env_vars():
    username = load_env_var("NUVOLOS_USERNAME", "username", print_value=True)
    password = load_env_var("NUVOLOS_SF_TOKEN", "Snowflake token", print_value=False)
    if username is None or password is None:
        return None
    else:
        return {"username": username, "snowflake_access_token": password}


def credd_from_secrets():
    username_filename = os.getenv("NUVOLOS_USERNAME_FILENAME", "/secrets/username")
    snowflake_access_token_filename = os.getenv(
        "NUVOLOS_SNOWFLAKE_ACCESSS_TOKEN_FILENAME",
        "/secrets/snowflake_access_token",
    )
    if not os.path.exists(username_filename):
        logger.debug(f"Could not find secret file {username_filename}")
        return None
    if not os.path.exists(snowflake_access_token_filename) and not _is_key_pair_auth():
        logger.debug(f"Could not find secret file {snowflake_access_token_filename}")
        return None
    if _is_key_pair_auth():
        with open(username_filename) as username, open(
            snowflake_access_token_filename
        ) as access_token:
            username = username.readline()
            logger.debug("Found username in /secrets file")
            return {"username": username, "snowflake_access_token": None}
    else:
        with open(username_filename) as username, open(
            snowflake_access_token_filename
        ) as access_token:
            username = username.readline()
            password = access_token.readline()
            logger.debug("Found username and Snowflake access token in /secrets files")
            return {"username": username, "snowflake_access_token": password}


def input_nuvolos_credential():
    # store username & password
    username = getpass.getpass("Please input your Nuvolos username:")
    keyring.set_password("nuvolos", "username", username)

    if not _is_key_pair_auth():
        password = getpass.getpass("Please input your Nuvolos password:")
        keyring.set_password("nuvolos", username, password)


def credd_from_local():
    # retrieve username & password
    username = keyring.get_password("nuvolos", "username")
    password = None
    if not _is_key_pair_auth():
        password = keyring.get_password("nuvolos", username) if username else None
    return {"username": username, "snowflake_access_token": password}


def dbpath_from_file(path_filename):
    if not os.path.exists(path_filename):
        logger.debug(f"Could not find dbpath file {path_filename}")
        return None
    with open(path_filename, "r") as path_file:
        lines = path_file.readlines()
        if len(lines) == 0:
            logger.debug(f"Could not parse dbpath file: {path_filename} is empty.")
            return None
        first_line = lines[0].rstrip()
        if "Tables are not enabled" in first_line:
            raise Exception(
                "Tables are not enabled for this space, please enable them first."
            )
        # Split at "." character
        # This should have resulted in two substrings
        split_arr = re.split('"."', first_line)
        if len(split_arr) != 2:
            logger.debug(
                f'Could not parse dbpath file: pattern "." not found in {path_filename}. '
                f"Are the names escaped with double quotes?"
            )
            return None
        # Remove the remaining double quotes, as we'll escape those
        db_name = split_arr[0].replace('"', "")
        schema_name = split_arr[1].replace('"', "")
        logger.debug(
            f"Found database = {db_name}, schema = {schema_name} in dbpath file {path_filename}."
        )
        return {"db_name": db_name, "schema_name": schema_name}


def dbpath_from_env_vars():
    db_name = load_env_var("NUVOLOS_DB", "Snowflake database", print_value=True)
    schema_name = load_env_var("NUVOLOS_SCHEMA", "Snowflake schema", print_value=True)
    if db_name is None or schema_name is None:
        return None
    return {"db_name": db_name, "schema_name": schema_name}


def _is_key_pair_auth() -> bool:
    private_key_path = os.getenv("SNOWFLAKE_RSA_KEY", __NUVOLOS_KEY_PATH)
    if __NUVOLOS_KEY_PATH == private_key_path:
        if os.path.exists(__NUVOLOS_PATH):
            # We assume that the user is running on Nuvolos
            if not os.path.exists(__NUVOLOS_KEY_PATH):
                raise FileNotFoundError(
                    f"Private key file for database connection [{__NUVOLOS_KEY_PATH}] not found."
                )
            else:
                return True
        else:
            # If the path does not exist, we assume that the user is not running on Nuvolos
            return False
    return os.path.exists(private_key_path)


def _get_connection_params(username=None, password=None, dbname=None, schemaname=None):
    if username is None and password is None:
        credd = credd_from_secrets() or credd_from_env_vars() or credd_from_local()
        if (
            credd is None
            or credd.get("username") is None
            or credd.get("snowflake_access_token") is None
        ):
            input_nuvolos_credential()
            credd = credd_from_local()

        username = credd["username"]
        password = credd["snowflake_access_token"]
    elif username is not None and password is None and not _is_key_pair_auth():
        raise ValueError(
            "You have provided a username but not a password. "
            "Please provite a password or set the SNOWFLAKE_RSA_KEY environment variable."
        )
    elif username is None and password is not None:
        raise ValueError(
            "You have provided a password but not a username. "
            "Please either provide both arguments or leave both arguments empty."
        )
    else:
        logger.debug("Found username and Snowflake access token as input arguments")

    if dbname is None and schemaname is None:
        path_filename = os.getenv("NUVOLOS_DBPATH_FILE", "/lifecycle/.dbpath")
        dbd = (
            dbpath_from_file(path_filename)
            or dbpath_from_file(".dbpath")
            or dbpath_from_env_vars()
        )
        if dbd is None:
            raise ValueError(
                "Could not find Snowflake database and schema in .dbpath files or env vars. "
                "If you're not using this function from Nuvolos, "
                "please specify the Snowflake database and schema names as input arguments"
            )
        else:
            db_name = dbd["db_name"]
            schema_name = dbd["schema_name"]
    elif dbname is not None and schemaname is None:
        raise ValueError(
            "You have provided a dbname argument but not a schemaname argument. "
            "Please either provide both or provide none of them."
        )
    elif dbname is None and schemaname is not None:
        raise ValueError(
            "You have provided a schemaname argument but not a dbname argument. "
            "Please either provide both or provide none of them."
        )
    else:
        db_name = dbname
        schema_name = schemaname
        logger.debug("Found database and schema as input arguments")

    default_snowflake_host = (
        "acstg.eu-central-1" if "STAGING/" in db_name else "alphacruncher.eu-central-1"
    )
    snowflake_host = os.getenv("NUVOLOS_SNOWFLAKE_HOST", default_snowflake_host)
    return username, password, snowflake_host, db_name, schema_name


def get_url(username=None, password=None, dbname=None, schemaname=None) -> URL:
    """
    Returns an SQLAlchemy connection URL which can be used to create a connection to Nuvolos.
    :param username: Nuvolos user name.
    :param password: Nuvolos password.
    :param dbname: Nuvolos database name from the Connection Guide.
    :param schemaname: Nuvolos schema name from the Connection Guide.
    :return: An SQLAlchemy connection URL representing the Nuvolos connection.
    """
    username, password, snowflake_host, db_name, schema_name = _get_connection_params(
        username=username, password=password, dbname=dbname, schemaname=schemaname
    )

    # Add RSA key authentication if configured
    if _is_key_pair_auth():
        masked_url = f"snowflake://{quote(username)}:'RSA_KEY'@{snowflake_host}"
    else:
        masked_url = f"snowflake://{quote(username)}:'********'@{snowflake_host}"

    params = (
        "/?database=%22"
        + quote(db_name)
        + "%22"
        + "&schema=%22"
        + quote(schema_name)
        + "%22"
        + "&CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX=TRUE"
        + "&VALIDATEDEFAULTPARAMETERS=TRUE"
    )
    masked_url = masked_url + params

    logger.debug("Built SQLAlchemy URL: " + masked_url)
    if password:
        return URL(
            account=snowflake_host,
            user=username,
            password=password,
            database=db_name,
            schema=schema_name,
            numpy=True,
        )
    else:
        return URL(
            account=snowflake_host,
            user=username,
            database=db_name,
            schema=schema_name,
            numpy=True,
        )


def get_engine(username=None, password=None, dbname=None, schemaname=None):
    """
    Returns an SQLAlchemy Engine object which can be used with Pandas read_sql/to_sql functions.
    :param username: Nuvolos user name.
    :param password: Nuvolos password.
    :param dbname: Nuvolos database name from the Connection Guide.
    :param schemaname: Nuvolos schema name from the Connection Guide.
    :return: A SQLAlchemy Engine object.
    """

    connect_args = {
        "QUERY_TAG": f"nuvolos {__version__}",
        "CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX": True,
        "VALIDATEDEFAULTPARAMETERS": True,
    }

    if _is_key_pair_auth():
        private_key_path = os.getenv("SNOWFLAKE_RSA_KEY", __NUVOLOS_KEY_PATH)
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives.asymmetric import dsa
        from cryptography.hazmat.primitives import serialization

        password = os.getenv("SNOWFLAKE_RSA_KEY_PASSPHRASE", None)
        with open(private_key_path, "rb") as key:
            p_key = serialization.load_pem_private_key(
                key.read(),
                password=password.encode() if password is not None else None,
                backend=default_backend(),
            )

        pkb = p_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        connect_args["private_key"] = pkb

    return create_engine(
        url=get_url(username, password, dbname, schemaname),
        echo=False,
        connect_args=connect_args,
    )


def get_connection(username=None, password=None, dbname=None, schemaname=None):
    loc_eng = get_engine(username, password, dbname, schemaname)
    return loc_eng.connect()


def get_raw_connection(username=None, password=None, dbname=None, schemaname=None):
    """
    Returns a raw Snowflake Python Connector API Connection object.
    :param username: Nuvolos user name.
    :param password: Nuvolos password.
    :param dbname: Nuvolos database name from the Connection Guide.
    :param schemaname: Nuvolos schema name from the Connection Guide.
    :return: A snowflake.connector.Connection object
    """
    (
        username,
        password,
        snowflake_host,
        db_name,
        schema_name,
    ) = _get_connection_params(
        username=username, password=password, dbname=dbname, schemaname=schemaname
    )

    connect_args = {
        "user": username,
        "account": snowflake_host,
        "database": db_name,
        "schema": schema_name,
        "session_parameters": {
            "QUERY_TAG": f"nuvolos {__version__}",
        },
    }

    if os.getenv("SNOWFLAKE_RSA_KEY"):
        connect_args["private_key_file"] = os.getenv("SNOWFLAKE_RSA_KEY")
        logger.debug(
            f"Using RSA key authentication with key file: {os.getenv('SNOWFLAKE_RSA_KEY')}"
        )
        if os.getenv("SNOWFLAKE_RSA_KEY_PASSPHRASE"):
            connect_args["private_key_file_pwd"] = os.getenv(
                "SNOWFLAKE_RSA_KEY_PASSPHRASE"
            )
    else:
        connect_args["password"] = password

    return snowflake.connector.connect(**connect_args)
