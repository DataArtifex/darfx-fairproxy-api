from fastapi import APIRouter

from fairproxy_api.routers import catalog, datasets, resources, servers, socrata, vocab


def get_router() -> APIRouter:
    router = APIRouter()
    router.include_router(datasets.router)
    router.include_router(socrata.router)
    router.include_router(servers.router)
    router.include_router(catalog.router)
    router.include_router(resources.router)
    router.include_router(vocab.router)
    return router
