import json
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response

from fairproxy_api.adapters.base import DatasetProvider
from fairproxy_api.dependencies import get_platform_adapter
from fairproxy_api.utils import get_rdf_format

router = APIRouter(prefix="/datasets", tags=["Unified Datasets"])


@router.get("/{uri:path}/croissant")
async def get_croissant(
    request: Request, adapter: Annotated[DatasetProvider, Depends(get_platform_adapter)]
) -> Response:
    """MLCommons Croissant metadata for this dataset."""
    format, mimetype = get_rdf_format(request)

    if format not in ["json", "json-ld"]:
        raise HTTPException(
            status_code=501,
            detail=f"Serialization format '{format}' not supported for Croissant. Only JSON-LD is available.",
        )

    croissant_dict = await adapter.get_croissant()
    response_data = json.dumps(croissant_dict, default=str)

    return Response(content=response_data, media_type=mimetype)


@router.get("/{uri:path}/dcat")
async def get_dcat(request: Request, adapter: Annotated[DatasetProvider, Depends(get_platform_adapter)]) -> Response:
    """W3C DCAT metadata for this dataset."""
    graph = await adapter.get_dcat_graph()
    format, mimetype = get_rdf_format(request)

    response_data = graph.serialize(format=format, indent=4)
    return Response(content=response_data, media_type=mimetype)


@router.get("/{uri:path}/ddi/cdif")
async def get_ddi_cdif(
    request: Request, adapter: Annotated[DatasetProvider, Depends(get_platform_adapter)], use_skos: bool = True
) -> Response:
    """DDI-CDI metadata for this dataset based on the CDIF Profile."""
    graph = await adapter.get_ddi_cdif_graph(use_skos=use_skos)
    format, mimetype = get_rdf_format(request)

    response_data = graph.serialize(format=format, indent=4)
    return Response(content=response_data, media_type=mimetype)


@router.get("/{uri:path}/ddi/codebook")
async def get_ddi_codebook(
    adapter: Annotated[DatasetProvider, Depends(get_platform_adapter)], pretty: bool = False
) -> Response:
    """DDI Codebook metadata for this dataset."""
    xml_content = await adapter.get_ddi_codebook_xml(pretty=pretty)
    return Response(content=xml_content, media_type="application/xml")


@router.get("/{uri:path}/markdown")
async def get_markdown(adapter: Annotated[DatasetProvider, Depends(get_platform_adapter)]) -> Response:
    """Markdown-formatted description of this dataset."""
    md_content = await adapter.get_markdown()
    return Response(content=md_content, media_type="text/markdown")


@router.get("/{uri:path}/postman/collection")
async def get_postman_collection(
    adapter: Annotated[DatasetProvider, Depends(get_platform_adapter)], pretty: bool = False
) -> Response:
    """A generated data-centric Postman collection for this dataset."""
    collection_dict = await adapter.get_postman_collection()

    if pretty:
        response_data = json.dumps(collection_dict, indent=4)
    else:
        # Re-dump without indent to save space if not pretty
        response_data = json.dumps(collection_dict)

    return Response(content=response_data, media_type="application/json")
