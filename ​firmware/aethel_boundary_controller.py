# ──────────────────────────────────────────────────────────────────────────
# FILE: firmware/aethel_boundary_controller.py
# ROLE: Toroidal DMA Streaming & Predictive Power-Rail Regulation Controller
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging
from typing import Dict, Any, Tuple

logger = logging.getLogger("AethelBoundaryController")

class AethelBoundaryController:
    def __init__(self, grid_resolution: int = 16, base_rail_voltage: float = 1.2):
        """
        Manages high-throughput boundary interfaces, handling spatial DMA 
        transfers and proactive power-rail voltage regulation.
        """
        self.res = grid_resolution
        self.base_voltage = base_rail_voltage
        self.current_rail_voltage = base_rail_voltage

    def execute_spatial_dma_stream(self, host_memory_buffer: np.ndarray, target_z_slice: int) -> np.ndarray:
        """
        [Domain 23: DMA Boundary Controllers]
        Streaming ingestion matrix. Takes a flat host data buffer and maps it 
        directly into a spatial 2D tensor slice ready for Tier 1 ingestion.
        """
        expected_elements = self.res * self.res
        # Truncate or pad input buffer to match the spatial slice footprint
        flat_data = host_memory_buffer.flatten()
        if flat_data.size < expected_elements:
            flat_data = np.pad(flat_data, (0, expected_elements - flat_data.size), 'constant')
        else:
            flat_data = flat_data[:expected_elements]
            
        # Shape data instantly into spatial layout matching the 3-Torus matrix slice
        spatial_slice = flat_data.reshape((self.res, self.res))
        logger.info(f"📥 DMA: Streamed host memory block directly to 3-Torus space slice [Z-INDEX: {target_z_slice}].")
        return spatial_slice

    def predict_and_scale_power_rails(self, upcoming_braid_steps: list) -> Dict[str, Any]:
        """
        [Domain 24: Predictive Quantization & Voltage Scaling Controllers]
        Parses upcoming compiler steps to proactively adjust voltage rails 
        before severe computational load changes occur.
        """
        # Count how many active memristor operations are scheduled in the next cycle
        active_gate_count = sum(1 for step in upcoming_braid_steps if step.get("gate_configuration") == "MEMRISTOR_CONTRACTION_MODE")
        
        # Proactively scale voltage based on scheduled structural load
        load_factor = active_gate_count / max(1, len(upcoming_braid_steps))
        voltage_offset = load_factor * 0.35  # Max delta allowance of 350mV
        
        target_voltage = self.base_voltage + voltage_offset
        voltage_delta = target_voltage - self.current_rail_voltage
        self.current_rail_voltage = target_voltage
        
        if abs(voltage_delta) > 0.05:
            logger.info(f"⚡ POWER: Proactively shifting rail voltage to {target_voltage:.3f}V (Delta: {voltage_delta:+.3f}V) for upcoming load.")
            
        return {
            "target_rail_voltage": target_voltage,
            "proactive_adjustment_mv": voltage_delta * 1000.0,
            "power_rail_stabilized": True
        }
