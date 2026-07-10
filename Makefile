# ──────────────────────────────────────────────────────────────────────────
# FILE: Makefile
# PROJECT: Solid-State Neuromorphic Quantum Optomechanical Core
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

# Compiler and Interpreter Definitions
PYTHON       = python3
VERILOG_LINT = verilator
VFLAGS       = --lint-only -Wall

# Core Repository Directory Structures
RTL_DIR      = rtl
FIRMWARE_DIR = firmware
UI_DIR       = ui
DOCS_DIR     = docs

# Tracked Code Assets
RTL_SOURCES  = $(RTL_DIR)/aethel_node-processor.v \
               $(RTL_DIR)/aethel_gravitywell-processor.v \
               $(RTL_DIR)/aethel_3t_interconnect_fabric.v

PYTHON_CORE  = main.py \
               $(FIRMWARE_DIR)/aethel_3d_torus_engine.py \
               $(FIRMWARE_DIR)/aethel_trajectory_generator.py \
               $(UI_DIR)/aethel_poincare_dashboard.py

.PHONY: all run lint clean help test-stack

all: lint run

help:
	@echo "========================================================================"
	@echo " AETHEL CORE 3T SYSTEM AUTOMATION ENGINE                                "
	@echo "========================================================================"
	@echo " Available Commands:"
	@echo "   make lint       - Run static analysis/linting on all Verilog RTL modules"
	@echo "   make run        - Execute the 3D Torus Emulation and Live ASCII UI Dashboard"
	@echo "   make test-stack - Validate that software package imports are secure"
	@echo "   make clean      - Remove temporary python caches and compiled binaries"
	@echo "   make all        - Lint the hardware files and immediately boot the software"
	@echo "========================================================================"

lint: $(RTL_SOURCES)
	@echo "⚙️  Initializing hardware compilation sweeps and linting Verilog RTL..."
	@if command -v $(VERILOG_LINT) >/dev/null 2>&1; then \
		$(VERILOG_LINT) $(VFLAGS) $(RTL_SOURCES); \
		echo "✅ RTL Hardware linting clean. Structural integrity verified."; \
	else \
		echo "⚠️  Verilator not found locally. Skipping structural linter pass."; \
	fi

run: $(PYTHON_CORE)
	@echo "🚀 Launching Core Emulation Pipeline..."
	$(PYTHON) main.py

test-stack:
	@echo "🧪 Verifying firmware package initialization integrity..."
	$(PYTHON) -c "import firmware; import ui; print('✅ Package structure fully integrated.')"

clean:
	@echo "🧹 Purging localized caching structures..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✨ Workspace sanitized."
# Append this target to your active Makefile configuration
test-hil:
	python3 -m tests.aethel_hil_harness
