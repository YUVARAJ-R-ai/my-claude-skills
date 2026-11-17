// Parametric Project Enclosure Example
// Demonstrates clean OpenSCAD practices: modularity, clearance tolerances, and epsilon offsets.

$fn = $preview ? 32 : 80;
eps = 0.02;

// --- Parametric Dimensions (all in mm) ---
inner_length  = 70.0;
inner_width   = 45.0;
inner_height  = 25.0;
wall_thick    = 2.0;
corner_radius = 3.0;

// PCB Standoffs
pcb_standoff_h = 4.0;
pcb_screw_d    = 2.8; // M3 tap fit

// Calculate outer dimensions
outer_length = inner_length + 2 * wall_thick;
outer_width  = inner_width + 2 * wall_thick;
outer_height = inner_height + wall_thick;

// --- Helper: Rounded Box ---
module rounded_box(l, w, h, r) {
    translate([r, r, 0])
    minkowski() {
        cube([l - 2*r, w - 2*r, h / 2]);
        cylinder(r=r, h=h / 2);
    }
}

// --- Main Enclosure Base ---
module enclosure_base() {
    difference() {
        // Outer Shell
        rounded_box(outer_length, outer_width, outer_height, corner_radius);
        
        // Inner Cavity (offset by wall thickness and eps)
        translate([wall_thick, wall_thick, wall_thick])
            cube([inner_length, inner_width, inner_height + eps]);
    }
    
    // Internal Standoffs (4 corners)
    standoff_offsets = [
        [wall_thick + 5, wall_thick + 5],
        [outer_length - wall_thick - 5, wall_thick + 5],
        [wall_thick + 5, outer_width - wall_thick - 5],
        [outer_length - wall_thick - 5, outer_width - wall_thick - 5]
    ];
    
    for (pos = standoff_offsets) {
        translate([pos[0], pos[1], wall_thick])
        difference() {
            cylinder(d=6.0, h=pcb_standoff_h);
            translate([0, 0, -eps])
                cylinder(d=pcb_screw_d, h=pcb_standoff_h + 2*eps);
        }
    }
}

// Render the base
enclosure_base();
