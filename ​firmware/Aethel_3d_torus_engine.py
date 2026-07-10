import numpy as np

class Aethel3DTorusEngine:
    def __init__(self, grid_size=16):
        self.grid_size = grid_size
        
        # 1. 3D TERNARY REGISTER: Map states to a 3D volumetric grid (-1, 0, +1)
        self.ternary_volume_register = np.zeros((grid_size, grid_size, grid_size), dtype=int)
        
        # 2. 3D TOPOGRAPHY: A continuous volumetric potential field map
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
        # Inject raw mathematical potential energy delta at that node
        self.topographic_volume_map[idx_x, idx_y, idx_z] = float(ternary_state) * -1.0

    def relax_3d_field_potentials(self, iterations=3, diffusion_factor=0.15):
        """
        [THE RELAXATION ALGORITHM]
        Applies a discrete 3D Laplace finite-difference relaxation sweep.
        Propagates localized potential distortions outward into adjacent 3D space 
        while maintaining perfect periodic wrapping across the 3-Torus boundaries.
        """
        for _ in range(iterations):
            next_map = np.copy(self.topographic_volume_map)
            
            # Vectorized shift operations with roll over axes to execute 3D boundary-wrapped relaxation
            east  = np.roll(self.topographic_volume_map, shift=-1, axis=0)
            west  = np.roll(self.topographic_volume_map, shift=1,  axis=0)
            north = np.roll(self.topographic_volume_map, shift=-1, axis=1)
            south = np.roll(self.topographic_volume_map, shift=1,  axis=1)
            front = np.roll(self.topographic_volume_map, shift=-1, axis=2)
            back  = np.roll(self.topographic_volume_map, shift=1,  axis=2)
            
            # Calculate average neighbor state across 6 points of spatial contact
            neighbor_average = (east + west + north + south + front + back) / 6.0
            
            # Smooth the field toward equilibrium based on diffusion coefficient
            self.topographic_volume_map = (1.0 - diffusion_factor) * self.topographic_volume_map + diffusion_factor * neighbor_average

    def calculate_3d_tensegrity(self, x, y, z):
        """Calculates directional tension pulling on a 3D node from its neighbors."""
        idx_x, idx_y, idx_z = self.map_coordinates_to_3d_torus(x, y, z)
        
        east_idx  = (idx_x + 1) % self.grid_size
        west_idx  = (idx_x - 1) % self.grid_size
        north_idx = (idx_y + 1) % self.grid_size
        south_idx = (idx_y - 1) % self.grid_size
        front_idx = (idx_z + 1) % self.grid_size
        back_idx  = (idx_z - 1) % self.grid_size
        
        t_e = self.topographic_volume_map[east_idx, idx_y, idx_z]
        t_w = self.topographic_volume_map[west_idx, idx_y, idx_z]
        t_n = self.topographic_volume_map[idx_x, north_idx, idx_z]
        t_s = self.topographic_volume_map[idx_x, south_idx, idx_z]
        t_f = self.topographic_volume_map[idx_x, idx_y, front_idx]
        t_b = self.topographic_volume_map[idx_x, idx_y, back_idx]
        
        return (t_e - t_w), (t_n - t_s), (t_f - t_b)
