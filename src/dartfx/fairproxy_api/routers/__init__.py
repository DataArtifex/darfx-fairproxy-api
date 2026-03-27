from fastapi import APIRouter

from fairproxy_api.routers import datasets, servers, socrata


def get_router() -> APIRouter:
    router = APIRouter()
    router.include_router(datasets.router)
    router.include_router(socrata.router)
    router.include_router(servers.router)
    return router
