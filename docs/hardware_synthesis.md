# Document: `docs/hardware_synthesis.md`
### FPGA Compilation Pipeline and Vivado Implementation Instructions

```text
1. TOOLCHAIN REQUIREMENT
* Synthesis Suite: AMD/Xilinx Vivado Design Suite (v2024.1 or newer)
* Target Hardware: Xilinx Zynq UltraScale+ Core (XCZU9EG)

2. PROJECT INGESTION PROTOCOL
* Step A: Create a new RTL Project in Vivado.
* Step B: Target the directory containing your synthesizable logic cores:
  - rtl/Aethel_Gravity_Well_Node_Processor.v
  - rtl/Aethel_Tile_Interconnect_Bridge.v
  - rtl/Aethel_Neural_Warp_Coprocessor.v
* Step C: Import the constraints module:
  - rtl/Aethel_Hardware_Constraints.xdc

3. SYNTHESIS AND BITSTREAM GENERATION
* Run Synthesis to map logic components directly to look-up tables (LUTs) and block RAM.
* Run Implementation to route logical interconnects along the hardware constraints.
* Generate Bitstream (.bit file) to flash onto the physical FPGA board to initialize the 3T substrate.
```
