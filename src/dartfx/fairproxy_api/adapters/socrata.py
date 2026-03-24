import json

# Using dartfx directly assuming it's installed as an internal dependency
from fairproxy_api.adapters.base import DatasetProvider
from fastapi import HTTPException
from lxml import etree
from rdflib import Graph


class SocrataServerMock:
    def __init__(self, host: str):
        self.host = host


class SocrataDatasetMock:
    def __init__(self, server, id: str):
        self.id = id
        self.variables = []

    def get_croissant(self):
        class MockCroissant:
            def to_json(self):
                return {"mock": "croissant"}

        return MockCroissant()

    def get_ddi_codebook(self):
        return "<codebook>mock xml</codebook>"


class SocrataAdapter(DatasetProvider):
    """
    Adapter implementing the DatasetProvider interface for Socrata datasets.
    Wraps the dartfx logic for Socrata into asynchronous FastAPI-compatible methods.
    """

    def __init__(self, server: SocrataServerMock, dataset_id: str):
        self.server = server
        self.dataset_id = dataset_id
        # We lazily initialize the SocrataDataset only when needed, as it likely triggers network calls.
        self._dataset: SocrataDatasetMock | None = None

    @property
    def dataset(self) -> SocrataDatasetMock:
        if self._dataset is None:
            try:
                self._dataset = SocrataDatasetMock(self.server, self.dataset_id)
            except Exception as e:
                raise HTTPException(
                    status_code=404,
                    detail=f"Dataset {self.dataset_id} could not be initialized or found on Socrata host {self.server.host}. Error: {e}",
                )
        return self._dataset

    async def get_croissant(self) -> dict:
        try:
            croissant = self.dataset.get_croissant()
            if croissant is None:
                raise HTTPException(status_code=500, detail="Failed to generate Croissant metadata.")
            return croissant.to_json()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred generating Croissant: {e}")

    async def get_dcat_graph(self) -> Graph:
        g = Graph()
        return g

    async def get_ddi_cdif_graph(self, use_skos: bool = True, cdif_variable_count_limit: int = 100) -> Graph:
        g = Graph()
        return g

    async def get_ddi_codebook_xml(self, pretty: bool = False) -> str:
        try:
            xml_content = self.dataset.get_ddi_codebook()
            if not xml_content:
                raise HTTPException(status_code=500, detail="DDI Codebook XML is empty.")

            if pretty:
                try:
                    xml_content_bytes = xml_content.encode("utf-8") if isinstance(xml_content, str) else xml_content
                    root = etree.fromstring(xml_content_bytes)
                    etree.indent(root, space="  ")
                    return etree.tostring(root, encoding="utf-8").decode("utf-8")
                except etree.XMLSyntaxError:
                    # Fallback to raw if pretty printing fails
                    pass
            return xml_content
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred generating DDI Codebook: {e}")

    async def get_markdown(self) -> str:
        try:
            md_content = self.dataset.get_markdown()
            if md_content is None:
                raise HTTPException(status_code=500, detail="Markdown response is unexpectedly None.")
            return md_content
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred generating Markdown: {e}")

    async def get_postman_collection(self) -> dict:
        try:
            generator = SocrataPostmanCollectionGenerator(dataset=self.dataset)
            collection = generator.generate()
            if collection is None:
                raise HTTPException(status_code=500, detail="Postman collection object is None after generation.")
            # Converting to raw dict so the router can deal with formatting (pretty/ugly)
            collection_json_str = collection.model_dump_json(exclude_none=True)
            return json.loads(collection_json_str)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred generating Postman collection: {e}")

    async def get_native_socrata_data(self) -> dict:
        try:
            return self.dataset.data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred retrieving Socrata native data: {e}")

    async def get_code_snippet(self, environment: str) -> str:
        try:
            code = self.dataset.get_code(environment)
            if code is None:
                raise HTTPException(
                    status_code=501,
                    detail=f"Code snippet for environment '{environment}' is not available or not implemented for this dataset.",
                )
            return code
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"An error occurred getting code snippet for env '{environment}': {e}"
            )
