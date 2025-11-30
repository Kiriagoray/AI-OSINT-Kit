"""
SSL Certificate module
Queries certificate transparency logs from crt.sh
"""
import httpx
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

CRTSH_API_URL = "https://crt.sh"


async def run_ssl(target: str) -> Dict[str, Any]:
    """
    Query certificate transparency logs for a domain
    
    Args:
        target: Domain name to query
        
    Returns:
        Dictionary with SSL certificate data
    """
    try:
        # Remove protocol if present
        domain = target.replace("https://", "").replace("http://", "").split("/")[0]
        
        # Query crt.sh API
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Query for certificates matching the domain
            # crt.sh API: https://crt.sh/?q=%.example.com&output=json
            # Try both with and without wildcard
            url = f"{CRTSH_API_URL}/"
            params = {
                "q": f"%.{domain}",
                "output": "json"
            }
            
            try:
                response = await client.get(url, params=params, follow_redirects=True)
                response.raise_for_status()
                certificates = response.json()
            except Exception as e:
                # If wildcard query fails, try exact match
                logger.warning(f"Wildcard query failed, trying exact match: {e}")
                params["q"] = domain
                response = await client.get(url, params=params, follow_redirects=True)
                response.raise_for_status()
                certificates = response.json()
            
            # Handle case where API returns empty list or error
            if not isinstance(certificates, list):
                certificates = []
            
            # Process and structure the certificate data
            result = {
                "domain": domain,
                "certificates": [],
                "subdomains": set(),
                "issuers": set(),
                "total_certificates": len(certificates) if isinstance(certificates, list) else 0,
            }
            
            if isinstance(certificates, list):
                for cert in certificates[:100]:  # Limit to first 100 certificates
                    cert_data = {
                        "id": cert.get("id"),
                        "logged_at": cert.get("entry_timestamp"),
                        "not_before": cert.get("not_before"),
                        "not_after": cert.get("not_after"),
                        "issuer_name": cert.get("issuer_name"),
                        "common_name": cert.get("name_value"),
                    }
                    
                    result["certificates"].append(cert_data)
                    
                    # Extract subdomains from common name and name_value
                    name_value = cert.get("name_value", "")
                    if name_value:
                        # Split by newlines (crt.sh returns multiple domains per cert)
                        for name in name_value.split("\n"):
                            name = name.strip()
                            if name and domain in name:
                                result["subdomains"].add(name)
                    
                    # Track issuers
                    if cert.get("issuer_name"):
                        result["issuers"].add(cert.get("issuer_name"))
                
                # Convert sets to lists for JSON serialization
                result["subdomains"] = sorted(list(result["subdomains"]))
                result["issuers"] = sorted(list(result["issuers"]))
            
            return {
                "success": True,
                "data": result,
                "timestamp": datetime.utcnow().isoformat(),
            }
            
    except httpx.TimeoutException:
        logger.error(f"Timeout querying crt.sh for {target}")
        return {
            "success": False,
            "error": "Request timeout",
            "timestamp": datetime.utcnow().isoformat(),
        }
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error querying crt.sh for {target}: {e}")
        return {
            "success": False,
            "error": f"HTTP error: {e.response.status_code}",
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Error querying SSL certificates for {target}: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat(),
        }

