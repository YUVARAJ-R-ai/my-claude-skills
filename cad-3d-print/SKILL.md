---
name: cad-3d-print
description: Design parametric 3D printable models, mechanical parts, brackets, adapters, and enclosures using OpenSCAD, compile them into STL/3MF, and verify fit tolerances. Use when the user requests 3D CAD modeling, 3D printing design, or STL generation.
trigger: /cad-3d-print
---

# /cad-3d-print

Expert parametric 3D CAD design for FDM 3D printing using OpenSCAD, automated CLI compilation, and slicing preparation.

## Quick Reference & Resources
- **Fit & Hole Standards**: [references/3d-printing-rules.md](./references/3d-printing-rules.md)
- **Reference Implementation**: [examples/parametric-enclosure.scad](./examples/parametric-enclosure.scad)
- **Compile Helper Script**: [scripts/render-model.sh](./scripts/render-model.sh)

---

## Workflow Instructions

### Phase 1: Clarify Requirements & Mechanical Constraints
Before generating code, verify key dimensional constraints:
1. **Dimensions & Clearance**: Overall length, width, height (in mm). Check whether fit is press-fit (0.1mm), snug-fit (0.2mm), or sliding (0.4mm).
2. **Mounting & Fasteners**: Screw sizes (M2, M2.5, M3, M4) and hole types (clearance through-hole, plastic tap hole, or heat-set insert cavity). Consult [3d-printing-rules.md](./references/3d-printing-rules.md).
3. **Printing Orientation & Overhangs**: Keep overhang angles $\le 45^\circ$ from vertical. Avoid unsupported horizontal overhangs or use chamfers / teardrop geometry.

---

### Phase 2: Write Parametric OpenSCAD Code
Always follow these engineering standards when writing `.scad` files:
1. **Top-Level Parameters**: All user-tweakable dimensions must be named variables declared at the very top of the file:
   ```scad
   // --- Dimensions (mm) ---
   inner_width  = 50.0;
   inner_length = 80.0;
   wall_thick   = 2.4;
   tolerance    = 0.3;
   ```
2. **Facet Resolution**:
   ```scad
   $fn = $preview ? 32 : 96;
   ```
3. **Epsilon Offset for Clean Booleans**:
   Never cut coincident faces. Define `eps = 0.02;` and expand cutout dimensions by `2 * eps` with a `-eps` translation to ensure watertight, manifold geometry without zero-thickness artifacts.
4. **Modularity**: Break complex parts into distinct `module` definitions (e.g., `mounting_tab()`, `pcb_standoff()`, `lid()`).

---

### Phase 3: Automated CLI Compilation & Verification
Use OpenSCAD's CLI or the bundled helper script to compile the model:

```bash
# Using the helper script:
~/.gemini/config/skills/cad-3d-print/scripts/render-model.sh model.scad model.stl --image

# Or directly via openscad:
openscad -o model.stl model.scad
```

Verify that:
- No OpenSCAD syntax or CGAL geometry errors are reported.
- Facets count is reasonable and rendering time finishes cleanly.
- The `.stl` file is created with non-zero size.

---

### Phase 4: Preview & Slicing
Prompt the user with quick commands to inspect and slice:
- **Instant Preview**: `fstl model.stl`
- **Slicing for Printer**: `orca-slicer model.stl`
