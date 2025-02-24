"""
This script configures a logger for the module and returns an instance of logger.
"""

import logging
import os

def get_logger(module_name: str) -> logging.Logger:
    """
    Creates an instance of the logger for the module specified.
    Ensures proper formatting and prevents duplicate handlers.
    """
    # Create or get a logger instance
    log = logging.getLogger(module_name)
    
    if not log.handlers:  # Avoid duplicate handlers
        # Set log level
        log.setLevel(logging.DEBUG)  # Change to desired level (DEBUG, INFO, etc.)
        
        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)  # Set console log level
        
        # Set a formatter
        formatter = logging.Formatter(
            "%(asctime)s : %(name)s : %(levelname)s : %(message)s"
        )
        console_handler.setFormatter(formatter)
        
        # Add the handler to the logger
        log.addHandler(console_handler)

    # Prevent logs from propagating to the root logger
    log.propagate = False
    
    return log
