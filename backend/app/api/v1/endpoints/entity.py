"""
Entity endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.entity import Entity
from app.models.finding import Finding
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/{entity_id}")
async def get_entity(
    entity_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get entity details, findings, and embeddings"""
    try:
        # Query entity from database
        result = await db.execute(
            select(Entity).where(Entity.id == entity_id)
        )
        entity = result.scalar_one_or_none()
        
        if not entity:
            raise HTTPException(status_code=404, detail="Entity not found")
        
        # Query findings for this entity
        findings_result = await db.execute(
            select(Finding).where(Finding.entity_id == entity_id)
        )
        findings = findings_result.scalars().all()
        
        return {
            "id": entity.id,
            "scan_id": entity.scan_id,
            "type": entity.type.value,
            "canonical_value": entity.canonical_value,
            "metadata": entity.metadata_json,
            "first_seen": entity.first_seen,
            "last_seen": entity.last_seen,
            "findings": [
                {
                    "id": f.id,
                    "source": f.source,
                    "type": f.type,
                    "confidence_score": f.confidence_score,
                    "raw_result": f.raw_result,
                    "created_at": f.created_at,
                }
                for f in findings
            ],
            "findings_count": len(findings),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving entity {entity_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve entity: {str(e)}"
        )


@router.get("/{entity_id}/findings")
async def get_entity_findings(
    entity_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all findings for an entity"""
    try:
        # Verify entity exists
        entity_result = await db.execute(
            select(Entity).where(Entity.id == entity_id)
        )
        entity = entity_result.scalar_one_or_none()
        
        if not entity:
            raise HTTPException(status_code=404, detail="Entity not found")
        
        # Query findings
        findings_result = await db.execute(
            select(Finding).where(Finding.entity_id == entity_id)
        )
        findings = findings_result.scalars().all()
        
        return {
            "entity_id": entity_id,
            "findings": [
                {
                    "id": f.id,
                    "source": f.source,
                    "type": f.type,
                    "confidence_score": f.confidence_score,
                    "raw_result": f.raw_result,
                    "created_at": f.created_at,
                }
                for f in findings
            ],
            "total": len(findings),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving findings for entity {entity_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve findings: {str(e)}"
        )












