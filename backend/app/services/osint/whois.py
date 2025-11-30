"""
WHOIS module
"""
import whois
from typing import Dict, Any
from datetime import datetime


async def run_whois(target: str) -> Dict[str, Any]:
    """
    Run WHOIS lookup on a domain
    
    Args:
        target: Domain name to lookup
        
    Returns:
        Dictionary with WHOIS data
    """
    try:
        domain = whois.whois(target)
        
        result = {
            "domain": target,
            "registrar": domain.registrar if hasattr(domain, "registrar") else None,
            "creation_date": domain.creation_date.isoformat() if domain.creation_date else None,
            "expiration_date": domain.expiration_date.isoformat() if domain.expiration_date else None,
            "name_servers": list(domain.name_servers) if domain.name_servers else [],
            "status": domain.status if hasattr(domain, "status") else None,
            "raw": str(domain),
        }
        
        return {
            "success": True,
            "data": result,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat(),
        }












