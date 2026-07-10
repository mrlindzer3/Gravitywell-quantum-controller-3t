# ──────────────────────────────────────────────────────────────────────────
# FILE: hardware/aethel_pins.xdc
# DESIGN: Aethel Solid-State Neuromorphic Quantum Optomechanical Core
# TARGET BOARD: AMD/Xilinx UltraScale+ / Custom ASIC Emulation Platform
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

## SYSTEM CLOCK MANAGEMENT (200 MHz Reference Oscillator)
set_property PACKAGE_PIN AK17 [get_ports clk]
set_property IOSTANDARD LVCMOS33 [get_ports clk]
create_clock -period 5.000 -name sys_clk_pin -waveform {0.000 2.500} -add [get_ports clk]

## SYSTEM RESET
set_property PACKAGE_PIN AN16 [get_ports rst_n]
set_property IOSTANDARD LVCMOS33 [get_ports rst_n]

## TIER 2: AVALANCHE PHOTODIODE (APD) OPTICAL TELEMETRY BUS (High-Speed Input Differential signaling)
# Node [0,0,0] Ternary State Input Pins
set_property PACKAGE_PIN AM19 [get_ports {local_ternary_state[0]}]
set_property IOSTANDARD LVCMOS33 [get_ports {local_ternary_state[0]}]
set_property PACKAGE_PIN AM20 [get_ports {local_ternary_state[1]}]
set_property IOSTANDARD LVCMOS33 [get_ports {local_ternary_state[1]}]

# Neighbor [1,0,0] Interconnect Pass-Through Logic Input Pins
set_property PACKAGE_PIN AP21 [get_ports {neighbor_ternary_state[0]}]
set_property IOSTANDARD LVCMOS33 [get_ports {neighbor_ternary_state[0]}]
set_property PACKAGE_PIN AP22 [get_ports {neighbor_ternary_state[1]}]
set_property IOSTANDARD LVCMOS33 [get_ports {neighbor_ternary_state[1]}]

## TIER 3: GALLIUM NITRIDE (GaN) MICRO-LED WAVEFRONT ACTUATOR BUS (Outputs)
# Resolved Velocity Driving Channels (Pulse-Width Modulation Phase Vectors)
set_property PACKAGE_PIN BA20 [get_ports {resolved_velocity_x[0]}]
set_property IOSTANDARD LVCMOS33 [get_ports {resolved_velocity_x[0]}]
set_property PACKAGE_PIN BB20 [get_ports {resolved_velocity_x[1]}]
set_property IOSTANDARD LVCMOS33 [get_ports {resolved_velocity_x[1]}]
set_property PACKAGE_PIN BC21 [get_ports {resolved_velocity_x[2]}]
set_property IOSTANDARD LVCMOS33 [get_ports {resolved_velocity_x[2]}]
set_property PACKAGE_PIN BD21 [get_ports {resolved_velocity_x[3]}]
set_property IOSTANDARD LVCMOS33 [get_ports {resolved_velocity_x[3]}]

## PARADIGM GÖDEL LOGIC CRITICAL ALERTS (Hardware Intercept Interrupt)
set_property PACKAGE_PIN AL18 [get_ports godel_anomaly_alert]
set_property IOSTANDARD LVCMOS33 [get_ports godel_anomaly_alert]
set_property DRIVE 12 [get_ports godel_anomaly_alert]

## TIMING & PLACEMENT OPTIMIZATION STRATEGY
# Enforce low-skew global clock routing buffers for internal multilinear contraction matrix
set_property BUFFER_TYPE BUFG [get_signals clk]
set_property MAX_FANOUT 500 [get_cells -hierarchical *]
