class DBBaseError(Exception):
    """Base class for all database-level operation errors."""

    status_code = 500


class ServiceBaseError(Exception):
    """Base class for all service-level operation errors."""

    status_code = 500
