import numpy as np

class AethelGravityWellController:
    def __init__(self, channels=16, max_voltage=3.3):
        """
        Manages the high-gradient voltage scaling to modulate Tier 3 GaN Micro-LED
        arrays, mirroring the macro configurations of aethel_gravitywell-processor.v.
        """
        self.channels = channels
        self.max_voltage = max_voltage
        # Baseline drive registers for the optical trapping matrix
        self.voltage_registers = np.zeros((channels, channels))

    def translate_field_to_voltages(self, potential_slice):
        """
        Maps a 2D slice of the 3D topographic potential map directly to physical 
        voltage values. Higher field densities map to higher drive currents to 
        deepen the optical gravity wells.
        """
        # Resample or slice the input potential map to match the hardware controller dimensions
        scaled_potentials = np.abs(potential_slice)
        max_pot = np.max(scaled_potentials) if np.max(scaled_potentials) > 0 else 1.0
        
        # Normalize potential values and map to the hardware operating voltage (e.g., 0V to 3.3V)
        normalized_map = scaled_potentials / max_pot
        self.voltage_registers = normalized_map * self.max_voltage
        
        return self.voltage_registers

    def generate_fresnel_pwm_vectors(self, phase_matrix_slice):
        """
        Converts the Einstein-Fresnel phase refraction matrix ($0$ to $2\pi$) 
        into discrete Pulse-Width Modulation (PWM) duty cycle percentages. 
        These vectors feed directly into the FPGA pins mapped in aethel_pins.xdc.
        """
        # Map phase angles seamlessly from 0 - 2pi to a 0% - 100% duty cycle
        pwm_duty_cycles = (phase_matrix_slice / (2.0 * np.pi)) * 100.0
        # Clip boundaries to protect physical GaN emitters from thermal overdrive
        return np.clip(pwm_duty_cycles, 0.0, 100.0)
