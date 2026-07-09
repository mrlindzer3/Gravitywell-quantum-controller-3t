import numpy as np

class AethelAdvancedMeshHILEngine:
    def __init__(self, mesh_rows=2, mesh_cols=2, torus_grid_size=16):
        self.mesh_rows = mesh_rows
        self.mesh_cols = mesh_cols
        self.grid_size = torus_grid_size
        
        # 1. TESSELLATED MESH: A grid of independent but interconnected toroidal fields
        self.mesh_topology = np.zeros((mesh_rows, mesh_cols, torus_grid_size, torus_grid_size))
        
        # 2. HIL DEGRADATION: Track health metrics (1.0 = perfect, 0.0 = completely dead)
        # Models mirror degradation or laser emitter fading across the physical surface
        self.hardware_health_matrix = np.ones((mesh_rows, mesh_cols, torus_grid_size, torus_grid_size))

    def map_global_coordinates_to_tessellation(self, x, y):
        """
        Translates global coordinates across the entire tessellated surface,
        routing particles seamlessly from one torus to an adjacent neighbor.
        """
        # Periodic boundaries wrap coordinates across the entire multi-torus macro-mesh
        gx = x % float(self.mesh_cols)
        gy = y % float(self.mesh_rows)
        
        col_idx = int(gx)
        row_idx = int(gy)
        
        # Local relative coordinates inside the targeted torus unit
        local_x = int((gx - col_idx) * (self.grid_size - 1))
        local_y = int((gy - row_idx) * (self.grid_size - 1))
        
        return row_idx, col_idx, local_x, local_y

    def inject_hardware_fault(self, row, col, local_x, local_y, degradation_factor=0.8):
        """[HIL EMULATION] Simulates physical hardware degradation at a specific pin."""
        current_health = self.hardware_health_matrix[row, col, local_x, local_y]
        self.hardware_health_matrix[row, col, local_x, local_y] = max(0.0, current_health - degradation_factor)

    def calculate_adaptive_tensegrity_field(self, x, y, base_tension):
        """
        [ADAPTIVE TENSEGRITY] 
        Calculates localized structural tension. If the HIL emulation flags hardware 
        degradation, the tensegrity network compensates by pulling load onto healthy nodes.
        """
        r, c, lx, ly = self.map_global_coordinates_to_tessellation(x, y)
        
        # Read the structural hardware health at this node
        node_health = self.hardware_health_matrix[r, c, lx, ly]
        
        if node_health < 1.0:
            # Hardware-in-the-loop adaptation protocol:
            # Amplify adjacent tension fields to offset the failing node's weak potential well
            adapted_tension = base_tension * (2.0 - node_health)
            status = f"[ADAPT] Node ({r},{c})[{lx},{ly}] degraded to {node_health:.2f}. Tensegrity amplified."
        else:
            adapted_tension = base_tension
            status = "[NOMINAL] Grid functioning at optimal efficiency bounds."
            
        return adapted_tension, status
