# Module: `main.py`
### Master System Coordinator and Execution Loop

```python
import time
import numpy as np
from ui.dashboard import GravityWellDashboard
from firmware.aethel_gravity_well_controller import AethelHarmonicGravityWellController
from firmware.trajectory_generator import BraidTrajectoryPlanner

def run_system_ecosystem(total_cycles=100):
    print("[INIT] Initializing 3-Tier Substrate Hardware Interface...")
    
    # Initialize the core software modules from your repository
    controller = AethelHarmonicGravityWellController(num_nodes=1024)
    planner = BraidTrajectoryPlanner(radius_limit=0.95)
    dashboard = GravityWellDashboard(grid_size=21)
    
    print("[READY] All systems operational. Executing real-time control loop.\n")
    time.sleep(1.5)

    for cycle in range(total_cycles):
        # 1. GENERATE PATHS
        # Use the trajectory generator to calculate the next target step for Node 0
        t = cycle * 0.1
        target_x, target_y = planner.generate_braid_step(time_step=t, node_index=0, braid_type="lissajous")
        
        # 2. READ HARDWARE SENSORS
        # Simulate physical Avalanche Photodiode (APD) current feedback
        # Adds minor random environmental vibration/noise to test stabilization
        rng = np.random.default_rng()
        live_apd_feedback = rng.normal(0.0, 0.2, 1024)
        
        # Force a massive environmental vibration spike at step 30 to test Braid-Shielding
        if cycle == 30:
            live_apd_feedback[0] = 5.5
            print("\n[ALERT] Artificial kinetic disruption pulse injected on Node 0!")

        # 3. ENGAGE THE NEUROMORPHIC ML COPROCESSOR
        # Run the predictive Neural-Warp loop to pre-emptively warp the space
        controller.execute_neural_warp_predictive_loop(live_apd_feedback)
        
        # 4. RUN CLOSED-LOOP PD STABILIZATION
        # Update the register configurations based on sensor input
        controller.update_well_states(live_apd_feedback)
        
        # 5. EXECUTE THE BRAID-SHIELD SAFETY PROTOCOL
        # Check the error bus and instantly reroute if noise thresholds are breached
        controller.execute_braid_shield_reroute(live_apd_feedback)

        # Update our tracking positions inside the script
        controller.braid_trajectory_target_x[0] = target_x
        controller.braid_trajectory_target_y[0] = target_y

        # 6. STREAM TO THE DASHBOARD
        # Clear the terminal and render the live physical movement profile
        dashboard.clear_screen()
        dashboard.render_poincare_disk(target_x, target_y)
        
        # Append telemetry log overlays directly under the interface matrix
        print(f"Cycle: {cycle:03d}/{total_cycles} | Target Vector: ({target_x:+.2f}, {target_y:+.2f})")
        print(f"Node 0 Driver Voltage Output: {controller.micro_led_intensity_register[0]:.2f}V / 5.00V")
        
        if cycle >= 30 and cycle <= 35:
            print("\n[SYSTEM NOTE] Watch the grid closely. The Braid-Shield protocol is actively\n"
                  "              warping the target coordinates away from the center to dodge noise.")
            
        time.sleep(0.1)

if __name__ == "__main__":
    run_system_ecosystem(total_cycles=60)
```
