# 3D Printing & CAD Design Guidelines (FDM)

Reference rules for designing functional, 3D printable mechanical parts and enclosures in OpenSCAD.

---

## 1. Fit & Clearance Tolerances (for 0.4mm Nozzle)

| Fit Type | Clearance (per side) | Total Hole/Gap Offset | Typical Use Case |
| :--- | :--- | :--- | :--- |
| **Tight Press Fit** | 0.05 mm – 0.10 mm | +0.1 mm to +0.2 mm | Dowel pins, bearings, embedded magnets |
| **Snug Friction Fit** | 0.15 mm – 0.20 mm | +0.3 mm to +0.4 mm | Snap-fit lids, sliding battery covers |
| **Free-Moving Fit** | 0.30 mm – 0.40 mm | +0.6 mm to +0.8 mm | Hinges, rotating shafts, sliding tracks |
| **Loose Clearance** | 0.50 mm+ | +1.0 mm+ | Cable passthroughs, gross mechanical clearance |

---

## 2. Standard Fastener Hole Sizing (Metric ISO)

When 3D printing holes vertically, plastic shrinkage and polygon approximation cause holes to print slightly smaller than designed. Always use these compensated diameters:

| Screw Size | Close Fit (Through Hole) | Free Fit (Clearance Hole) | Thread Tap Hole (Plastic) | Heat-Set Insert (Outer D x Depth) |
| :--- | :--- | :--- | :--- | :--- |
| **M2** | 2.2 mm | 2.4 mm | 1.8 mm | 3.2 mm x 4.0 mm |
| **M2.5** | 2.7 mm | 3.0 mm | 2.2 mm | 3.6 mm x 4.5 mm |
| **M3** | 3.2 mm – 3.4 mm | 3.6 mm | 2.6 mm | 4.4 mm – 4.6 mm x 5.0 mm |
| **M4** | 4.3 mm – 4.5 mm | 4.8 mm | 3.5 mm | 5.8 mm x 6.0 mm |
| **M5** | 5.3 mm – 5.5 mm | 5.8 mm | 4.4 mm | 7.0 mm x 7.0 mm |

---

## 3. Structural Rules & Printability

1. **Wall Thickness**:
   - Minimum: `1.2 mm` (3 perimeters with 0.4mm nozzle).
   - Robust / Structural: `2.0 mm – 3.0 mm`.
   - Bottom & Top layers: Minimum `1.2 mm` (6 layers at 0.2mm layer height).

2. **The 45° Overhang Rule**:
   - Overhangs steeper than 45° from vertical require support material.
   - Use chamfers (45°) instead of rounded fillets for upward-expanding overhangs.

3. **Horizontal Holes & Teardrops**:
   - For horizontal holes larger than 8mm, use a teardrop profile (45° roof) to prevent roof sagging without supports.

4. **Elephant's Foot Compensation**:
   - Add a `0.5 mm x 45°` chamfer on the bottom edge touching the build plate to prevent first-layer squish from ruining outer dimensions.

---

## 4. OpenSCAD Code Conventions

- **Epsilon Overlap**: Always add a tiny offset (`eps = 0.02`) to cutouts in `difference()` to avoid zero-thickness non-manifold surfaces:
  ```scad
  eps = 0.02;
  difference() {
      cube([20, 20, 10]);
      translate([5, 5, -eps])
          cube([10, 10, 10 + 2 * eps]);
  }
  ```
- **Facet Resolution**:
  ```scad
  $fn = $preview ? 32 : 100; // Fast in preview, high resolution in final export
  ```
- **Parametric Header**: Define all core dimensions at the very top as variables so the user can easily adjust them.
