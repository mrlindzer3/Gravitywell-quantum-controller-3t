# ──────────────────────────────────────────────────────────────────────────
# FILE: hardware/aethel_quantum_shuttler.py
# ROLE: Sideband Phonon Cooler & Adiabatic Quantum State Shuttler
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging
from typing import Dict, Any, Tuple

logger = logging.getLogger("AethelQuantumShuttler")

class AethelQuantumShuttler:
    def __init__(self, cavity_resonance_ghz: float = 193400.0, mechanical_omega_m_mhz: float = 300.0):
        """
        Manages sideband optical pumping for phononic quantum ground-state cooling 
        and executes STIRAP-driven adiabatic mechanical state transfers.
        """
        self.omega_c = cavity_resonance_ghz
        self.omega_m = mechanical_omega_m_mhz / 1e3 # Convert to GHz
        self.current_phonon_occupancy = 12.5 # Initial thermal occupancy state

    def calculate_red_sideband_pump_frequency(self) -> float:
        """
        [Domain 67: Sympathetic Phononic Sideband Cooling]
        Calculates the exact laser pump frequency required to target the red-detuned 
        motional sideband, driving phonon extraction down to the quantum ground state.
        """
        # Red sideband target: w_pump = w_cavity - w_mechanical
        target_pump_frequency_ghz = self.omega_c - self.omega_m
        
        # Simulate phonon extraction down toward the ground state limit (n -> 0)
        if self.current_phonon_occupancy > 0.05:
            self.current_phonon_occupancy *= 0.4
            logger.info(f"❄️ SIDEBAND: Red-detuned laser pump active at {target_pump_frequency_ghz:.4f} GHz. Mean phonon occupancy dropped to {self.current_phonon_occupancy:.4f}.")
            
        return target_pump_frequency_ghz

    def calculate_stirap_pulse_overlap(self, coupling_strength_mhz: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        [Domain 68: Coherent Adiabatic State Transfer]
        Generates the counter-intuitive pulse timing profiles (Pump and Stokes waves) 
        needed to achieve high-fidelity adiabatic state shuttling between mechanical nodes.
        """
        time_steps = np.linspace(-5, 5, 100)
        
        # STIRAP requires the Stokes pulse to arrive BEFORE the Pump pulse to form the dark state
        stokes_pulse = coupling_strength_mhz * np.exp(-(time_steps + 1.5)**2 / 2.0)
        pump_pulse = coupling_strength_mhz * np.exp(-(time_steps - 1.5)**2 / 2.0)
        
        fidelity = 1.0 - (0.0001 / max(1.0, coupling_strength_mhz))
        logger.info(f"🌊 STIRAP: Counter-intuitive pulse sequence generated. Predicted State Transfer Fidelity: {fidelity * 100.0:.3f}%.")
        
        return pump_pulse, stokes_pulse
