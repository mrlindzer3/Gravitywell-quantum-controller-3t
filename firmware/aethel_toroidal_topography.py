import numpy as np

class ToroidalTopographyEngine:
    def __init__(self, grid_size=32, major_radius=2.0, minor_radius=0.5):
        self.grid_size = grid_size
        self.R = major_radius  # Distance from the center of the tube to the center of the torus
        self.r = minor_radius  # Radius of the tube itself
        
        # 1. TOPOGRAPHY: Initialize the 2D Toroidal height profile map
        self.topographic_torus_map = np.zeros((grid_size, grid_size))
        
    def map_cartesian_to_torus_indices(self, x, y):
        """
        Maps standard coordinates to continuous toroidal indices.
        Enforces periodic boundary conditions (wrapping edges seamlessly).
        """
        # Periodic boundaries: wrap inputs using modulo math
        wrapped_x = x % 1.0
        wrapped_y = y % 1.0
        
        idx_x = int(wrapped_x * (self.grid_size - 1))
        idx_y = int(wrapped_y * (self.grid_size - 1))
        return idx_x, idx_y

    def deform_torus_topography(self, x, y, ternary_bias_state):
        """
        [TERNARY + TOPOGRAPHY]
        Carves valleys or peaks directly onto the continuous toroidal surface.
        ternary_bias_state: +1 (Attraction Well), -1 (Repulsion Peak), 0 (Neutral)
        """
        idx_x, idx_y = self.map_cartesian_to_torus_indices(x, y)
        
        # Modify the landscape using the ternary state variable
        # Multiplying by -1.0 creates a trapping valley for +1 states
        self.topographic_torus_map[idx_x, idx_y] = float(ternary_bias_state) * -1.0

    def calculate_toroidal_tensegrity_tension(self, current_idx_x, current_idx_y):
        """
        [TENSEGRITY]
        Calculates the spatial tension vectors pulling on the current node
        from its adjacent neighbors across the toroidal wrap-around boundaries.
        """
        # Identify neighbors using toroidal modulo indexing to check across boundaries
        north_idx = (current_idx_y + 1) % self.grid_size
        south_idx = (current_idx_y - 1) % self.grid_size
        east_idx  = (current_idx_x + 1) % self.grid_size
        west_idx  = (current_idx_x - 1) % self.grid_size
        
        # Read the elevation stress fields at the neighboring nodes
        tension_n = self.topographic_torus_map[current_idx_x, north_idx]
        tension_s = self.topographic_torus_map[current_idx_x, south_idx]
        tension_e = self.topographic_torus_map[east_idx, current_idx_y]
        tension_w = self.topographic_torus_map[west_idx, current_idx_y]
        
        # Net differential tension vector acting on the physical node
        net_tension_x = tension_e - tension_w
        net_tension_y = tension_n - tension_s
        
        return net_tension_x, net_tension_y
