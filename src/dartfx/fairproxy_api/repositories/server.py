from abc import ABC, abstractmethod

from fairproxy_api.models import Platform, ServerInfo


class ServerRepository(ABC):
    """
    Abstract interface for retrieving backend servers containing datasets.
    Can be implemented via YAML (local), PostgreSQL logic, or RDF Triplestore logic.
    """

    @abstractmethod
    def get_all(self, platform: Platform | None = None) -> list[ServerInfo]:
        """Fetch all server instances. Optionally filtered by Platform enum."""
        pass

    @abstractmethod
    def get_by_id(self, server_id: str) -> ServerInfo | None:
        """Fetch a specific ServerInfo via its ID."""
        pass
