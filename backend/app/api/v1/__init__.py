"""
API v1 router
"""
from fastapi import APIRouter
from app.api.v1.endpoints import scan, entity, search, report, health

router = APIRouter()

# Include endpoint routers
router.include_router(health.router, tags=["health"])
router.include_router(scan.router, prefix="/scan", tags=["scans"])
router.include_router(entity.router, prefix="/entity", tags=["entities"])
router.include_router(search.router, prefix="/search", tags=["search"])
router.include_router(report.router, prefix="/report", tags=["reports"])












