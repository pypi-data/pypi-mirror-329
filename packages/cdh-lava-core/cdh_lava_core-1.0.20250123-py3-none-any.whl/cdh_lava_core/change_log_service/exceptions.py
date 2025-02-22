# cdh_lava_core/change_log_service/exceptions.py

class ChangeLogError(Exception):
    """Base class for exceptions in this module."""
    pass

class CalledProcessError(ChangeLogError):
    """Exception raised for errors in the subprocess call."""
    pass

class FileNotFoundError(ChangeLogError):
    """Exception raised for missing command errors."""
    pass

class UnexpectedError(ChangeLogError):
    """Exception raised for unexpected errors."""
    pass
