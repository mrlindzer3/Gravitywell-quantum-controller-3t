# ──────────────────────────────────────────────────────────────────────────
# FILE: ui/aethel_poincare_dashboard.py
# ROLE: Real-Time Multi-Panel Volumetric ASCII Matrix Interface
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import os
import numpy as np
from typing import Tuple, Dict, Any

class AethelPoincareDashboard:
    def __init__(self, grid_size: int = 16):
        """
        Initializes an enterprise-grade terminal-based visualization cockpit
        to monitor hardware metrics, recycling loops, and braid trajectories.
        """
        self.grid_size = grid_size
        self.terminal_width = 90

    def clear_terminal(self):
        """Forces a clean console refresh frame-by-frame."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def _generate_ascii_slice(self, potential_map: np.ndarray, current_z: float) -> list:
        """Renders a 2D cross-section spatial slice of the 3-Torus manifold."""
        z_idx = int((current_z * self.grid_size) % self.grid_size)
        slice_data = potential_map[:, :, z_idx]
        
        # ASCII density gradients to map field intensity visually
        chars = [" ", ".", "-", "=", "+", "*", "#", "%", "@"]
        max_val = np.max(np.abs(slice_data)) if np.max(np.abs(slice_data)) > 0 else 1.0
        
        lines = []
        for r in range(self.grid_size):
            row_str = ""
            for c in range(self.grid_size):
                val = abs(slice_data[r, c])
                char_idx = min(int((val / max_val) * (len(chars) - 1)), len(chars) - 1)
                row_str += chars[char_idx] + " "
            lines.append(row_str)
        return lines

    def render_field_slices(self, step: int, pos: Tuple[float, float, float], 
                             velocities: Tuple[float, float, float], potential_map: np.ndarray, 
                             anomaly_flag: bool, recycling_metrics: Dict[str, float],
                             cluster_status: Dict[str, Any], compiler_braid_id: str = "TENSOR_0"):
        """
        Draws the synchronized multi-panel dashboard directly to stdout.
        """
        self.clear_terminal()
        px, py, pz = pos
        vx, vy, vz = velocities
        
        # 1. Generate the spatial manifold ASCII projection slice
        ascii_lines = self._generate_ascii_slice(potential_map, pz)
        
        # Header block banner
        print("═" * self.terminal_width)
        print(f" AETHEL CORE CORE SYSTEM INTERFACE v3.1.0 // FRAME RUNTIME STEP: {step:03d}")
        print("═" * self.terminal_width)
        
        # 2. Render Left Panel (Spatial Geometry) side-by-side with Right Panel (Hardware Diagnostics)
        print(f" [3-TORUS SPATIAL REFRACTION SLICE (Z-INDEX: {int((pz*self.grid_size)%self.grid_size):02d})] │ [SUBSTRATE OPERATING METRICS]")
        
        right_panel_metrics = [
            f"• Core Spatial Position  : ({px:.3f}, {py:.3f}, {pz:.3f})",
            f"• Tensored Velocity Bias : ({vx:.3f}, {vy:.3f}, {vz:.3f})",
            f"• Active Compiler Braid  : {compiler_braid_id}",
            f"• Gödel Hardware Guard   : {'⚠️ ANOMALY INTERCEPT' if anomaly_flag else '✅ LOGIC SECURE'}",
            "─" * 43,
            f" [5-POINT THERMODYNAMIC RECYCLING HARVEST] ",
            f"• Phonon Lattice Intercept: {recycling_metrics.get('Phonon_Recovered_nJ', 0.0):.3f} nJ",
            f"• Photonic & Back-EMF     : {recycling_metrics.get('Photonic_Recovered_nJ', 0.0):.3f} nJ",
            f"• Seebeck Cross-Layer Grad: {recycling_metrics.get('Seebeck_Recovered_nJ', 0.0):.3f} nJ",
            f"• Kinetic Drag Recovery   : {recycling_metrics.get('Kinetic_Recovered_nJ', 0.0):.3f} nJ",
            f"• Cumulative Energy Saved : {recycling_metrics.get('Total_Reclaimed_Energy_nJ', 0.0):.3f} nJ",
            "─" * 43,
            f" [SUPER-TORUS CLUSTER SCALABILITY HEALTH] ",
            f"• Active Array Clustering: {cluster_status.get('Total_Active_Chips', 1)} Physical Node Die(s)",
            f"• Total Grid Intersects  : {cluster_status.get('Total_Cluster_Grid_Points', 4096)} Nodes",
            f"• Inter-Chip Data Lanes  : {cluster_status.get('Inter_Chip_Interconnect_Lanes', 0)} Optical Channels"
        ]
        
        # Merge columns line-by-line for stable terminal layout formatting
        for i in range(self.grid_size):
            left_side = ascii_lines[i] if i < len(ascii_lines) else " " * (self.grid_size * 2)
            right_side = right_panel_metrics[i] if i < len(right_panel_metrics) else ""
            print(f"   {left_side} │ {right_side}")
            
        print("═" * self.terminal_width)
        print(" SYSTEM COMMAND CONSOLE KEY: [Ctrl+C] to Halt Emulation Track Pipeline")
        print("═" * self.terminal_width)
