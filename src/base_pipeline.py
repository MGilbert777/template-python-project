from abc import ABC, abstractmethod
from typing import Any
from .logger_factory import setup_logging
from .clients import GCPClientFactory

class GCPBasePipeline(ABC):
    """
    Abstract base class for modular GCP data pipelines.
    
    Attributes:
        logger: Configured loguru instance.
        clients: Factory for GCP service clients.
    """
    def __init__(self, service_name: str):
        self.logger = setup_logging("pipeline")
        self.clients = GCPClientFactory()
        self.service_name = service_name

    @abstractmethod
    def extract(self) -> Any:
        """Extract data from source (GCS, API, etc.)"""
        pass

    @abstractmethod
    def transform(self, data: Any) -> Any:
        """Apply business logic and cleaning."""
        pass

    @abstractmethod
    def load(self, data: Any) -> None:
        """Load data into destination (BigQuery, etc.)"""
        pass
