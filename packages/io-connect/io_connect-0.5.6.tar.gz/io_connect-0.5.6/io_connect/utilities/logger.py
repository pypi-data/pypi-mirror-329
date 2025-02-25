import sys
from timeit import default_timer


class Timer:
    def __init__(self, message: str, log_time: bool = False):
        self.interval = 0
        self.message = message
        self.log_time = log_time

    def __enter__(self):
        self.start = default_timer()
        return self

    def __exit__(self, *args):
        self.end = default_timer()
        self.interval = self.end - self.start
        if self.log_time:
            print(f"[NETWORK] {self.message} {self.interval:.4f} seconds")


def display_log(log: str):
    """
    Display a log message on the console.

    This function writes a log message to the standard output stream (stdout),
    overwriting any existing content on the current line.

    Args:
        log (str): The log message to be displayed.

    Returns:
        None

     Example:
        >>> display_log("Processing...")  # Displays "Processing..." on the console

    """

    # Move the cursor to the beginning of the line
    sys.stdout.write("\r")

    # Clear the content from the cursor to the end of the line
    sys.stdout.write("\033[K")

    # Write the log message
    sys.stdout.write(log)

    # Flush the output buffer to ensure the message is displayed immediately
    sys.stdout.flush()
