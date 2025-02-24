import logging
import sys

# Configure the root logger for verbose output
logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG for detailed logs
    format=(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d "
        "| %(funcName)s | %(message)s"
    ),
    datefmt="%Y-%m-%d %H:%M:%S",  # Add a cleaner timestamp format
    handlers=[
        logging.StreamHandler(sys.stdout),  # Log to stdout
        # Uncomment the next line to enable logging to a file
        # logging.FileHandler("verbose_output.log"),
    ],
)


# Create a function to get a logger for each module
def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger with the given name.

    Parameters:
        name (str): The name of the logger (usually __name__).

    Returns:
        logging.Logger: Configured logger instance.
    """
    return logging.getLogger(name)
