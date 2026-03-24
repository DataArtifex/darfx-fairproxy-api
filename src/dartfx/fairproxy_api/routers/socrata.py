import httpx
from fastapi import APIRouter, HTTPException, Request, Response

from fairproxy_api.adapters.socrata import SocrataAdapter
from fairproxy_api.dependencies import get_socrata_server
from fairproxy_api.utils import get_rdf_format

router = APIRouter(prefix="/socrata", tags=["Socrata Native"])


def get_socrata_adapter(host: str, dataset_id: str) -> SocrataAdapter:
    server = get_socrata_server(host)
    return SocrataAdapter(server, dataset_id)


@router.get("/{host}/{dataset_id}/dcat")
async def get_dcat(host: str, dataset_id: str, request: Request) -> Response:
    """W3C DCAT metadata for this dataset."""
    adapter = get_socrata_adapter(host, dataset_id)
    graph = await adapter.get_dcat_graph()
    format, mimetype = get_rdf_format(request)

    response_data = graph.serialize(format=format, indent=4)
    return Response(content=response_data, media_type=mimetype)


@router.get("/{host}/{dataset_id}/ddi/cdif")
async def get_ddi_cdif(host: str, dataset_id: str, request: Request, use_skos: bool = True) -> Response:
    """DDI-CDI metadata for this dataset based on the CDIF Profile."""
    adapter = get_socrata_adapter(host, dataset_id)
    graph = await adapter.get_ddi_cdif_graph(use_skos=use_skos)
    format, mimetype = get_rdf_format(request)

    response_data = graph.serialize(format=format, indent=4)
    return Response(content=response_data, media_type=mimetype)


@router.get("/{host}/{dataset_id}/ddi/codebook")
async def get_ddi_codebook(host: str, dataset_id: str, pretty: bool = False) -> Response:
    """DDI Codebook metadata for this dataset."""
    adapter = get_socrata_adapter(host, dataset_id)
    xml_content = await adapter.get_ddi_codebook_xml(pretty=pretty)
    return Response(content=xml_content, media_type="application/xml")


@router.get("/{host}/{dataset_id}/syntax/{environment}")
async def get_syntax(host: str, dataset_id: str, environment: str) -> Response:
    """Code snippets to use this dataset in the specified environment's syntax."""
    adapter = get_socrata_adapter(host, dataset_id)
    code = await adapter.get_code_snippet(environment)
    return Response(content=code, media_type="text/plain")


@router.get("/{host}/{path:path}")
async def view_proxy(host: str, path: str, request: Request) -> Response:
    """
    Proxies a direct request back to the Socrata API backend.
    """
    url = f"https://{host}/api/views/{path}"

    # Filter out Host header to prevent mismatches upstream
    headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
    params = dict(request.query_params)

    async with httpx.AsyncClient() as client:
        try:
            # Fastapi request.stream() would be ideal for streaming bodies here, but a direct proxy works for simple getters
            proxy_res = await client.request(
                method=request.method, url=url, headers=headers, params=params, timeout=10.0
            )
            proxy_res.raise_for_status()
        except httpx.HTTPStatusError as e:
            status = e.response.status_code if e.response else 502
            raise HTTPException(
                status_code=status if status >= 500 else 502, detail=f"Socrata proxy API exception: {str(e)}"
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Failed connecting to Socrata host proxy {host}: {str(e)}")

    # Forward the content, passing back upstream headers directly (omitting chunking identifiers)
    excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection"]
    res_headers = {k: v for k, v in proxy_res.headers.items() if k.lower() not in excluded_headers}

    return Response(content=proxy_res.content, status_code=proxy_res.status_code, headers=res_headers)
