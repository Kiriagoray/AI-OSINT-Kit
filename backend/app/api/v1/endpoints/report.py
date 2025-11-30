"""
Report endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.report import Report
from app.models.scan import Scan
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/{report_id}")
async def get_report(
    report_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get generated LLM report"""
    try:
        result = await db.execute(
            select(Report).where(Report.id == report_id)
        )
        report = result.scalar_one_or_none()
        
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        return {
            "id": report.id,
            "scan_id": report.scan_id,
            "title": report.title,
            "generated_text": report.generated_text,
            "sections": report.sections,
            "score": report.score,
            "created_at": report.created_at,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving report {report_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve report: {str(e)}"
        )


@router.get("/scan/{scan_id}")
async def get_scan_reports(
    scan_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all reports for a scan"""
    try:
        # Verify scan exists
        scan_result = await db.execute(
            select(Scan).where(Scan.id == scan_id)
        )
        scan = scan_result.scalar_one_or_none()
        
        if not scan:
            raise HTTPException(status_code=404, detail="Scan not found")
        
        # Get reports
        reports_result = await db.execute(
            select(Report).where(Report.scan_id == scan_id).order_by(Report.created_at.desc())
        )
        reports = reports_result.scalars().all()
        
        return [
            {
                "id": r.id,
                "scan_id": r.scan_id,
                "title": r.title,
                "generated_text": r.generated_text,
                "sections": r.sections,
                "score": r.score,
                "created_at": r.created_at,
            }
            for r in reports
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving reports for scan {scan_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve reports: {str(e)}"
        )


@router.post("/{scan_id}/generate")
async def generate_report(scan_id: str):
    """Force generate a report from scan data using LLM"""
    # TODO: Implement LLM report generation
    return {
        "report_id": "temp-id",
        "scan_id": scan_id,
        "status": "generating",
        "message": "Report generation not yet implemented. LLM integration pending.",
    }












