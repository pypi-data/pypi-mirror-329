import datetime


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
