"""
Entity endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import Optional

router = APIRouter()


@router.get("/{entity_id}")
async def get_entity(entity_id: str):
    """Get entity details, findings, and embeddings"""
    # TODO: Implement entity retrieval from database
    raise HTTPException(status_code=404, detail="Entity not found")


@router.get("/{entity_id}/findings")
async def get_entity_findings(entity_id: str):
    """Get all findings for an entity"""
    # TODO: Implement findings retrieval
    return {"entity_id": entity_id, "findings": []}












