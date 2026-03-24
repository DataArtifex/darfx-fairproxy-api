from typing import Any

from fairproxy_api.adapters.base import DatasetProvider
from fastapi import HTTPException
from rdflib import Graph


class MtnaAdapter(DatasetProvider):
    """
    Adapter implementing the DatasetProvider interface for MTNA datasets.
    This functionality is marked as experimental and returns 501 Not Implemented
    as requested for the scaffolding phase.
    """

    def __init__(self, host: str, dataset_id: str):
        self.host = host
        self.dataset_id = dataset_id

    async def get_croissant(self) -> dict[str, Any]:
        raise HTTPException(status_code=501, detail="MTNA Croissant generation is experimental and currently disabled.")

    async def get_dcat_graph(self) -> Graph:
        raise HTTPException(status_code=501, detail="MTNA DCAT generation is experimental and currently disabled.")

    async def get_ddi_cdif_graph(self, use_skos: bool = True) -> Graph:
        del use_skos
        raise HTTPException(status_code=501, detail="MTNA DDI-CDIF generation is experimental and currently disabled.")

    async def get_ddi_codebook_xml(self, pretty: bool = False) -> str:
        del pretty
        raise HTTPException(
            status_code=501, detail="MTNA DDI Codebook generation is experimental and currently disabled."
        )

    async def get_markdown(self) -> str:
        raise HTTPException(status_code=501, detail="MTNA Markdown generation is experimental and currently disabled.")

    async def get_postman_collection(self) -> dict[str, Any]:
        raise HTTPException(
            status_code=501, detail="MTNA Postman Collection generation is experimental and currently disabled."
        )

    async def get_native_data(self) -> dict[str, Any]:
        raise HTTPException(status_code=501, detail="MTNA native data is experimental and currently disabled.")
