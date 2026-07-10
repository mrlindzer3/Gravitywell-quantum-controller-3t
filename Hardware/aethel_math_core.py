# ──────────────────────────────────────────────────────────────────────────
# FILE: hardware/aethel_math_core.py
# ROLE: Mathematical Invariant Engine (Hamiltonian Linearizer & Symplectic V)
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging
from typing import Dict, Any, Tuple

logger = logging.getLogger("AethelMathCore")

class AethelMathCore:
    def __init__(self, hbar: float = 1.0):
        """
        Executes exact numerical evaluations for the optomechanical radiation 
        pressure Hamiltonians and Symplectic covariance matrices.
        """
        self.hbar = hbar

    def compute_linearized_eigenfrequencies(self, delta_0: float, omega_m: float, coupling_G: float) -> Tuple[complex, complex]:
        """
        [Domain 81: The Optomechanical Cavity Splitting Hamiltonian]
        Solves the characteristic equation for the coupled optomechanical system matrix 
        to find the hybrid optical-mechanical eigenmodes.
        """
        # System drift matrix M for the linearized fluctuations (dx, dp, dX, dP)
        system_matrix = np.array([
            [0,       omega_m,   0,          0],
            [-omega_m, 0,         2*coupling_G, 0],
            [0,       0,         0,          delta_0],
            [2*coupling_G, 0,    -delta_0,   0]
        ], dtype=np.float64)
        
        eigenvalues = np.linalg.eigvals(system_matrix)
        # Sort by imaginary component to isolate the primary split modes
        sorted_eigenvals = eigenvalues[np.argsort(np.abs(eigenvalues.imag))]
        
        logger.info(f"🧮 MATH: Linearized system matrix diagonalized. Split mode frequencies: {sorted_eigenvals[0]:.4f}, {sorted_eigenvals[2]:.4f}")
        return (sorted_eigenvals[0], sorted_eigenvals[2])

    def verify_symplectic_uncertainty_relation(self, covariance_matrix: np.ndarray) -> Tuple[bool, float]:
        """
        [Domain 82: Continuous-Variable Symplectic Geometry]
        Verifies compliance with the generalized uncertainty principle: V + (i/2)*Omega >= 0
        """
        num_modes = covariance_matrix.shape[0] // 2
        
        # Build the Symplectic Matrix Omega
        omega = np.zeros_like(covariance_matrix, dtype=np.complex128)
        for i in range(num_modes):
            omega[2*i, 2*i+1] = 1.0
            omega[2*i+1, 2*i] = -1.0
            
        # Evaluate the uncertainty matrix eigenvalue spectrum
        uncertainty_matrix = covariance_matrix.astype(np.complex128) + (1j * 0.5 * self.hbar) * omega
        min_eigenval = float(np.real(np.min(np.linalg.eigvals(uncertainty_matrix))))
        
        is_physically_valid = min_eigenval >= -1e-7
        if is_physically_valid:
            logger.info(f"✅ MATH: Symplectic Heisenberg relation verified. Minimum uncertainty eigenvalue: {min_eigenval:.6f}")
        else:
            logger.error(f"❌ MATH: Symplectic violation detected! Unphysical state representation (Eigenvalue: {min_eigenval:.6f})")
            
        return is_physically_valid, min_eigenval
