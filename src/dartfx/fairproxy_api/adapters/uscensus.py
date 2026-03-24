from fairproxy_api.adapters.base import DatasetProvider
from fastapi import HTTPException
from rdflib import Graph


class UsCensusAdapter(DatasetProvider):
    """
    Adapter implementing the DatasetProvider interface for U.S. Census datasets.
    This functionality is marked as experimental and returns 501 Not Implemented
    as requested for the scaffolding phase.
    """

    def __init__(self, host: str, dataset_id: str):
        self.host = host
        self.dataset_id = dataset_id

    async def get_croissant(self) -> dict:
        raise HTTPException(
            status_code=501, detail="U.S. Census Croissant generation is experimental and currently disabled."
        )

    async def get_dcat_graph(self) -> Graph:
        raise HTTPException(
            status_code=501, detail="U.S. Census DCAT generation is experimental and currently disabled."
        )

    async def get_ddi_cdif_graph(self, use_skos: bool = True) -> Graph:
        raise HTTPException(
            status_code=501, detail="U.S. Census DDI-CDIF generation is experimental and currently disabled."
        )

    async def get_ddi_codebook_xml(self, pretty: bool = False) -> str:
        raise HTTPException(
            status_code=501, detail="U.S. Census DDI Codebook generation is experimental and currently disabled."
        )

    async def get_markdown(self) -> str:
        raise HTTPException(
            status_code=501, detail="U.S. Census Markdown generation is experimental and currently disabled."
        )

    async def get_postman_collection(self) -> dict:
        raise HTTPException(
            status_code=501, detail="U.S. Census Postman Collection generation is experimental and currently disabled."
        )

    async def get_native_data(self) -> dict:
        raise HTTPException(status_code=501, detail="U.S. Census native data is experimental and currently disabled.")

    async def get_geography(self) -> dict:
        raise HTTPException(
            status_code=501, detail="U.S. Census geography data is experimental and currently disabled."
        )

    async def get_variables(self) -> dict:
        raise HTTPException(
            status_code=501, detail="U.S. Census variables data is experimental and currently disabled."
        )
