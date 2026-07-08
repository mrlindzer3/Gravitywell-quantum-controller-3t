// =========================================================================
// Company/Project: Aethel Quantum Hardware Systems
// Module Name:    Aethel_Tile_Interconnect_Bridge
// Description:    North-South-East-West (NSEW) Edge Interface routing boundary 
//                 qubit coordinates across a multi-tile optoelectronic array.
// =========================================================================

module Aethel_Tile_Interconnect_Bridge (
    input  wire        clk,                  // Tile Synchronous Local Clock
    input  wire        rst_n,                // Active-Low Hardware Reset
    input  wire [15:0] local_edge_coord,     // Boundary particle position from local tile (Q8.8)
    input  wire [15:0] rx_optical_link,      // Inbound coordinate stream from adjacent tile edge
    output reg  [15:0] tx_optical_link,      // Outbound optical lane transmitter register
    output reg         handoff_trigger       // Signals coordinate handoff across tile boundary
);

    // Hyperbolic Boundary Threshold (Set at 0.95 inside the Poincaré Disk)
    localparam [15:0] BOUNDARY_THRESHOLD = 16'h00F3; 

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            tx_optical_link <= 16'h0000;
            handoff_trigger <= 1'b0;
        end else begin
            // Continuously stream current edge tracking state out through the optical lane
            tx_optical_link <= local_edge_coord;

            // If a local particle's coordinate passes the boundary threshold,
            // execute an instantaneous hardware handoff to the neighboring tile.
            if (local_edge_coord > BOUNDARY_THRESHOLD) begin
                handoff_trigger <= 1'b1;
            end else begin
                handoff_trigger <= 1'b0;
            end
        end
    end

endmodule
