# Standard library imports
import hashlib
import uuid
import psutil

# 3rd party library imports
import pandas as pd

# Local imports


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
