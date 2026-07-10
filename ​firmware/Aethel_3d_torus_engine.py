import numpy as np

class Aethel3DTorusEngine:
    def __init__(self, grid_size=16):
        self.grid_size = grid_size
        
        # 1. 3D TERNARY REGISTER: Map states to a 3D volumetric grid (-1, 0, +1)
        self.ternary_volume_register = np.zeros((grid_size, grid_size, grid_size), dtype=int)
        
        # 2. 3D TOPOGRAPHY: A continuous volumetric field map
        self.topographic_volume_map = np.zeros((grid_size, grid_size, grid_size))

    def map_coordinates_to_3d_torus(self, x, y, z):
        """Maps 3D floating inputs into continuous, wrapped 3D torus grid indices."""
        idx_x = int((x % 1.0) * (self.grid_size - 1))
        idx_y = int((y % 1.0) * (self.grid_size - 1))
        idx_z = int((z % 1.0) * (self.grid_size - 1))
        return idx_x, idx_y, idx_z

    def process_3d_ternary_topography(self, x, y, z, raw_signal):
        """Evaluates raw signals into ternary states across 3D coordinates."""
        idx_x, idx_y, idx_z = self.map_coordinates_to_3d_torus(x, y, z)
        
        if raw_signal > 1.5:
            ternary_state = 1
        elif raw_signal < -1.5:
            ternary_state = -1
        else:
            ternary_state = 0
            
        self.ternary_volume_register[idx_x, idx_y, idx_z] = ternary_state
        self.topographic_volume_map[idx_x, idx_y, idx_z] = float(ternary_state) * -1.0

    def calculate_3d_tensegrity(self, x, y, z):
        """
        Calculates directional tension pulling on a 3D node from its 6 primary 
        adjacent neighbors (North/South, East/West, Front/Back) across 3D wrapped boundaries.
        """
        idx_x, idx_y, idx_z = self.map_coordinates_to_3d_torus(x, y, z)
        
        # Periodic boundaries wrap across all three independent axes using modulo
        east_idx  = (idx_x + 1) % self.grid_size
        west_idx  = (idx_x - 1) % self.grid_size
        north_idx = (idx_y + 1) % self.grid_size
        south_idx = (idx_y - 1) % self.grid_size
        front_idx = (idx_z + 1) % self.grid_size
        back_idx  = (idx_z - 1) % self.grid_size
        
        # Extract stress levels from the surrounding 3D field grid
        t_e = self.topographic_volume_map[east_idx, idx_y, idx_z]
        t_w = self.topographic_volume_map[west_idx, idx_y, idx_z]
        t_n = self.topographic_volume_map[idx_x, north_idx, idx_z]
        t_s = self.topographic_volume_map[idx_x, south_idx, idx_z]
        t_f = self.topographic_volume_map[idx_x, idx_y, front_idx]
        t_b = self.topographic_volume_map[idx_x, idx_y, back_idx]
        
        # 3D differential tension vectors
        net_x = t_e - t_w
        net_y = t_n - t_s
        net_z = t_f - t_b
        
        return net_x, net_y, net_z
