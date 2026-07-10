`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Module Name: aethel_3t_interconnect_fabric
// Description: Top-level routing matrix enforcing wrapped 3-Torus boundary 
//              conditions for a localized grid cluster of node processors.
//////////////////////////////////////////////////////////////////////////////////

module aethel_3t_interconnect_fabric #(
    parameter GRID_SIZE = 4, // 4x4x4 local hardware cluster example
    parameter BIT_WIDTH = 32
)(
    input wire clk,
    input wire rst_n,
    
    // Flattened array of potentials from the macro gravitywell processor
    input wire [BIT_WIDTH*GRID_SIZE*GRID_SIZE*GRID_SIZE-1:0] flat_potentials,
    output reg [BIT_WIDTH*GRID_SIZE*GRID_SIZE*GRID_SIZE-1:0] routed_velocities
);

    // Coordinate mapping and routing logic executed in parallel
    genvar x, y, z;
    generate
        for (x = 0; x < GRID_SIZE; x = x + 1) begin: gen_x
            for (y = 0; y < GRID_SIZE; y = y + 1) begin: gen_y
                for (z = 0; z < GRID_SIZE; z = z + 1) begin: gen_z
                    
                    // Derive wrapped indices for neighbors using modulo math
                    localparam EAST_X  = (x + 1) % GRID_SIZE;
                    localparam WEST_X  = (x - 1 < 0) ? GRID_SIZE - 1 : x - 1;
                    
                    wire [BIT_WIDTH-1:0] local_pot_east;
                    wire [BIT_WIDTH-1:0] local_pot_west;
                    wire [BIT_WIDTH-1:0] out_vel_x;
                    
                    // Slice the flattened input bus to extract neighbor potentials
                    assign local_pot_east = flat_potentials[((EAST_X * GRID_SIZE * GRID_SIZE) + (y * GRID_SIZE) + z) * BIT_WIDTH +: BIT_WIDTH];
                    assign local_pot_west = flat_potentials[((WEST_X * GRID_SIZE * GRID_SIZE) + (y * GRID_SIZE) + z) * BIT_WIDTH +: BIT_WIDTH];
                    
                    // Instantiate a node processor for every point in the structural fabric
                    aethel_node_processor #(
                        .BIT_WIDTH(BIT_WIDTH),
                        .FRAC_WIDTH(16)
                    ) node_inst (
                        .clk(clk),
                        .rst_n(rst_n),
                        .potential_east(local_pot_east),
                        .potential_west(local_pot_west),
                        .ramanujan_scale(32'h00010000), // Normalized 1.0 fixed-point placeholder
                        .local_ternary_state(2'b01),
                        .neighbor_ternary_state(2'b00),
                        .resolved_velocity_x(out_vel_x),
                        .godel_anomaly_alert()
                    );
                    
                    // Bind the resolved node calculations back to the master tracking bus
                    always @(posedge clk) begin
                        routed_velocities[((x * GRID_SIZE * GRID_SIZE) + (y * GRID_SIZE) + z) * BIT_WIDTH +: BIT_WIDTH] <= out_vel_x;
                    end
                end
            end
        end
    endgenerate

endmodule
