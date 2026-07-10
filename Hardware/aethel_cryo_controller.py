# ──────────────────────────────────────────────────────────────────────────
# FILE: hardware/aethel_cryo_controller.py
# ROLE: Cryogenic Helium Loop Throttler & Superconducting Power Monitor
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging
from typing import Dict, List, Any, Tuple

logger = logging.getLogger("AethelCryoController")

class AethelCryoController:
    def __init__(self, target_temperature_k: float = 0.015, max_current_amps: float = 120.0):
        """
        Manages sub-Kelvin helium re-condensation micro-fluidic loops and 
        monitors critical current boundaries across the superconducting power rails.
        """
        self.target_temp = target_temperature_k
        self.max_current = max_current_amps
        self.current_temp_k = target_temperature_k
        self.superconducting_state_locked = True

    def throttle_helium_fluidic_valves(self, measured_temperatures: np.ndarray) -> float:
        """
        [Domain 57: Closed-Loop Helium-3 Re-Condensation Thermal Isolation]
        Calculates the required micro-fluidic valve aperture shift based on 
        live wafer thermal telemetry to nullify micro-Kelvin hot spots.
        """
        avg_temp = float(np.mean(measured_temperatures))
        temp_delta = avg_temp - self.target_temp
        
        # Proportional-Integral feedback loop to determine valve flow scaling (0.0 to 1.0)
        valve_aperture = np.clip(temp_delta * 150.0, 0.0, 1.0)
        self.current_temp_k = avg_temp
        
        if valve_aperture > 0.05:
            logger.info(f"❄️ CRYO: Substrate temperature drift detected ({avg_temp:.4f} K). Throttling Helium flow valve to {valve_aperture * 100.0:.2f}%.")
            
        return valve_aperture

    def verify_superconducting_critical_limits(self, active_load_current_amps: float) -> Dict[str, Any]:
        """
        [Domain 58: High-Current Superconducting Power Distribution Lines]
        Verifies that the power delivery network remains below the critical current 
        threshold (I_c), preventing the YBCO rails from reverting to a resistive state.
        """
        # If current exceeds critical thresholds, the material undergoes a phase transition (quench)
        if active_load_current_amps >= self.max_current:
            self.superconducting_state_locked = False
            logger.critical(f"🚨 CRYO POWER: Critical current threshold breached ({active_load_current_amps} A >= {self.max_current} A)! Superconducting state lost.")
        else:
            self.superconducting_state_locked = True
            
        return {
            "superconducting_active": self.superconducting_state_locked,
            "critical_current_margin_amps": self.max_current - active_load_current_amps,
            "rail_efficiency_ratio": 1.0 if self.superconducting_state_locked else 0.12
        }
