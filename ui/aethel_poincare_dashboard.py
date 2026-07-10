import os
import numpy as np

class AethelPoincareDashboard:
    def __init__(self, grid_size=16):
        self.grid_size = grid_size
        # ASCII density scale to represent different field potentials
        self.ascii_chars = [" ", ".", "-", "=", "+", "*", "#", "%", "@"]

    def _value_to_ascii(self, val, max_val=1.0):
        """Maps a floating-point potential value to an ASCII character density."""
        normalized = max(0, min(len(self.ascii_chars) - 1, 
                     int((val / (max_val + 1e-6)) * (len(self.ascii_chars) - 1))))
        return self.ascii_chars[normalized]

    def clear_terminal(self):
        """Clears the terminal screen dynamically for real-time frame animation."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def render_field_slices(self, step, pos, velocities, potential_map, anomaly_flag):
        """
        Renders a side-by-side 2D cross-sectional matrix slice layout of the 
        active 3D Three-Torus field potential configuration.
        """
        self.clear_terminal()
        px, py, pz = pos
        vx, vy, vz = velocities
        
        # Calculate current lattice index of the tracked particle
        idx_x = int((px % 1.0) * (self.grid_size - 1))
        idx_y = int((py % 1.0) * (self.grid_size - 1))
        idx_z = int((pz % 1.0) * (self.grid_size - 1))

        print("=" * 78)
        print(f" AETHEL CORE 3T MONITOR // STEP {step:03d} // SYSTEM STATE TENSOR DASHBOARD")
        print("=" * 78)
        print(f" POSITION:   X: {px:.4f}  | Y: {py:.4f}  | Z: {pz:.4f}  (Grid Map: [{idx_x},{idx_y},{idx_z}])")
        print(f" VELOCITIES: Vx:{vx:+.4f} | Vy:{vy:+.4f} | Vz:{vz:+.4f}")
        
        status_string = "⚠️  [ANOMALY TRIGGERED]" if anomaly_flag else "✅ [LOGIC SECURE]"
        print(f" PARADIGM GÖDEL STATE: {status_string}")
        print("-" * 78)
        
        # Render the XY Slice (at the particle's current Z index) and XZ Slice side-by-side
        print("     [XY CROSS-SECTION SLICE]             [XZ CROSS-SECTION SLICE]")
        print("    " + " ".join([str(i%10) for i in range(self.grid_size)]) + "        " + " ".join([str(i%10) for i in range(self.grid_size)]))
        
        for y in range(self.grid_size):
            xy_line = ""
            xz_line = ""
            for x in range(self.grid_size):
                # XY slice calculation
                val_xy = abs(potential_map[x, y, idx_z])
                char_xy = "O" if (x == idx_x and y == idx_y) else self._value_to_ascii(val_xy)
                xy_line += char_xy + " "
                
                # XZ slice calculation (using current Y index)
                val_xz = abs(potential_map[x, idx_y, y])
                char_xz = "O" if (x == idx_x and y == idx_z) else self._value_to_ascii(val_xz)
                xz_line += char_xz + " "
                
            print(f"{y:02d}  {xy_line}    {y:02d}  {xz_line}")
            
        print("=" * 78)
        print(" Legend: 'O' = Tracked Qubit Particle Boundary | Density Scale: [ .-=+*#%@ ]")
