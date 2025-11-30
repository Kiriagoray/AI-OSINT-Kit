"""
Scan background tasks
"""
import asyncio
from datetime import datetime
from celery import Celery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.database import AsyncSessionLocal
from app.models.scan import Scan, ScanStatus
from app.models.entity import Entity, EntityType
from app.models.finding import Finding
from app.services.osint import run_whois, run_ssl
import logging

logger = logging.getLogger(__name__)

# Initialize Celery
celery_app = Celery(
    "osint_kit",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


async def _update_scan_status(
    db: AsyncSession,
    scan_id: int,
    status: ScanStatus,
    started_at: datetime = None,
    finished_at: datetime = None
):
    """Update scan status in database"""
    result = await db.execute(select(Scan).where(Scan.id == scan_id))
    scan = result.scalar_one_or_none()
    
    if scan:
        scan.status = status
        if started_at:
            scan.started_at = started_at
        if finished_at:
            scan.finished_at = finished_at
        await db.commit()
        await db.refresh(scan)
        return scan
    return None


async def _get_or_create_entity(
    db: AsyncSession,
    scan_id: int,
    entity_type: EntityType,
    canonical_value: str,
    metadata: dict = None
) -> Entity:
    """Get existing entity or create a new one"""
    # Check if entity already exists
    result = await db.execute(
        select(Entity).where(
            Entity.canonical_value == canonical_value,
            Entity.type == entity_type
        )
    )
    entity = result.scalar_one_or_none()
    
    if entity:
        # Update last_seen and metadata
        entity.last_seen = datetime.utcnow()
        if metadata:
            # Merge metadata
            if entity.metadata_json:
                entity.metadata_json.update(metadata)
            else:
                entity.metadata_json = metadata
        await db.commit()
        await db.refresh(entity)
        return entity
    else:
        # Create new entity
        entity = Entity(
            scan_id=scan_id,
            type=entity_type,
            canonical_value=canonical_value,
            metadata_json=metadata or {}
        )
        db.add(entity)
        await db.commit()
        await db.refresh(entity)
        return entity


async def _create_finding(
    db: AsyncSession,
    entity_id: int,
    source: str,
    finding_type: str,
    confidence_score: float = 0.0,
    raw_result: dict = None
):
    """Create a finding record"""
    finding = Finding(
        entity_id=entity_id,
        source=source,
        type=finding_type,
        confidence_score=confidence_score,
        raw_result=raw_result or {}
    )
    db.add(finding)
    await db.commit()
    await db.refresh(finding)
    return finding


async def _run_scan_async(scan_id: int, target: str, modules: list):
    """Async function to run OSINT scan"""
    async with AsyncSessionLocal() as db:
        try:
            # Update scan status to running
            started_at = datetime.utcnow()
            await _update_scan_status(db, scan_id, ScanStatus.RUNNING, started_at=started_at)
            logger.info(f"Starting scan {scan_id} for target {target}")
            
            # Default modules if none specified
            if not modules:
                modules = ["whois", "ssl"]
            
            # Run WHOIS module
            if "whois" in modules:
                try:
                    logger.info(f"Running WHOIS for {target}")
                    whois_result = await run_whois(target)
                    
                    if whois_result.get("success"):
                        whois_data = whois_result.get("data", {})
                        
                        # Create or update domain entity
                        domain_entity = await _get_or_create_entity(
                            db, scan_id, EntityType.DOMAIN, target, whois_data
                        )
                        
                        # Create finding for WHOIS data
                        await _create_finding(
                            db, domain_entity.id, "whois", "domain_info",
                            confidence_score=1.0, raw_result=whois_data
                        )
                        
                        # Extract name servers as entities
                        name_servers = whois_data.get("name_servers", [])
                        for ns in name_servers:
                            if ns:
                                await _get_or_create_entity(
                                    db, scan_id, EntityType.DOMAIN, ns.lower(),
                                    metadata={"source": "whois", "type": "name_server"}
                                )
                        
                        logger.info(f"WHOIS completed for {target}")
                    else:
                        logger.warning(f"WHOIS failed for {target}: {whois_result.get('error')}")
                        
                except Exception as e:
                    logger.error(f"Error running WHOIS for {target}: {e}", exc_info=True)
            
            # Run SSL certificate module
            if "ssl" in modules:
                try:
                    logger.info(f"Running SSL certificate lookup for {target}")
                    ssl_result = await run_ssl(target)
                    
                    if ssl_result.get("success"):
                        ssl_data = ssl_result.get("data", {})
                        
                        # Create finding for SSL certificate data
                        domain_entity = await _get_or_create_entity(
                            db, scan_id, EntityType.DOMAIN, target
                        )
                        
                        await _create_finding(
                            db, domain_entity.id, "ssl", "certificate_transparency",
                            confidence_score=1.0, raw_result=ssl_data
                        )
                        
                        # Extract subdomains as entities
                        subdomains = ssl_data.get("subdomains", [])
                        for subdomain in subdomains:
                            if subdomain and subdomain != target:
                                await _get_or_create_entity(
                                    db, scan_id, EntityType.SUBDOMAIN, subdomain.lower(),
                                    metadata={"source": "ssl", "parent_domain": target}
                                )
                        
                        logger.info(f"SSL certificate lookup completed for {target}, found {len(subdomains)} subdomains")
                    else:
                        logger.warning(f"SSL lookup failed for {target}: {ssl_result.get('error')}")
                        
                except Exception as e:
                    logger.error(f"Error running SSL lookup for {target}: {e}", exc_info=True)
            
            # Update scan status to completed
            finished_at = datetime.utcnow()
            await _update_scan_status(db, scan_id, ScanStatus.COMPLETED, finished_at=finished_at)
            logger.info(f"Scan {scan_id} completed successfully")
            
        except Exception as e:
            logger.error(f"Error in scan {scan_id}: {e}", exc_info=True)
            # Update scan status to failed
            try:
                finished_at = datetime.utcnow()
                await _update_scan_status(db, scan_id, ScanStatus.FAILED, finished_at=finished_at)
            except Exception as update_error:
                logger.error(f"Failed to update scan status: {update_error}", exc_info=True)
            raise


@celery_app.task(name="scan_domain", bind=True)
def scan_domain_task(self, scan_id: int, target: str, modules: list):
    """
    Background task to run OSINT scan on a domain
    
    Args:
        scan_id: Scan database ID
        target: Domain to scan
        modules: List of modules to run
    """
    try:
        # Run async scan function
        # Use asyncio.run() which creates a new event loop
        # Celery tasks run in separate processes, so this should work
        asyncio.run(_run_scan_async(scan_id, target, modules))
    except Exception as e:
        logger.error(f"Celery task failed for scan {scan_id}: {e}", exc_info=True)
        raise


@celery_app.task(name="scan_email", bind=True)
def scan_email_task(self, scan_id: int, target: str, modules: list):
    """
    Background task to run OSINT scan on an email
    
    Args:
        scan_id: Scan database ID
        target: Email to scan
        modules: List of modules to run
    """
    # For now, email scans use the same logic as domain scans
    # TODO: Implement email-specific OSINT modules
    try:
        asyncio.run(_run_scan_async(scan_id, target, modules))
    except Exception as e:
        logger.error(f"Celery task failed for email scan {scan_id}: {e}", exc_info=True)
        raise


