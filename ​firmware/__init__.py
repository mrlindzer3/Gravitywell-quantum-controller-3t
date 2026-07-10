 ──────────────────────────────────────────────────────────────────────────
# FILE: firmware/__init__.py
# SYSTEM: Solid-State Neuromorphic Quantum Optomechanics Substrate Core
# SPECIFICATION: System Package Initialization, Type Registry & Validation Layer
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

"""
Aethel Core Firmware Initialization Subsystem.

This package orchestrates the low-level mathematical operations, boundary
wrapping routines, and physical voltage translation matrices required to 
drive the 3-Tier Vertically Integrated Monolithic Substrate.

Core Architecture Mappings:
    Tier 1 (Base): Memristor Crossbar Array [Analog Compute Core]
    Tier 2 (Mid):  Avalanche Photodiode (APD) Matrix [Low-Latency Sensing]
    Tier 3 (Top):  Gallium Nitride (GaN) Micro-LED Array [Phase Actuation]
"""

import sys
import logging
from typing import Tuple, Dict, Any, Union
from .aethel_3d_torus_engine import Aethel3DTorusEngine
from .aethel_trajectory_generator import AethelTrajectoryGenerator
from .aethel_gravity_well_controller import AethelGravityWellController
from .aethel_hardware_driver import AethelHardwareDriver  # Add this linefrom .aethel_3d_torus_engine import Aethel3DTorusEngine
from .aethel_trajectory_generator import AethelTrajectoryGenerator
from .aethel_gravity_well_controller import AethelGravityWellController
from .aethel_hardware_driver import AethelHardwareDriver
from .aethel_topography_firmware import AethelTopographyFirmware
from .aethel_thermodynamic_recycler import AethelThermodynamicRecycler  # Add this line
from .aethel_wavefront_calibrator import AethelWavefrontCalibrator
from hardware.aethel_diagnostics_logger import AethelDiagnosticsLogger
from .aethel_predictive_controller import AethelPredictiveController
from .aethel_manifold_controller import AethelManifoldController
from .aethel_boundary_controller import AethelBoundaryController
from .aethel_alignment_controller import AethelAlignmentController
from .aethel_synaptic_controller import AethelSynapticController
from .aethel_routing_controller import AethelRoutingController
from .aethel_clock_controller import AethelClockController
from .aethel_failover_controller import AethelFailoverController
from .aethel_state_controller import AethelStateController
from .aethel_braid_optimizer import AethelBraidOptimizer
from .aethel_metric_compiler import AethelMetricCompiler
from .aethel_fusion_compiler import AethelFusionCompiler
from .aethel_functor_compiler import AethelFunctorCompiler
from hardware.aethel_layout_verifier import AethelLayoutVerifier
from hardware.aethel_mask_optimizer import AethelMaskOptimizer
from hardware.aethel_photonic_controller.py import AethelPhotonicController
from hardware.aethel_plasmonic_controller import AethelPlasmonicController
from hardware.aethel_edge_controller import AethelEdgeController
from hardware.aethel_cluster_fabric import AethelClusterFabric
from hardware.aethel_optomechanics_controller import AethelOptomechanicsController
from hardware.aethel_quantum_shuttler import AethelQuantumShuttler
from hardware.aethel_quantum_gates import AethelQuantumGates
from hardware.aethel_quantum_telemetry import AethelQuantumTelemetry
from hardware.aethel_cluster_mbqc import AethelClusterMBQC
from hardware.aethel_qec_fabric import AethelQECFabric
from hardware.aethel_automaton import AethelAutomaton
from hardware.aethel_tensor_compiler import AethelTensorCompiler
from hardware.aethel_math_core import AethelMathCore


# Enforce clean numerical array handling dependencies across the stack
try:
    import numpy as np
except ImportError:
    raise ImportError(
        "Critical Dependency Error: NumPy is required to process the "
        "Multilinear Tensor Contraction core matrix."
    )

# ── EXPOSE CORE INTERFACES TO THE ECOSYSTEM ──────────────────────────────
from .aethel_3d_torus_engine import Aethel3DTorusEngine
from .aethel_trajectory_generator import AethelTrajectoryGenerator
from .aethel_gravity_well_controller import AethelGravityWellController

__all__ = [
    'Aethel3DTorusEngine',
    'AethelTrajectoryGenerator',
    'AethelGravityWellController',
    'verify_firmware_stack_integrity',
    'FirmwarePackageRegistry'
]

# ── SYSTEM VERSIONING & REGISTRY STATE MANIFEST ──────────────────────────
__version__ = "3.1.0"
__author__ = "Ryan Taylor Lindsey"

# Configure package-level diagnostic log streams
logging.basicConfig(level=logging.INFO, format="[AETHEL-FW-SYS] %(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("AethelFirmware")


class FirmwarePackageRegistry:
    """
    Maintains a runtime footprint registry of the hardware-software co-design
    dimensions to prevent memory overflow during tensor contraction loops.
    """
    def __init__(self):
        self._expected_dimensions: int = 16
        self._target_clock_mhz: float = 200.0
        self._manifold_topology: str = "3-Torus (S¹ x S¹ x S¹)"
        self._voltage_domain_max: float = 3.3
        
    @property
    def system_configuration(self) -> Dict[str, Any]:
        """Returns structural bounds matching the hardware rtl design criteria."""
        return {
            "Lattice_Grid_Resolution": self._expected_dimensions,
            "Target_FPGA_Clock_MHz": self._target_clock_mhz,
            "Manifold_Geometry": self._manifold_topology,
            "Max_GaN_Driving_Voltage": self._voltage_domain_max,
            "Engine_Version": __version__
        }


def verify_firmware_stack_integrity(grid_resolution: int = 16) -> bool:
    """
    Executes a pre-flight sanity check and self-test across the deployed 
    firmware modules before allowing main.py or physical HIL lines to run.
    """
    logger.info("Initializing system validation sweeps on local firmware architecture...")
    
    try:
        # 1. Test Math & Engine Initialization Topology
        engine = Aethel3DTorusEngine(grid_size=grid_resolution)
        if engine.grid_size != grid_resolution:
            logger.error("Grid scaling discrepancy intercepted in Aethel3DTorusEngine.")
            return False
            
        # Verify 3D array memory allocation footprint matches standard requirements
        if engine.topographic_volume_map.shape != (grid_resolution, grid_resolution, grid_resolution):
            logger.error("3D Volumetric Tensor allocation failed verification checks.")
            return False
            
        # 2. Test 3-Torus Boundary Periodic Wrapping Modulo Logic
        test_coords = [1.1, -0.1, 0.5]
        wrapped_idx = engine.map_coordinates_to_3d_torus(test_coords[0], test_coords[1], test_coords[2])
        
        # Upper boundary check (1.1 % 1.0 = 0.1 -> index mapping)
        expected_x_idx = int((1.1 % 1.0) * (grid_resolution - 1))
        if wrapped_idx[0] != expected_x_idx:
            logger.error("T³ periodic manifold wrapping constraint failure detected on X-axis.")
            return False
            
        # 3. Test Kinematic Integration Mechanics
        generator = AethelTrajectoryGenerator(step_size=0.05)
        next_pos = generator.compute_next_step((0.99, 0.5, 0.5), (1.0, 0.0, 0.0))
        
        # Confirm that the kinematics module properly wraps boundaries in tandem
        if not (0.0 <= next_pos[0] < 1.0):
            logger.error("Kinematic trajectory generator leaked outside the continuous 3-Torus manifold bounds.")
            return False
            
        # 4. Test Voltage Mapping and Thermal Overdrive Protections
        controller = AethelGravityWellController(channels=grid_resolution, max_voltage=3.3)
        mock_slice = np.ones((grid_resolution, grid_resolution)) * 5.0  # Force over-saturated field input
        calculated_voltages = controller.translate_field_to_voltages(mock_slice)
        
        # Ensure voltage clamps prevent hard physical degradation on Tier 3 GaN emitters
        if np.any(calculated_voltages > controller.max_voltage):
            logger.error("Voltage modulation clamp violation. Hard saturation clip failed.")
            return False
            
        # 5. Check Multilinear Tensor Contraction Channel Mapping
        # Ingest a standard test coordinate to confirm ramanujan vectors converge properly
        v_x, v_y, v_z, anomaly = engine.calculate_tensored_ramanujan_godel_lagrangian(0.5, 0.5, 0.5, particle_mass=1.0)
        if np.isnan(v_x) or np.isnan(v_y) or np.isnan(v_z):
            logger.error("Multilinear Tensor Contraction output returned an indeterminate NaN trace.")
            return False
            
    except Exception as exc:
        logger.critical(f"Fatal Hardware-Software Co-Design Simulation Exception caught during init trace: {str(exc)}")
        return False
        
    logger.info("✅ All core firmware components verified. Environmental state secure.")
    return True

# ── PACKAGE AUTO-EXECUTION ROUTINE ───────────────────────────────────────
# Instantly check environment state upon framework deployment initialization
_registry = FirmwarePackageRegistry()
_integrity_passed = verify_firmware_stack_integrity(_registry.system_configuration["Lattice_Grid_Resolution"])

if not _integrity_passed:
    sys.stderr.write("[CRITICAL INITIALIZATION ERROR] Aethel Firmware package sanity checks failed.\n")
    # We log the warning but don't force a hard kill to ensure that testing frameworks
    # can run static code analysis sweeps without breaking live builds.
else:
    logger.info(f"System Paradigms Active: Mapped on {_registry.system_configuration['Manifold_Geometry']}")
#
# Append these tracking modules if they aren't already explicitly imported
from .aethel_hardware_driver import AethelHardwareDriver
from .aethel_topography_firmware import AethelTopographyFirmware
from .aethel_thermodynamic_recycler import AethelThermodynamicRecycler
from .aethel_cluster_monitor import AethelClusterMonitor
from .aethel_graph_compiler import AethelGraphCompiler
from hardware.aethel_diagnostics_logger import AethelDiagnosticsLogger
 ──────────────────────────────────────────────────────────────────────────
──────────────────────────────────────────────────────────
