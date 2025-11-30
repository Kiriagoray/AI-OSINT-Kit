"""
Scan endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.models.scan import Scan, ScanStatus, ScanType
from app.models.entity import Entity
from app.models.finding import Finding
from app.tasks.scan import scan_domain_task, scan_email_task
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class ScanRequest(BaseModel):
    """Scan request model"""
    target: str
    type: str  # domain, email, ip, handle
    modules: Optional[List[str]] = None


class ScanResponse(BaseModel):
    """Scan response model"""
    scan_id: int
    status: str
    target: str
    type: str
    created_at: datetime


@router.post("", response_model=ScanResponse)
async def create_scan(
    request: ScanRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Start a new OSINT scan
    
    - **target**: Domain, email, IP, or social handle to scan
    - **type**: Type of target (domain, email, ip, handle)
    - **modules**: List of OSINT modules to run (optional)
    """
    try:
        # Validate scan type
        try:
            scan_type = ScanType(request.type.lower())
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid scan type: {request.type}. Must be one of: domain, email, ip, handle"
            )
        
        # Create scan record in database
        scan = Scan(
            target=request.target,
            type=scan_type,
            status=ScanStatus.QUEUED,
            settings={"modules": request.modules or []},
        )
        
        db.add(scan)
        await db.commit()
        await db.refresh(scan)
        
        # Queue Celery task based on scan type
        modules = request.modules or []
        
        if scan_type == ScanType.DOMAIN:
            scan_domain_task.delay(scan.id, request.target, modules)
            logger.info(f"Queued domain scan task for scan_id={scan.id}, target={request.target}")
        elif scan_type == ScanType.EMAIL:
            scan_email_task.delay(scan.id, request.target, modules)
            logger.info(f"Queued email scan task for scan_id={scan.id}, target={request.target}")
        else:
            # For IP and HANDLE types, use domain task for now
            # TODO: Implement dedicated tasks for IP and handle scans
            scan_domain_task.delay(scan.id, request.target, modules)
            logger.info(f"Queued scan task for scan_id={scan.id}, target={request.target}, type={scan_type}")
        
        return ScanResponse(
            scan_id=scan.id,
            status=scan.status.value,
            target=scan.target,
            type=scan.type.value,
            created_at=scan.created_at,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating scan: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create scan: {str(e)}"
        )


@router.get("")
async def get_scans(
    db: AsyncSession = Depends(get_db),
    limit: int = 100
):
    """Get all scans"""
    try:
        result = await db.execute(
            select(Scan).order_by(Scan.created_at.desc()).limit(limit)
        )
        scans = result.scalars().all()
        
        return [
            {
                "scan_id": scan.id,
                "target": scan.target,
                "type": scan.type.value,
                "status": scan.status.value,
                "settings": scan.settings,
                "created_at": scan.created_at,
                "started_at": scan.started_at,
                "finished_at": scan.finished_at,
            }
            for scan in scans
        ]
    except Exception as e:
        logger.error(f"Error retrieving scans: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve scans: {str(e)}"
        )


@router.get("/{scan_id}")
async def get_scan(
    scan_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get scan status and summary with entities and findings"""
    try:
        # Query scan from database
        result = await db.execute(
            select(Scan).where(Scan.id == scan_id)
        )
        scan = result.scalar_one_or_none()
        
        if not scan:
            raise HTTPException(status_code=404, detail="Scan not found")
        
        # Query entities for this scan
        entities_result = await db.execute(
            select(Entity).where(Entity.scan_id == scan_id)
        )
        entities = entities_result.scalars().all()
        
        # Query findings for entities in this scan
        entity_ids = [e.id for e in entities]
        findings = []
        if entity_ids:
            findings_result = await db.execute(
                select(Finding).where(Finding.entity_id.in_(entity_ids))
            )
            findings = findings_result.scalars().all()
        
        return {
            "scan_id": scan.id,
            "target": scan.target,
            "type": scan.type.value,
            "status": scan.status.value,
            "settings": scan.settings,
            "created_at": scan.created_at,
            "started_at": scan.started_at,
            "finished_at": scan.finished_at,
            "entities": [
                {
                    "id": e.id,
                    "scan_id": e.scan_id,
                    "type": e.type.value,
                    "canonical_value": e.canonical_value,
                    "metadata": e.metadata_json,
                    "first_seen": e.first_seen,
                    "last_seen": e.last_seen,
                }
                for e in entities
            ],
            "findings": [
                {
                    "id": f.id,
                    "entity_id": f.entity_id,
                    "source": f.source,
                    "type": f.type,
                    "confidence_score": f.confidence_score,
                    "raw_result": f.raw_result,
                    "created_at": f.created_at,
                }
                for f in findings
            ],
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving scan {scan_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve scan: {str(e)}"
        )


@router.websocket("/{scan_id}/ws")
async def scan_websocket(scan_id: str):
    """WebSocket endpoint for real-time scan updates"""
    # TODO: Implement WebSocket for live scan progress
    pass


