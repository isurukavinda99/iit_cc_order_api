from fastapi import APIRouter
router = APIRouter()


@router.get("/health", tags=["monitoring"])
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "services": {
            "database": "available",
            "cache": "available"
        }
    }