# Circuit Design & Engineering Reference Rules

Quick rules and calculation tables for designing robust, noise-immune PCBs.

---

## 1. Power Supply & Decoupling Capacitor Rules

1. **Per-Pin Decoupling**:
   - Every single $V_{CC} / V_{DD}$ pin of an IC requires a **100 nF (0.1 µF)** X7R ceramic capacitor placed as physically close to the pin as possible (< 2 mm).
   - Trace route order: `Power Plane / Source` → `Capacitor Pad` → `IC Pin`. Never branch the capacitor off a stub.
2. **Bulk Decoupling**:
   - Place a **10 µF** (or 22 µF) ceramic/tantalum capacitor at the output of every voltage regulator and where power enters the board.
3. **Ferrite Beads**:
   - For analog $V_{DDA}$ / $V_{REF}$ or sensitive RF/ADC supplies, use an LC filter (e.g., `120Ω @ 100MHz Ferrite Bead` + `100nF` + `10µF`).

---

## 2. Standard Subcircuit Golden Rules

### USB-C 2.0 (Device / Sink Mode)
- **CC Pins**: Connect two individual **5.1 kΩ (1% tolerance)** pull-down resistors:
  - `CC1` → 5.1 kΩ → `GND`
  - `CC2` → 5.1 kΩ → `GND`
  - *(Never tie CC1 and CC2 together to one resistor; e-marked cables will fail to power).*
- **D+ / D-**: Keep differential pair length matched within 1.25 mm. Add a TVS ESD protection diode (e.g., USBLC6-2SC6).
- **VBUS**: Add a reverse voltage Schottky diode or P-FET reverse polarity protection if battery powered.

### I2C Bus Pull-Ups
- Standard Mode (100 kHz) & Fast Mode (400 kHz): **4.7 kΩ** pull-ups to $V_{CC}$ on both `SDA` and `SCL`.
- Long cables or noisy environments: **2.2 kΩ** to reduce rise time.

### Microcontroller Reset (NRST / RESET)
- **10 kΩ** pull-up to 3.3V.
- **100 nF** capacitor to GND (filters high-frequency noise glitches).
- Tactile switch across the capacitor pulling NRST to GND.

---

## 3. Copper Trace Sizing (IPC-2152 Standard, 1oz Copper, 10°C Rise)

| Current Capacity | External Layer Trace Width | Internal Layer Trace Width | Typical Usage |
| :--- | :--- | :--- | :--- |
| **< 0.3 A** | 0.20 mm (8 mil) | 0.35 mm (14 mil) | Standard signals, SPI, I2C, UART |
| **0.5 A** | 0.30 mm (12 mil) | 0.60 mm (24 mil) | Sensor power lines |
| **1.0 A** | 0.50 mm (20 mil) | 1.10 mm (43 mil) | MCU main power rail |
| **2.0 A** | 1.20 mm (47 mil) | 2.50 mm (98 mil) | USB 5V VBUS / Motor logic |
| **3.0 A+** | Polygon Pour (Copper Plane) | Polygon Pour (Copper Plane) | High-current power distribution |

---

## 4. Via Current Sizing
- Standard via (0.3 mm drill / 0.6 mm pad) safely carries **~1.2 A** to **1.5 A**.
- For power rails carrying > 1 A, always place **2 to 3 parallel vias** to minimize inductance and resistance.
