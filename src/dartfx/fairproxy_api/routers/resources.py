from fastapi import APIRouter

router = APIRouter(prefix="/resources", tags=["Resources"])


@router.get("/")
def get_resources() -> dict[str, str]:
    """Placeholder endpoint for Resources."""
    return {"message": "Development endpoint for `/resources/` placeholder."}
