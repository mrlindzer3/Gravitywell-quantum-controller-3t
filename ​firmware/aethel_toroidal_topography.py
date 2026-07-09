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

import numpy as np

class AethelTernaryTensegrityTopographyEngine:
    def __init__(self, num_nodes=1024):
        self.num_nodes = num_nodes
        
        # 1. TERNARY: States mapped to -1 (Repulsion), 0 (Neutral), +1 (Attraction)
        self.ternary_state_register = np.zeros(num_nodes, dtype=int)
        
        # 2. TENSEGRITY: Virtual spring-tension network configuration matrix
        self.tension_network_matrix = np.eye(num_nodes) * 1.0
        
        # 3. TOPOGRAPHY: Elevation mapping profile matrix (Z-axis light metrics)
        self.topographic_relief_map = np.zeros((32, 32))

    def evaluate_ternary_logic(self, raw_input_currents):
        """Processes sensor data into clean -1, 0, or +1 states."""
        # Express logic thresholds cleanly using Ternary parameters
        self.ternary_state_register = np.where(raw_input_currents > 1.5, 1, 
                                      np.where(raw_input_currents < -1.5, -1, 0))
        return self.ternary_state_register

    def calculate_tensegrity_balance(self, applied_force_vector):
        """Balances localized node adjustments across the continuous tension framework."""
        # Distribute kinetic stress evenly across the continuous network
        balanced_tension_response = np.dot(self.tension_network_matrix, applied_force_vector)
        return balanced_tension_response

    def deform_topographic_landscape(self, target_x, target_y, well_depth):
        """Alters the physical topography of the optical landscape."""
        # Convert raw coordinate tracks into a 2D topographic grid elevation layer
        grid_x = int(clip((target_x + 1) * 15.5, 0, 31))
        grid_y = int(clip((target_y + 1) * 15.5, 0, 31))
        
        # Carve a physical valley (potential minimum) into the topography map
        self.topographic_relief_map[grid_x, grid_y] = -well_depth

def clip(val, low, high):
    return max(low, min(val, high))

