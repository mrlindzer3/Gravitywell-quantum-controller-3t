# ──────────────────────────────────────────────────────────────────────────
# FILE: firmware/aethel_predictive_controller.py
# ROLE: Multi-Axis Predictive Trajectory & Thermal Gradient Controller
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging
from typing import Tuple, Dict

logger = logging.getLogger("AethelController")

class AethelPredictiveController:
    def __init__(self, Kp: float = 0.6, Ki: float = 0.1, Kd: float = 0.2):
        """
        Advanced feedback and feed-forward controller to stabilize physical 
        qubit trajectories and balance cross-layer substrate thermal loads.
        """
        # PID Controller Parameters for spatial stabilization
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        
        # Error accumulation registers
        self.integral_error = np.zeros(3)
        self.previous_error = np.zeros(3)
        
        # Max safe operating temperature delta (Kelvin) before throttling triggers
        self.max_safe_delta_t = 45.0

    def compute_predictive_actuation_vectors(self, current_pos: Tuple[float, float, float], 
                                              target_pos: Tuple[float, float, float], 
                                              velocity: Tuple[float, float, float], 
                                              dt: float = 0.005) -> np.ndarray:
        """
        [Domain 19: Predictive Trajectory Controllers]
        Calculates the required physical voltage adjustment vector using a PID loop 
        augmented with a velocity feed-forward trajectory estimator.
        """
        current_arr = np.array(current_pos)
        target_arr = np.array(target_pos)
        vel_arr = np.array(velocity)
        
        # 1. Feed-Forward Estimator: Predict upcoming position drop-in
        predicted_pos = current_arr + (vel_arr * dt)
        
        # 2. Compute spatial error vectors against target
        error = target_arr - predicted_pos
        self.integral_error += error * dt
        derivative_error = (error - self.previous_error) / dt
        
        # 3. Calculate unified control output response
        pid_output = (self.Kp * error) + (self.Ki * self.integral_error) + (self.Kd * derivative_error)
        
        # Preserve error tracking for the next sequence tick
        self.previous_error = error
        return pid_output

    def regulate_substrate_thermal_loads(self, tier1_temp: float, tier3_temp: float) -> Dict[str, Any]:
        """
        [Domain 20: Thermal Gradient Regulators]
        Monitors cross-layer thermal differentials and issues throttling directives
        to preserve spatial optical alignment across the metamaterial cavity.
        """
        delta_t = abs(tier3_temp - tier1_temp)
        throttle_active = delta_t > self.max_safe_delta_t
        
        # Calculate dynamic scaling factor for local Event-Driven PLL clocks
        # Throttles down local clock frequencies if thermal bounds are broken
        clock_frequency_scale = 1.0
        if throttle_active:
            overshoot = delta_t - self.max_safe_delta_t
            clock_frequency_scale = max(0.2, 1.0 - (overshoot * 0.02))
            logger.warning(f"⚠️ THERMAL MITIGATION ACTIVE: Delta T at {delta_t:.2f}K. Throttling local sector clock down to {clock_frequency_scale * 100:.1f}%.")
            
        return {
            "temperature_gradient_k": delta_t,
            "thermal_throttling_engaged": throttle_active,
            "target_clock_scale": clock_frequency_scale
        }
