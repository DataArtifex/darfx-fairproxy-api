from abc import ABC, abstractmethod

from rdflib import Graph


class DatasetProvider(ABC):
    """
    Abstract base class enforcing a contract for heterogeneous datastores
    (Socrata, MTNA RDS, US Census) exposed via the FAIRification API.
    """

    @abstractmethod
    def __init__(self, host: str, dataset_id: str):
        pass

    @abstractmethod
    async def get_croissant(self) -> dict:
        """Return the MLCommons Croissant metadata as a dictionary."""
        pass

    @abstractmethod
    async def get_dcat_graph(self) -> Graph:
        """Return the W3C DCAT metadata as an rdflib Graph."""
        pass

    @abstractmethod
    async def get_ddi_cdif_graph(self, use_skos: bool = True) -> Graph:
        """Return the DDI-CDI metadata based on the CDIF Profile as an rdflib Graph."""
        pass

    @abstractmethod
    async def get_ddi_codebook_xml(self, pretty: bool = False) -> str:
        """Return the DDI Codebook metadata as raw XML."""
        pass

    @abstractmethod
    async def get_markdown(self) -> str:
        """Return a markdown-formatted description of this dataset."""
        pass

    @abstractmethod
    async def get_postman_collection(self) -> dict:
        """Return a generated data-centric Postman collection for this dataset."""
        pass
