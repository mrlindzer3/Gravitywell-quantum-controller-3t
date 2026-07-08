// =========================================================================
// Company/Project: Aethel Quantum Hardware Systems
// Module Name:    Aethel_Gravity_Well_Node_Processor_TB
// Description:    Behavioral Testbench verifying fixed-point scaling,
//                 proportional-derivative logic, and voltage clipping.
// =========================================================================

`timescale 1ns / 1ps

module Aethel_Gravity_Well_Node_Processor_TB;

    // Testbench Signals
    reg         clk;
    reg         rst_n;
    reg  [15:0] test_apd_input;
    reg  [15:0] test_metric_scale;
    wire [15:0] led_output_voltage;

    // Instantiate the Unit Under Test (UUT)
    Aethel_Gravity_Well_Node_Processor uut (
        .clk(clk),
        .rst_n(rst_n),
        .apd_input_current(test_apd_input),
        .static_metric_scale(test_metric_scale),
        .micro_led_drive_v(led_output_voltage)
    );

    // Clock Generation (50MHz system clock simulation)
    always #10 clk = ~clk;

    initial begin
        // Initialize Core Signals
        clk = 0;
        rst_n = 0;
        test_apd_input = 16'h0000;
        test_metric_scale = 16'h0100; // Unity scale factor (1.0 in Q8.8)

        #20;
        rst_n = 1; // Release Hardware Reset
        
        // --- Test Case 1: Standard Proportional Alignment Response ---
        // Simulating a minor positive positional particle drift
        #20;
        test_apd_input = 16'h0010; // Nominal input signal
        
        // --- Test Case 2: Boundary Underflow Saturation ---
        // Forcing a negative calculation boundary to check 0.0V ground clamp
        #40;
        test_apd_input = 16'h7FFF; // Force extreme positive input saturation

        // --- Test Case 3: Poincaré Boundary Overdrive Protection ---
        // Simulating particle near disk perimeter with high metric scaling factor
        #40;
        test_apd_input = 16'hFF00; // High reverse sensor deflection
        test_metric_scale = 16'h0A00; // Hyperbolic scale factor multiplier of 10.0

        #40;
        $display("Simulation complete. Verify that output limits conform to 0x0000 and 0x0500 constraints.");
        $finish;
    end

endmodule
