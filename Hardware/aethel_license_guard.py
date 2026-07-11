# ──────────────────────────────────────────────────────────────────────────
# FILE: hardware/aethel_license_guard.py
# ROLE: Cryptographic Licensing Guard, Telemetry Hub, and Remote Off-Switch
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import json
import logging
import urllib.request
import urllib.error
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AethelLicenseGuard")

class AethelLicenseGuard:
    def __init__(self, license_key: str = "DEMO_UNPAID_KEY"):
        self.license_key = license_key
        # In production, point this to your secure control panel API endpoint
        self.auth_endpoint = "https://api.aethelmatrix.com/v1/verify"
        self.is_active = True

    def verify_access_and_report_telemetry(self, telemetry_data: Dict[str, Any]) -> bool:
        """
        Pings the central licensing system to verify the user identity, reports
        what type of data they are rendering, and checks the status of the remote off-switch.
        """
        logger.info(f"🔒 GUARD: Verifying license authority token: [{self.license_key}]...")
        
        # Prepare the telemetry packet detailing what the user is doing with the repo
        payload = {
            "license_key": self.license_key,
            "telemetry": {
                "vertex_count": telemetry_data.get("vertex_count", 0),
                "render_mode": telemetry_data.get("render_mode", "Standard silicon"),
                "system_user": os.getlogin() if hasattr(os, 'getlogin') else "unknown"
            }
        }
        
        # Self-contained fallback logic: If offline or unable to connect, we allow execution 
        # but log strict warnings, ensuring paying clients aren't bricked by network blips.
        try:
            # Code structure prepared for production HTTP REST request hook:
            # req = urllib.request.Request(self.auth_endpoint, data=json.dumps(payload).encode('utf-8'))
            # ...
            
            # Mocking server response rules for security testing
            if self.license_key == "REVOKED_USER" or self.license_key == "DEMO_UNPAID_KEY":
                self.is_active = False
                logger.error("🚨 GUARD: ACCESS DENIED. License is invalid or remote off-switch flipped.")
                return False
                
            logger.info("🔑 GUARD: License verified successfully. Remote kill-switch is green.")
            return True
            
        except Exception as e:
            logger.warning(f"⚠️ GUARD: Telemetry network unreachable ({str(e)}). Proceeding on local grace period.")
            return True

    def enforce_gatekeeper(self):
        """
        Strict structural gatekeeper function. Raises an explicit environment halt if unauthorized.
        """
        if not self.is_active:
            raise PermissionError("❌ CRITICAL: Software execution halted by remote administrator. Unlicensed usage detected.")
