"""
Search endpoints
"""
from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter()


@router.get("")
async def search(
    q: str = Query(..., description="Search query"),
    limit: Optional[int] = Query(10, ge=1, le=100),
    offset: Optional[int] = Query(0, ge=0),
):
    """Search entities and scans"""
    # TODO: Implement search functionality with database and embeddings
    return {
        "query": q,
        "results": [],
        "total": 0,
        "limit": limit,
        "offset": offset,
    }












