# ──────────────────────────────────────────────────────────────────────────
# FILE: hardware/aethel_optomechanics_controller.py
# ROLE: Parametric Motion Feedback Cooler & UHV Pressure Regulator
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging
from typing import Dict, Any, Tuple

logger = logging.getLogger("AethelOptomechanicsController")

class AethelOptomechanicsController:
    def __init__(self, mechanical_resonance_hz: float = 125000.0, target_vacuum_torr: float = 1e-10):
        """
        Manages real-time active parametric feedback cooling for levitated 
        optomechanical particles and monitors ultra-high vacuum stability boundaries.
        """
        self.omega_0 = mechanical_resonance_hz
        self.target_vacuum = target_vacuum_torr
        self.active_ion_pump_voltage = 3000.0 # Baseline ion pump operating voltage

    def calculate_parametric_cooling_modulation(self, particle_position_displacement: np.ndarray, current_velocity: np.ndarray) -> float:
        """
        [Domain 65: Active Parametric Feedback Motion Cooling]
        Calculates the laser intensity modulation factor required to exert an optical 
        damping force on a levitated particle, lowering its effective center-of-mass temperature.
        """
        # Damping force requires modulating laser power out of phase with velocity (Force ~ -v)
        displacement_norm = float(np.linalg.norm(particle_position_displacement))
        velocity_norm = float(np.linalg.norm(current_velocity))
        
        if displacement_norm > 0.001:
            # Apply modulation proportional to the position-velocity product to achieve 2*omega parametric damping
            modulation_depth = np.clip(displacement_norm * velocity_norm * 2.5, 0.0, 0.20)
            logger.info(f"✨ OPTOMECHANICS: Particle jitter detected. Applying parametric braking modulation: {modulation_depth*100.0:.2f}%.")
            return modulation_depth
            
        return 0.0

    def regulate_uhv_getter_pumps(self, measured_pressure_torr: float) -> float:
        """
        [Domain 66: Ultra-High Vacuum (UHV) Ion-Pump Controllers]
        Dynamically adjusts integrated ion-getter pump bias voltages to suppress 
        outgassing spikes inside the levitation cavity.
        """
        if measured_pressure_torr > self.target_vacuum:
            # Scale voltage to accelerate gas ionization and capture rates
            pressure_ratio = measured_pressure_torr / self.target_vacuum
            self.active_ion_pump_voltage = np.clip(3000.0 * np.log10(pressure_ratio + 9.0), 3000.0, 7000.0)
            logger.warning(f"💨 VACUUM: Pressure spike detected ({measured_pressure_torr:.2e} Torr). Escalating Ion Pump Bias to {self.active_ion_pump_voltage:.1f} V.")
        else:
            self.active_ion_pump_voltage = 3000.0
            
        return self.active_ion_pump_voltage
