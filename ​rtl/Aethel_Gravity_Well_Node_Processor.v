// =========================================================================
// Company/Project: Aethel Quantum Hardware Systems
// Module Name:    Aethel_Gravity_Well_Node_Processor
// Description:    Hardware RTL engine executing real-time stabilization
//                 and conformal metric scaling for a single potential well.
// =========================================================================

module Aethel_Gravity_Well_Node_Processor (
    input  wire        clk,                  // Master System Clock
    input  wire        rst_n,                // Active-Low Hardware Reset
    input  wire [15:0] apd_input_current,    // 16-bit Fixed-Point APD Sensing Input (Q8.8 format)
    input  wire [15:0] static_metric_scale,  // Pre-calculated Hyperbolic Scaling Factor from ROM (Q8.8)
    output reg  [15:0] micro_led_drive_v     // 16-bit Fixed-Point Voltage Drive Output to LED (Q8.8)
);

    // Internal Fixed-Point Control Parameters (Q8.8 Format)
    // Kp = 15.5 (16'h0F80), Kd = 2.25 (16'h0240)
    localparam signed [15:0] KP_GAIN = 16'h0F80;
    localparam signed [15:0] KD_GAIN = 16'h0240;

    // Internal Hardware Registers
    reg signed [15:0] prev_error;
    reg signed [31:0] intermediate_product;

    // Typecast inputs to signed values natively for clean hardware arithmetic
    wire signed [15:0] signed_apd_input    = apd_input_current;
    wire signed [15:0] signed_metric_scale = static_metric_scale;

    // Wire declarations for internal arithmetic
    wire signed [15:0] current_error;
    wire signed [15:0] derivative;
    wire signed [15:0] raw_stabilization;

    // Invert sensing input to derive positional deviation from focal center
    assign current_error = -signed_apd_input;
    assign derivative    = current_error - prev_error;
    
    // Proportional-Derivative (PD) Correction Matrix Step
    assign raw_stabilization = (current_error * KP_GAIN) + (derivative * KD_GAIN);

    // Synchronous Register-Transfer Logic
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            prev_error            <= 16'h0000;
            intermediate_product  <= 32'h00000000;
            micro_led_drive_v     <= 16'h0000;
        end else begin
            // Store baseline error for the derivative calculation of the next cycle
            prev_error <= current_error;

            // Physical Curvature Mapping: Multiply PD drive by the static hyperbolic conformal factor
            intermediate_product <= raw_stabilization * signed_metric_scale;

            // Hardware Saturation and Clipping Layer [0.0V to 5.0V]
            // Prevents register overflow and limits peak voltage to the Micro-LED film
            if (intermediate_product[31] == 1'b1) begin
                // Negative voltage correction clipped to absolute 0V ground floor
                micro_led_drive_v <= 16'h0000;
            end else if (intermediate_product[23:8] > 16'h0500) begin
                // Voltage caps precisely at 5.0V (16'h0500 in Q8.8) to protect GaN junctions
                micro_led_drive_v <= 16'h0500;
            end else begin
                // Pass the bit-shifted fixed-point slice safely to the output register
                micro_led_drive_v <= intermediate_product[23:8];
            end
        end
    end

endmodule
