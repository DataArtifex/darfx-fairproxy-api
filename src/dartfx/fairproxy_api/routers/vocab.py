from fastapi import APIRouter

router = APIRouter(prefix="/vocab", tags=["Vocabularies"])


@router.get("/")
def get_vocab():
    """Placeholder endpoint for Vocabularies."""
    return {"message": "Development endpoint for `/vocab/` placeholder."}
