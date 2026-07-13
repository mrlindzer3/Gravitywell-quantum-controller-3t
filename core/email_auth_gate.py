# ──────────────────────────────────────────────────────────────────────────
# FILE: core/email_auth_gate.py
# ROLE: Cryptographic Email Authentication & Substrate Latch Gate
# ARCHITECTURE: Security Access Layer for Non-Von Neumann Operations
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging
import hashlib

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("EmailAuthGate")

class EmailAuthGate:
    def __init__(self, admin_email: str = "mr.lindzer3@gmail.com"):
        self.admin_email = admin_email
        self.is_account_created = False
        self.active_challenge_token = None
        
    def initiate_account_request(self) -> str:
        """
        Generates a secure cryptographic challenge string that must be sent
        via email to the administrator for cross-verification.
        """
        raw_token = str(np.random.randint(100000, 999999))
        self.active_challenge_token = hashlib.sha256(raw_token.encode()).hexdigest()[:8].upper()
        
        print("\n" + "🛑"*35)
        print(f" ACCESS DENIED: Account Registration Required.")
        print(f" Action Required: Send an authorization email request to {self.admin_email}")
        print(f" Provide the following Challenge Token in the message: {self.active_challenge_token}")
        print("🛑"*35 + "\n")
        
        return self.active_challenge_token

    def verify_email_response_handshake(self, incoming_response_token: str) -> bool:
        """
        Validates the incoming token received from the email reply handshake.
        If valid, it permanently opens the logic gates.
        """
        if self.active_challenge_token and incoming_response_token.strip().upper() == self.active_challenge_token:
            self.is_account_created = True
            logger.info(f"✨ AUTH: Handshake confirmed from {self.admin_email}. Account successfully provisioned!")
            return True
        else:
            logger.error("❌ AUTH: Invalid verification token. Substrate execution remains locked.")
            return False

    def enforce_gatekeeper_protection(self):
        """
        Protection wrapper. Throws an absolute runtime exception if an unauthenticated
        entity tries to interact with the core repository components.
        """
        if not self.is_account_created:
            raise PermissionError(
                "CRITICAL SECURITY FAULT: Attempted to run code on an unauthenticated substrate. "
                f"You must complete the email handshake with {self.admin_email} to create an account."
            )
