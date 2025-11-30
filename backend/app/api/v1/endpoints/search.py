"""
Search endpoints
"""
from fastapi import APIRouter, Query, Depends, HTTPException
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.db.database import get_db
from app.models.entity import Entity
from app.models.scan import Scan
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("")
async def search(
    q: str = Query(..., description="Search query"),
    limit: Optional[int] = Query(10, ge=1, le=100),
    offset: Optional[int] = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """Search entities and scans"""
    try:
        search_term = f"%{q.lower()}%"
        
        # Search entities
        entities_result = await db.execute(
            select(Entity)
            .where(Entity.canonical_value.ilike(search_term))
            .limit(limit)
            .offset(offset)
        )
        entities = entities_result.scalars().all()
        
        # Search scans
        scans_result = await db.execute(
            select(Scan)
            .where(Scan.target.ilike(search_term))
            .limit(limit)
            .offset(offset)
        )
        scans = scans_result.scalars().all()
        
        # Combine results
        results = []
        
        # Add entities
        for entity in entities:
            results.append({
                "type": "entity",
                "id": entity.id,
                "value": entity.canonical_value,
                "entity_type": entity.type.value,
                "scan_id": entity.scan_id,
                "first_seen": entity.first_seen,
            })
        
        # Add scans
        for scan in scans:
            results.append({
                "type": "scan",
                "id": scan.id,
                "target": scan.target,
                "scan_type": scan.type.value,
                "status": scan.status.value,
                "created_at": scan.created_at,
            })
        
        return {
            "query": q,
            "results": results,
            "total": len(results),
            "limit": limit,
            "offset": offset,
        }
    except Exception as e:
        logger.error(f"Error searching: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )












