// =========================================================================
// Company/Project: Aethel Quantum Hardware Systems
// Module Name:    Aethel_Neural_Warp_Coprocessor
// Description:    Hardware neural accelerator processing predictive 
//                 drift corrections via direct register weighting.
// =========================================================================

module Aethel_Neural_Warp_Coprocessor (
    input  wire        clk,                  // Master System Clock
    input  wire        rst_n,                // Active-Low Hardware Reset
    input  wire [15:0] live_error_input,     // Real-time error from sensor node (Q8.8)
    input  wire [15:0] neural_weight_bias,   // Synaptic weight value from memristor crossbar (Q8.8)
    output reg  [15:0] predictive_warp_out   // Pre-emptive voltage bias offset to scale engine
);

    // Internal pipeline registers
    reg signed [31:0] raw_matrix_product;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            raw_matrix_product  <= 32'h00000000;
            predictive_warp_out <= 16'h0000;
        end else begin
            // Instantaneous physical scalar multiplication mimicking a neuromorphic synapse
            raw_matrix_product <= $signed(live_error_input) * $signed(neural_weight_bias);

            // Shift and pass the predictive bias vector out to the main LED control line
            // Caps the neural warp factor to a strict window to prevent overdrive loop errors
            if (raw_matrix_product[31] == 1'b1) begin
                predictive_warp_out <= 16'h0000; // Floor clamp
            end else if (raw_matrix_product[23:8] > 16'h0100) begin
                predictive_warp_out <= 16'h0100; // Cap predictive adjustments at 1.0V max bias
            end else begin
                predictive_warp_out <= raw_matrix_product[23:8];
            end
        end
    end

endmodule
