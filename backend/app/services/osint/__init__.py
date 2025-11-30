"""OSINT modules"""
from app.services.osint.whois import run_whois
from app.services.osint.ssl import run_ssl

__all__ = ["run_whois", "run_ssl"]

