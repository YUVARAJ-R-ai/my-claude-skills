# PCB Manufacturing & SMT Assembly Reference Rules

Fabrication guidelines optimized for standard fast-turn fabs (JLCPCB, PCBWay, OSHPark).

---

## 1. Standard Fabrication Capabilities (Low-Cost / High-Yield)

| Parameter | Recommended Safe Value | Absolute Minimum Limit |
| :--- | :--- | :--- |
| **Board Thickness** | 1.6 mm (Standard) / 1.0 mm | 0.6 mm |
| **Copper Weight** | 1 oz (35 µm) | 2 oz (costs extra) |
| **Trace Width / Spacing** | 0.15 mm / 0.15 mm (6 mil / 6 mil) | 0.127 mm (5 mil) |
| **Via Drill Diameter** | 0.3 mm (12 mil) | 0.25 mm |
| **Via Annular Ring** | $\ge 0.15$ mm (6 mil) | 0.13 mm |
| **Silkscreen Text Height** | $\ge 1.0$ mm | 0.8 mm |
| **Silkscreen Line Width** | $\ge 0.15$ mm | 0.12 mm |
| **Board Edge Clearance** | $\ge 0.3$ mm (Copper to Edge) | 0.2 mm |

---

## 2. JLCPCB SMT Assembly Preparation

When designing for automated Surface Mount Technology (SMT) assembly, prepare these three files:

### 1. Gerber Files (`.zip`)
Export RS-274X Gerbers and Excellon drill files containing:
- Copper layers (`.gtl`, `.gbl`)
- Solder mask (`.gts`, `.gbs`)
- Silkscreen (`.gto`, `.gbo`)
- Mechanical outline / Edge Cuts (`.gko` or `.gm1`)
- Drill file (`.drl`)

### 2. Bill of Materials (BOM) Format (`bom.csv`)
Must include the following CSV columns:
```csv
Comment,Designator,Footprint,LCSC Part #
100nF,C1 C2 C3,C_0402_1005Metric,C1525
10uF,C4,C_0805_2012Metric,C15850
5.1k,R1 R2,R_0402_1005Metric,C25905
ESP32-S3-WROOM-1-N8,U1,RF_Module:ESP32-S3-WROOM-1,C2913200
```
> **Tip**: Choose components from the **JLCPCB Basic Library** when possible to avoid the $3.00/reel extended loading fee.

### 3. Component Placement List (CPL / Centroid) Format (`cpl.csv`)
Defines the pick-and-place location and rotation for each component:
```csv
Designator,Val,Package,Mid X,Mid Y,Rotation,Layer
C1,100nF,0402,25.40,12.70,0,Top
U1,ESP32-S3,Module,30.00,20.00,90,Top
```
> **Watch Out for Pin 1 Rotations**: Verify in the fab's 3D/2D DFM viewer that polarized components (diodes, ICs, USB-C) match the orientation of pin 1.
