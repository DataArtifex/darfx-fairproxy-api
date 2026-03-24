from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from fairproxy_api.dependencies import get_server_repository
from fairproxy_api.models import Platform, ServerInfo
from fairproxy_api.repositories.server import ServerRepository

router = APIRouter(prefix="/servers", tags=["Servers"])


@router.get("/")
def search_servers(
    repository: Annotated[ServerRepository, Depends(get_server_repository)],
    platform: Platform | None = Query(None, description="Filter servers by platform type"),
) -> list[ServerInfo]:
    """Retrieve backend servers."""
    servers = repository.get_all(platform=platform)
    return sorted(servers, key=lambda server: server.name.lower())


@router.get("/{server_id}")
def get_server(server_id: str, repository: Annotated[ServerRepository, Depends(get_server_repository)]) -> ServerInfo:
    """Retrieve a specific backend server via its ID."""
    server = repository.get_by_id(server_id)
    if not server:
        raise HTTPException(status_code=404, detail=f"Server {server_id} not found.")
    return server
