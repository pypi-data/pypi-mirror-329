class SAISError(Exception):
    """Base exception for SAIS SDK"""


class ConfigurationError(SAISError):
    """Configuration related errors"""


class DataAccessError(SAISError):
    """Data access client errors"""


class MLFlowIntegrationError(SAISError):
    """MLFlow integration errors"""
