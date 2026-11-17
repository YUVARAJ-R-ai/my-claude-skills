---
name: pcb-design
description: Design printed circuit boards (PCBs) and electronic circuits, calculate passive components, generate KiCad schematics, script component placement via Python (pcbnew), route traces using Freerouting, run DRC, and export manufacturing packages (Gerbers, Drill, BOM, CPL, STEP) for JLCPCB/PCBWay. Use when the user requests PCB design, schematic creation, circuit calculation, or PCB manufacturing export.
trigger: /pcb-design
---

# /pcb-design

End-to-end electronic circuit and PCB design workflow using KiCad, Python scripting (`pcbnew`), Freerouting, and automated CLI manufacturing export.

## Quick Reference & Resources
- **Circuit Design & Component Calculations**: [references/circuit-calculators.md](./references/circuit-calculators.md)
- **Fab Rules & BOM/CPL Specs (JLCPCB/PCBWay)**: [references/manufacturing-specs.md](./references/manufacturing-specs.md)
- **Automated Export Script (`kicad-cli`)**: [scripts/kicad-export.sh](./scripts/kicad-export.sh)
- **Auto-Router Launcher**: [scripts/run-freerouting.sh](./scripts/run-freerouting.sh)
- **Parametric Placement Script**: [examples/placement-script.py](./examples/placement-script.py)

---

## Workflow Instructions

### Phase 1: Clarify Circuit Requirements & Architecture
Before generating schematic or layout files:
1. **Power Budget**: Source voltage (USB 5V, LiPo 3.7V, 12V DC barrel) and operating rails (3.3V, 1.8V, 5V). Select appropriate LDO (e.g., AMS1117, XC6206, ME6211) or Buck Converter (e.g., MP2315).
2. **Core ICs**: Microcontrollers (ESP32-C3/S3, RP2040, STM32), sensors, and communication buses (I2C, SPI, UART).
3. **Connectors & Protection**: USB-C CC 5.1kΩ pull-downs, TVS diodes for ESD protection on data lines, reverse polarity P-FET or Schottky diodes.
4. **LCSC Part Numbers**: Prefer components from the JLCPCB Basic Library to minimize setup fees. Consult [manufacturing-specs.md](./references/manufacturing-specs.md).

---

### Phase 2: Schematic Capture & Calculation
Follow the golden circuit rules in [circuit-calculators.md](./references/circuit-calculators.md):
- Place **100 nF** ceramic decoupling capacitor right at each power pin of every IC.
- Add bulk **10 µF** capacitor at regulator outputs.
- Add **4.7 kΩ** pull-up resistors on `SDA` and `SCL` lines.
- Calculate LED series resistors: $R = \frac{V_{CC} - V_F}{I_F}$ (typically 330Ω to 1kΩ for indicators).
- Format and organize nets logically into functional blocks (Power, MCU, USB/Comm, Peripherals).

---

### Phase 3: Board Layout & Parametric Placement
1. **Board Outline (Edge.Cuts)**: Define exact dimensions, corner radiuses, and mounting hole positions (e.g., M3 clearance holes = 3.2mm diameter, placed 4mm from corners).
2. **Connector & Edge Constraints**: Place edge connectors (USB-C, pin headers, barrel jacks) precisely on the board perimeter.
3. **Parametric Layout**: For repetitive components (e.g., circular LED rings, keyboard switch matrices), use or adapt [examples/placement-script.py](./examples/placement-script.py).

---

### Phase 4: Trace Routing & Auto-Routing
1. **Trace Widths**:
   - Signal traces: `0.20 mm` (8 mil).
   - MCU / Sensor power: `0.30 mm – 0.50 mm` (12 – 20 mil).
   - Ground: Use unbroken solid copper plane on the bottom layer (B.Cu).
2. **Auto-routing via Freerouting**:
   - In KiCad PCB Editor: **File → Export → Specctra DSN**.
   - Run:
     ```bash
     ~/.gemini/config/skills/pcb-design/scripts/run-freerouting.sh board.dsn
     ```
   - In KiCad PCB Editor: **File → Import → Specctra Session (`board.ses`)**.

---

### Phase 5: DRC & Manufacturing Export (`kicad-cli`)
Run the export helper script to produce the complete fab package:

```bash
~/.gemini/config/skills/pcb-design/scripts/kicad-export.sh path/to/board.kicad_pcb ./output
```

This automatically generates:
- `drc_report.txt`: Design Rule Check results.
- `*_gerbers.zip`: Production-ready Gerber & drill archive for JLCPCB/PCBWay.
- `*_cpl.csv`: Pick-and-Place centroid file for SMT assembly.
- `*.step`: 3D STEP model of the populated board.

---

### Phase 6: Enclosure Co-Design
Feed the exported `*.step` model or board outline dimensions directly into the `/cad-3d-print` skill to generate a custom 3D-printed enclosure matching your board's standoffs, port openings, and button cutouts.
