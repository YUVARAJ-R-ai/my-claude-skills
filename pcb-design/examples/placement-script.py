#!/usr/bin/env python3
"""
Parametric PCB Component Placement Script
Uses KiCad's pcbnew Python API to parametrically position components on a board.
Can be executed from terminal: python3 placement-script.py <board.kicad_pcb>
"""

import sys
import math

try:
    import pcbnew
except ImportError:
    print("Notice: 'pcbnew' Python module not found in the current Python environment.")
    print("In NixOS, run using the kicad python environment or 'nix-shell -p kicad --run python3'.")
    sys.exit(0)

def arrange_circular_leds(board, center_x_mm, center_y_mm, radius_mm, led_prefix="D", count=8):
    """Positions an array of LEDs in an exact circle with outward radial orientation."""
    angle_step = 2 * math.pi / count
    for i in range(count):
        ref = f"{led_prefix}{i+1}"
        footprint = board.FindFootprintByReference(ref)
        if footprint is None:
            print(f"Warning: Footprint '{ref}' not found on board.")
            continue
        
        angle = i * angle_step
        x = center_x_mm + radius_mm * math.cos(angle)
        y = center_y_mm + radius_mm * math.sin(angle)
        
        # KiCad internal coordinates are in nanometers (1 mm = 1,000,000 nm)
        footprint.SetPosition(pcbnew.VECTOR2I(int(x * 1e6), int(y * 1e6)))
        
        # Set orientation facing outward
        deg = math.degrees(angle)
        footprint.SetOrientationDegrees(deg)
        print(f"Placed {ref} at ({x:.2f}mm, {y:.2f}mm), angle {deg:.1f}°")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 placement-script.py <path-to-board.kicad_pcb>")
        sys.exit(1)
        
    pcb_path = sys.argv[1]
    board = pcbnew.LoadBoard(pcb_path)
    
    print(f"Board loaded: {pcb_path}")
    print("Arranging components...")
    
    # Example: Arrange D1 through D8 in a 20mm radius circle at center (50mm, 50mm)
    arrange_circular_leds(board, 50.0, 50.0, 20.0, "D", 8)
    
    board.Save(pcb_path)
    print(f"✔ Board updated and saved: {pcb_path}")

if __name__ == "__main__":
    main()
