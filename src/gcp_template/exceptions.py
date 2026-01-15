class GCPTemplateError(Exception):
    """Base exception for all errors in the GCP template library."""
    pass

class GCPSecretError(GCPTemplateError):
    """Raised when there is an issue interacting with Secret Manager."""
    pass

class GCPResourceNotFoundError(GCPSecretError):
    """Raised when a specific secret or version is not found."""
    pass

class GCPConfigurationError(GCPTemplateError):
    """Raised when environment variables or project IDs are missing."""
    pass