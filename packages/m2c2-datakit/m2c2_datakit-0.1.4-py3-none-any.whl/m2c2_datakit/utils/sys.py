# Standard library imports
import psutil


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
