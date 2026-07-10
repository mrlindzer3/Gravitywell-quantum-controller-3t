# ──────────────────────────────────────────────────────────────────────────
# FILE: hardware/aethel_tapeout_validator.py
# ROLE: Lithography Rule Checker & Monolithic MIV Target Validator
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging
from typing import Dict, Tuple, List

logger = logging.getLogger("AethelTapeout")

class AethelTapeoutValidator:
    def __init__(self, target_node_nm: int = 4, max_allowable_overlay_nm: float = 0.5):
        """
        Validates 3D monolithic aspect ratios, vertical layer alignment steps, 
        and foundry DRC (Design Rule Checking) limits for the 3-Tier substrate.
        """
        self.target_node = target_node_nm
        self.max_overlay = max_allowable_overlay_nm
        
        # Physical material layer thickness references (in microns)
        self.layer_thickness_map = {
            "Tier1_CMOS_Silicon": 725.0,     # Standard handle wafer base
            "Tier2_Ge_Photodiode": 0.8,      # Epitaxial sensing film
            "Tier3_GaN_MicroLED": 1.2        # MOCVD optical cap
        }

    def validate_miv_aspect_ratios(self, via_diameter_nm: float, via_depth_nm: float) -> bool:
        """
        [Domain 11: Monolithic Epitaxial Stacking]
        Verifies that Monolithic Inter-Tier Vias (MIVs) do not exceed structural 
        aspect ratio thresholds, which could cause structural voids during metal fill.
        """
        aspect_ratio = via_depth_nm / via_diameter_nm
        max_safe_ratio = 8.0  # Foundry safety limit for ultra-dense 3D IC structural fills
        
        if aspect_ratio > max_safe_ratio:
            logger.error(f"DRC VIOLATION: MIV Aspect Ratio ({aspect_ratio:.2f}:1) is too high. Structural void danger.")
            return False
        return True

    def ingest_sem_metrology_alignment(self, overlay_errors_x_nm: np.ndarray, overlay_errors_y_nm: np.ndarray) -> Dict[str, Any]:
        """
        [Domain 12: Electron Beam Metrology]
        Ingests real angstrom-scale measurements from cleanroom CD-SEM tools 
        to identify lithography shifts across the wafer surface.
        """
        max_error_x = np.max(np.abs(overlay_errors_x_nm))
        max_error_y = np.max(np.abs(overlay_errors_y_nm))
        worst_case_error = max(max_error_x, max_error_y)
        
        tapeout_approved = worst_case_error <= self.max_overlay
        
        return {
            "Peak_Lithography_Overlay_Error_nm": worst_case_error,
            "Foundry_Tapeout_Ready": tapeout_approved,
            "Required_Calibration_Skew_X": -np.mean(overlay_errors_x_nm),
            "Required_Calibration_Skew_Y": -np.mean(overlay_errors_y_nm)
        }
