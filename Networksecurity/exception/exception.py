# sys module provides access to system-specific functions
# We need it to get error details such as line number and filename
import sys

# Importing logger so that we can write logs
from Networksecurity.logging import logger


# Creating our own custom exception class
# Exception is the parent class of all Python errors

class NetworkSecurityException(Exception):

    # Constructor
    # Runs automatically whenever an object of this class is created
    def __init__(self, error_message, error_details: sys):

        # Store the original error message
        self.error_message = error_message

        # exc_info() returns information about the current exception
        #
        # Returns 3 things:
        # 1. exception type
        # 2. exception object
        # 3. traceback object
        #
        # Example:
        # (<class 'ZeroDivisionError'>,
        #  ZeroDivisionError('division by zero'),
        #  traceback object)
        _, _, exc_tb = error_details.exc_info()


        # tb_lineno gives the line number
        # where the exception occurred
        self.lineno = exc_tb.tb_lineno

        # tb_frame gives access to the stack frame
        # f_code gives code object
        # co_filename gives file name
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    # This method runs automatically whenever
    # we print the exception object
    def __str__(self):

        return (
            "Error occurred in python script name [{0}] "
            "line number [{1}] "
            "error message [{2}]"
        ).format(
            self.file_name,
            self.lineno,
            str(self.error_message)
        )


# Main block
# This code runs only when exception.py is executed directly
if __name__ == "__main__":

    try:

        # Logging a message
        logger.logging.info("Enter the try block")
        # logging is a variable in the logger.py

        # Intentional error
        # Division by zero is not allowed
        a = 1 / 0

        # This line will never execute
        print("This will not be printed", a)

    except Exception as e:

        # Catch the original error

        # Create our custom exception object
        # and raise it
        raise NetworkSecurityException(e, sys)

# we are trying to run the code inside the exception.py so logs folder will be created inside the exception folder