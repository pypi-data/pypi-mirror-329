import datetime

# Standard library imports
import psutil

# Standard library imports
import hashlib
import uuid
import psutil

# 3rd party library imports
import pandas as pd

# Local imports


def get_sys_stats() -> dict:
    """
    Retrieve system statistics for the current process.

    Returns:
        dict: A dictionary containing memory usage (MB) and CPU percentage.
    """
    process = psutil.Process()
    memory = process.memory_info().rss / (1024**2)  # Memory usage in MB
    cpu = process.cpu_percent(interval=0.1)  # CPU usage percentage
    return {"memory_mb": memory, "cpu_percent": cpu}


def get_timestamp() -> datetime.datetime:
    """
    Returns the current timestamp as a datetime object.

    Returns:
        datetime.datetime: The current timestamp.
    """
    return datetime.datetime.now()


def get_filename_timestamp() -> str:
    """
    Returns a timestamp formatted for filenames.

    Returns:
        str: The timestamp as a string in 'YYYYMMDD_HHMMSS' format.
    """
    return get_timestamp().strftime("%Y%m%d_%H%M%S")


def get_uuid(version: int = 4) -> str:
    """
    Generate a UUID based on the specified version.

    Parameters:
        version (int): The version of the UUID to generate (1 or 4).
                      Defaults to version 4.

    Returns:
        str: A string representation of the generated UUID.
    """
    if version == 1:
        return str(uuid.uuid1())
    return str(uuid.uuid4())


def compute_md5_hash(df: pd.DataFrame) -> str:
    """
    Compute an MD5 hash of a Pandas DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame to hash.

    Returns:
        str: The MD5 hash as a hexadecimal string.
    """
    # Convert DataFrame to JSON string format for consistent hashing
    df_string = df.to_json()
    return hashlib.md5(df_string.encode()).hexdigest()
