#!/usr/bin/env python3
"""
Verify code structure and imports for AI-OSINT-Kit
This script checks that all modules can be imported and basic structure is correct.
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

def check_imports():
    """Check that all main modules can be imported"""
    errors = []
    warnings = []
    
    print("[*] Checking imports...")
    
    # Check database models
    try:
        from app.models import User, Scan, Entity, Finding, Report
        print("[OK] Database models imported successfully")
    except Exception as e:
        errors.append(f"Failed to import models: {e}")
        print(f"[ERROR] Failed to import models: {e}")
    
    # Check database connection
    try:
        from app.db.database import Base, get_db, init_db
        print("[OK] Database module imported successfully")
    except Exception as e:
        errors.append(f"Failed to import database: {e}")
        print(f"[ERROR] Failed to import database: {e}")
    
    # Check OSINT modules
    try:
        from app.services.osint import run_whois, run_ssl
        print("[OK] OSINT modules imported successfully")
    except Exception as e:
        warnings.append(f"Failed to import OSINT modules: {e}")
        print(f"[WARN] Failed to import OSINT modules: {e}")
    
    # Check Celery tasks
    try:
        from app.tasks.scan import celery_app, scan_domain_task, scan_email_task
        print("[OK] Celery tasks imported successfully")
    except Exception as e:
        warnings.append(f"Failed to import Celery tasks: {e}")
        print(f"[WARN] Failed to import Celery tasks: {e}")
    
    # Check API endpoints
    try:
        from app.api.v1.endpoints.scan import router, ScanRequest, ScanResponse
        print("[OK] API endpoints imported successfully")
    except Exception as e:
        errors.append(f"Failed to import API endpoints: {e}")
        print(f"[ERROR] Failed to import API endpoints: {e}")
    
    # Check configuration
    try:
        from app.core.config import settings
        print("[OK] Configuration imported successfully")
    except Exception as e:
        errors.append(f"Failed to import configuration: {e}")
        print(f"[ERROR] Failed to import configuration: {e}")
    
    return errors, warnings

def check_migration_file():
    """Check that migration file exists and is valid"""
    print("\n[*] Checking migration file...")
    
    migration_file = backend_path / "alembic" / "versions" / "001_initial_migration.py"
    
    if not migration_file.exists():
        print(f"[ERROR] Migration file not found: {migration_file}")
        return False
    
    print(f"[OK] Migration file exists: {migration_file}")
    
    # Check file contents
    try:
        with open(migration_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Check for required components
            if 'revision =' in content:
                print("[OK] Migration has revision ID")
            else:
                print("[WARN] Migration missing revision ID")
            
            if 'def upgrade()' in content:
                print("[OK] Migration has upgrade function")
            else:
                print("[ERROR] Migration missing upgrade function")
                return False
            
            if 'def downgrade()' in content:
                print("[OK] Migration has downgrade function")
            else:
                print("[WARN] Migration missing downgrade function")
            
            # Check for table creations
            tables = ['users', 'scans', 'entities', 'findings', 'reports']
            for table in tables:
                if f"'{table}'" in content or f'"{table}"' in content:
                    print(f"[OK] Migration includes {table} table")
                else:
                    print(f"[WARN] Migration missing {table} table")
            
    except Exception as e:
        print(f"[ERROR] Error reading migration file: {e}")
        return False
    
    return True

def check_ssl_module():
    """Check SSL module implementation"""
    print("\n[*] Checking SSL module...")
    
    ssl_module = backend_path / "app" / "services" / "osint" / "ssl.py"
    
    if not ssl_module.exists():
        print("[ERROR] SSL module not found")
        return False
    
    print("[OK] SSL module exists")
    
    try:
        with open(ssl_module, 'r', encoding='utf-8') as f:
            content = f.read()
            
            if 'async def run_ssl' in content:
                print("[OK] SSL module has run_ssl function")
            else:
                print("[ERROR] SSL module missing run_ssl function")
                return False
            
            if 'crt.sh' in content or 'CRTSH_API_URL' in content:
                print("[OK] SSL module uses crt.sh API")
            else:
                print("[WARN] SSL module may not use crt.sh API")
            
    except Exception as e:
        print(f"[ERROR] Error reading SSL module: {e}")
        return False
    
    return True

def main():
    """Main verification function"""
    print("=" * 60)
    print("AI-OSINT-Kit Code Verification")
    print("=" * 60)
    print()
    
    errors, warnings = check_imports()
    migration_ok = check_migration_file()
    ssl_ok = check_ssl_module()
    
    print("\n" + "=" * 60)
    print("Verification Summary")
    print("=" * 60)
    
    if errors:
        print(f"\n[ERROR] Errors found: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
    
    if warnings:
        print(f"\n[WARN] Warnings: {len(warnings)}")
        for warning in warnings:
            print(f"  - {warning}")
    
    if not errors and migration_ok and ssl_ok:
        print("\n[OK] All checks passed!")
        print("\nNext steps:")
        print("1. Start Docker services: docker compose up -d")
        print("2. Run migration: ./scripts/run_migration.sh (or scripts\\run_migration.bat on Windows)")
        print("3. Test the API: curl http://localhost:8000/health")
        return 0
    else:
        print("\n[WARN] Some checks failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

