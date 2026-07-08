# Module: `rtl/Aethel_Hardware_Constraints.xdc`
### Physical Pin-Mapping Constraints File for COTS FPGA Implementation

```hardware
# =========================================================================
# Project: Aethel Quantum Hardware Systems 3T Control Core
# Target Device: Xilinx Zynq UltraScale+ (xczu9eg-ffvb1156-2-e)
# File Type: Vivado Design Constraints (.xdc)
# =========================================================================

# Global Clock Configuration (200 MHz System Reference Oscillation)
set_property PACKAGE_PIN AN14 [get_ports clk]
set_property IOSTANDARD LVCMOS18 [get_ports clk]
create_clock -period 5.000 -name sys_clk [get_ports clk]

# System Hardware Reset Line (Active Low Switch mapping)
set_property PACKAGE_PIN AM13 [get_ports rst_n]
set_property IOSTANDARD LVCMOS18 [get_ports rst_n]

# 16-Bit Parallel Micro-LED Driver Core Output (Pins mapping to High-Speed Bank 45)
set_property PACKAGE_PIN AP12 [get_ports {micro_led_drive_v[0]}]
set_property PACKAGE_PIN AN12 [get_ports {micro_led_drive_v[1]}]
set_property PACKAGE_PIN AM12 [get_ports {micro_led_drive_v[2]}]
set_property PACKAGE_PIN AL12 [get_ports {micro_led_drive_v[3]}]
set_property PACKAGE_PIN AK12 [get_ports {micro_led_drive_v[4]}]
set_property PACKAGE_PIN AJ12 [get_ports {micro_led_drive_v[5]}]
set_property PACKAGE_PIN AH12 [get_ports {micro_led_drive_v[6]}]
set_property PACKAGE_PIN AG12 [get_ports {micro_led_drive_v[7]}]
set_property PACKAGE_PIN AF12 [get_ports {micro_led_drive_v[8]}]
set_property PACKAGE_PIN AE12 [get_ports {micro_led_drive_v[9]}]
set_property PACKAGE_PIN AD12 [get_ports {micro_led_drive_v[10]}]
set_property PACKAGE_PIN AC12 [get_ports {micro_led_drive_v[11]}]
set_property PACKAGE_PIN AB12 [get_ports {micro_led_drive_v[12]}]
set_property PACKAGE_PIN AA12 [get_ports {micro_led_drive_v[13]}]
set_property PACKAGE_PIN Y12  [get_ports {micro_led_drive_v[14]}]
set_property PACKAGE_PIN W12  [get_ports {micro_led_drive_v[15]}]
set_property IOSTANDARD LVCMOS18 [get_ports {micro_led_drive_v[*]}]

# Optimization Constraints Configuration
set_max_delay -from [get_ports apd_input_current[*]] -to [get_ports micro_led_drive_v[*]] 4.500
set_operating_conditions -ambient_temp 25.0
```
