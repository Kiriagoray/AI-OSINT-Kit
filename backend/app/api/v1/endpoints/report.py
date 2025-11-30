"""
Report endpoints
"""
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/{report_id}")
async def get_report(report_id: str):
    """Get generated LLM report"""
    # TODO: Implement report retrieval from database
    raise HTTPException(status_code=404, detail="Report not found")


@router.post("/{scan_id}/generate")
async def generate_report(scan_id: str):
    """Force generate a report from scan data using LLM"""
    # TODO: Implement LLM report generation
    return {
        "report_id": "temp-id",
        "scan_id": scan_id,
        "status": "generating",
        "message": "Report generation not yet implemented",
    }












