# Regenerating design files

Use KiCad 7 with its pcbnew Python module and standard footprint library. The generator requires the footprint library path in its LIB setting; update that location for another workstation. Run build_hardware.py, then route.py on the placed board, then export schematics/netlists/Gerbers and drills with kicad-cli. Regenerating replaces the edited board, so keep hand edits in a separate copy. Never run the router twice on existing routes.

Run verification/test_core.py with CPython for the portable behavior tests. MicroPython on a real Pico is required for the complete application. Open enclosure.scad with OpenSCAD and select its part variable for print exports.
