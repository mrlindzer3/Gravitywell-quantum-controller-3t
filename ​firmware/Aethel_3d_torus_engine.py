import numpy as np

class Aethel3DTorusEngine:
    def __init__(self, grid_size=16):
        self.grid_size = grid_size
        
        # 1. 3D STATE REGISTERS
        self.ternary_volume_register = np.zeros((grid_size, grid_size, grid_size), dtype=int)
        self.topographic_volume_map = np.zeros((grid_size, grid_size, grid_size))
        
        # 2. EINSTEIN-FRESNEL REFRACTION MATRIX
        # Tracks phase distortion zones emanating from the center of the grid
        self.fresnel_phase_matrix = np.zeros((grid_size, grid_size, grid_size))

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

    def relax_3d_field_potentials(self, iterations=3, diffusion_factor=0.15):
        """Applies a discrete 3D Laplace finite-difference relaxation sweep."""
        for _ in range(iterations):
            east  = np.roll(self.topographic_volume_map, shift=-1, axis=0)
            west  = np.roll(self.topographic_volume_map, shift=1,  axis=0)
            north = np.roll(self.topographic_volume_map, shift=-1, axis=1)
            south = np.roll(self.topographic_volume_map, shift=1,  axis=1)
            front = np.roll(self.topographic_volume_map, shift=-1, axis=2)
            back  = np.roll(self.topographic_volume_map, shift=1,  axis=2)
            
            neighbor_average = (east + west + north + south + front + back) / 6.0
            self.topographic_volume_map = (1.0 - diffusion_factor) * self.topographic_volume_map + diffusion_factor * neighbor_average

    def compute_einstein_fresnel_lens(self, center_x=0.5, center_y=0.5, center_z=0.5, wavelength=0.05):
        """
        [THE EINSTEIN-FRESNEL ALGORITHM]
        Calculates concentric phase refraction zones. Combines gravitational 
        field warping (Einstein) with concentric phase ring zoning (Fresnel)
        to calculate localized spatial focal points.
        """
        # Create relative spatial coordinate steps across the 3D grid dimensions
        u = np.linspace(-0.5, 0.5, self.grid_size)
        x_net, y_net, z_net = np.meshgrid(u, u, u, indexing='ij')
        
        # Calculate true radial Euclidean distance from the lens focal center
        r_squared = (x_net - (center_x - 0.5))**2 + (y_net - (center_y - 0.5))**2 + (z_net - (center_z - 0.5))**2
        distance = np.sqrt(r_squared) + 1e-9 # Prevent divide-by-zero
        
        # 1. Einstein Gravitational Lensing effect (Refractive deflection scale)
        # Deep potential wells dramatically twist local spatial grid pathways
        gravitational_warp = np.abs(self.topographic_volume_map) * 2.0
        
        # 2. Fresnel Zone phase calculation (Modulo wave cycles)
        # Zones space into phase steps: 2*pi * (r^2 / wavelength) modified by the spatial warp
        raw_phase = (2.0 * np.pi * (r_squared / wavelength)) * (1.0 + gravitational_warp)
        
        # Bound the phase between 0 and 2*pi to simulate physical refractive ring steps
        self.fresnel_phase_matrix = raw_phase % (2.0 * np.pi)
        
        return self.fresnel_phase_matrix

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
