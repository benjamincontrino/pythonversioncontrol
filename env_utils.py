"""
env_utils.py
============
Core utility functions for loading and auditing environment variables
from a .env file. This is the standard Python pattern for keeping
credentials out of source code and version control.

Usage
-----
    from dotenv import load_dotenv
    from pythonversioncontrol import get_env_var, list_env_connections

    load_dotenv(".env")               # load once at the top of your script
    server = get_env_var("DB_SERVER") # access anywhere after that
"""

import os
import warnings
from typing import Optional
from dotenv import load_dotenv


def get_env_var(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Retrieve an environment variable safely after loading a .env file.

    This is the core pattern used for all cloud database connectivity —
    credentials are never hardcoded in scripts; they live in ``.env``
    and are accessed at runtime via ``os.environ``.

    Parameters
    ----------
    key : str
        The name of the environment variable to retrieve.
        Examples: ``"DB_PASSWORD"``, ``"DATABRICKS_TOKEN"``.
    default : str, optional
        Value returned if the variable is not set. If ``None`` (the default),
        a warning is issued and ``None`` is returned when the key is missing.

    Returns
    -------
    str or None
        The value of the environment variable, or ``default`` / ``None``
        if not found.

    Notes
    -----
    Always call ``load_dotenv(".env")`` at the top of your script before
    using this function. Environment variables are loaded into ``os.environ``
    by python-dotenv and persist for the life of the process.

    Environment Variable Categories
    --------------------------------
    +------------------+----------------------------+
    | Prefix           | Platform                   |
    +==================+============================+
    | ``DB_``          | SQL Server                 |
    +------------------+----------------------------+
    | ``AZURE_``       | Azure Blob Storage         |
    +------------------+----------------------------+
    | ``FABRIC_``      | Microsoft Fabric           |
    +------------------+----------------------------+
    | ``DATABRICKS_``  | Azure Databricks           |
    +------------------+----------------------------+
    | ``SNOWFLAKE_``   | Snowflake Data Cloud       |
    +------------------+----------------------------+

    Examples
    --------
    >>> from dotenv import load_dotenv
    >>> from pythonversioncontrol import get_env_var
    >>> load_dotenv(".env")
    True
    >>> server = get_env_var("DB_SERVER")
    >>> port = get_env_var("DB_PORT", default="1433")
    """
    val = os.environ.get(key)

    if not val:
        if default is None:
            warnings.warn(
                f"Environment variable '{key}' is not set. "
                "Did you call load_dotenv('.env') at the top of your script?",
                UserWarning,
                stacklevel=2,
            )
            return None
        return default

    return val


def list_env_connections() -> list[dict]:
    """
    Audit all configured cloud connection variables from the environment.

    Scans ``os.environ`` for known cloud platform variables and returns
    a list of dicts showing which are set. Values are masked for security —
    only the variable names and their set/unset status are shown.

    Returns
    -------
    list of dict
        Each dict has the keys:
        - ``platform`` (str): the cloud platform name
        - ``variable`` (str): the environment variable name
        - ``is_set`` (bool): whether the variable has a non-empty value

    Examples
    --------
    >>> from dotenv import load_dotenv
    >>> from pythonversioncontrol import list_env_connections
    >>> load_dotenv(".env")
    True
    >>> results = list_env_connections()
    >>> for row in results:
    ...     print(row["platform"], row["variable"], row["is_set"])
    """
    platform_map = {
        # SQL Server
        "DB_DRIVER":   "SQL Server",
        "DB_SERVER":   "SQL Server",
        "DB_NAME":     "SQL Server",
        "DB_USER":     "SQL Server",
        "DB_PASSWORD": "SQL Server",
        "DB_PORT":     "SQL Server",
        # Azure Blob Storage
        "AZURE_STORAGE_ACCOUNT": "Azure Blob Storage",
        "AZURE_STORAGE_KEY":     "Azure Blob Storage",
        "AZURE_CONTAINER":       "Azure Blob Storage",
        # Microsoft Fabric
        "FABRIC_DB_DRIVER": "Microsoft Fabric",
        "FABRIC_DB_SERVER": "Microsoft Fabric",
        "FABRIC_DB_NAME":   "Microsoft Fabric",
        # Databricks
        "DATABRICKS_HOST":      "Databricks",
        "DATABRICKS_TOKEN":     "Databricks",
        "DATABRICKS_HTTP_PATH": "Databricks",
        "DATABRICKS_CATALOG":   "Databricks",
        "DATABRICKS_SCHEMA":    "Databricks",
        # Snowflake
        "SNOWFLAKE_ACCOUNT":   "Snowflake",
        "SNOWFLAKE_USER":      "Snowflake",
        "SNOWFLAKE_PASSWORD":  "Snowflake",
        "SNOWFLAKE_WAREHOUSE": "Snowflake",
        "SNOWFLAKE_DATABASE":  "Snowflake",
        "SNOWFLAKE_SCHEMA":    "Snowflake",
        "SNOWFLAKE_ROLE":      "Snowflake",
    }

    return [
        {
            "platform": platform,
            "variable": var,
            "is_set":   bool(os.environ.get(var)),
        }
        for var, platform in platform_map.items()
    ]
