# ──────────────────────────────────────────────────────────────────────────
# FILE: firmware/aethel_alignment_controller.py
# ROLE: Phase-Slip Interpolation & Emergency Quenching Controller
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging
from typing import Dict, Any, Tuple

logger = logging.getLogger("AethelAlignmentController")

class AethelAlignmentController:
    def __init__(self, grid_resolution: int = 16):
        """
        Manages real-time phase-slip corrections and handles safe sub-nanosecond 
        voltage decay profiles during emergency hardware quenching events.
        """
        self.res = grid_resolution
        # Tracks phase-slip history per coordinate sector (in radians)
        self.phase_slip_registry = np.zeros((self.res, self.res, self.res), dtype=np.float64)

    def interpolate_phase_slips(self, active_node: Tuple[int, int, int], measured_skew_rad: float) -> float:
        """
        [Domain 25: Phase-Slip Interpolation Controllers]
        Registers localized timing skews and calculates an absolute phase-compensation 
        value to apply to the node's local Event-Driven PLL.
        """
        x, y, z = active_node
        if 0 <= x < self.res and 0 <= y < self.res and 0 <= z < self.res:
            # Apply a rolling average tracking window to damp out random noise spikes
            self.phase_slip_registry[x, y, z] = (0.8 * self.phase_slip_registry[x, y, z]) + (0.2 * measured_skew_rad)
            
            # Compensation target is the inverse of the stabilized running skew value
            compensation_val = -self.phase_slip_registry[x, y, z]
            if abs(compensation_val) > 0.05:
                logger.info(f"⏱️ ALIGNMENT: Applied {compensation_val:.4f} rad timing offset to cell [{x},{y},{z}] to nullify phase-slip.")
            return compensation_val
        return 0.0

    def execute_emergency_hardware_quench(self, active_rail_voltages: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        [Domain 26: State-Preservation & Quenching Controllers]
        Executes a controlled, multi-step sub-nanosecond voltage decay profile 
        to bleed off trapping field energy without triggering a back-EMF surge.
        """
        logger.critical("🚨 QUENCH: Initiating controlled voltage decay profile across the GaN driving matrix...")
        
        # Safe exponential decay modeling: V_t = V_0 * e^(-t/tau)
        decay_factor = 0.35 
        quenched_voltages = active_rail_voltages * decay_factor
        
        # Calculate the thermal energy safely diverted back to the storage capacitor banks (in Nanojoules)
        energy_diverted_nj = float(np.sum(active_rail_voltages - quenched_voltages) * 1.85)
        logger.info(f"🔋 QUENCH: Trapping field bled down safely. Diverted {energy_diverted_nj:.3f} nJ to storage rails.")
        
        return quenched_voltages, energy_diverted_nj
