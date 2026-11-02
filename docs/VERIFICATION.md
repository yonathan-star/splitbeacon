# Verification record

## Completed design checks

- KiCad 7.0.11 loads and exports the schematic and board.
- Final controller DRC: zero violations, zero unconnected pads, zero footprint errors. Original report: verification/controller-drc.txt.
- 88 connected logical pin mappings agree between schematic export, design manifest, and PCB. Explicit NC pins are excluded.
- Ten CPython tests pass: pause behavior, target latching, repeat-cue suppression, bounded history, debounce, pixel mapping uniqueness, channel caps, corrupt history rejection, ADC endpoints and stopped-lap rejection.
- All three firmware files pass Python syntax compilation. Device-specific machine/framebuf/neopixel APIs require MicroPython.
- Six printable parts exported through OpenSCAD as simple solids.
- Vendor carts verified quantities and price. JLCPCB detected the earlier 100x100mm two-layer Gerber set. The final capacitor-footprint correction was re-exported locally. The saved quote is based on dimensions; the final ZIP has not received a retained vendor DFM review.

## Power estimate

At the channel ceiling of 16, a conservative RGB die model gives 64 x 60mA x 16/255 = 241mA plus an assumed 64mA pixel idle allowance. Allow another 100mA for Pico, TFT and controls: approximately 405mA. The 500mA hold PTC has limited headroom and derates with temperature. Never bypass the firmware channel cap. Measure real full-frame current and enclosure temperature before routine operation. At warm ambient, lower the cap if the PTC warms or nuisance-trips.

The PCB uses 0.3mm tracks and 0.8/0.4mm vias. It is designed around the capped load rather than the 3.84A full-white maximum of 64 unbounded pixels. The 4A PSU capacity is not permission to exceed board/fuse limits.

## Bench tests not performed

Check every rail and polarity, switch-pin orientation, cold start, 15-minute timer accuracy against a reference, pause/resume, 65+ laps, target changes mid-lap, dark/bright sensor response, matrix pixel order, TFT color/orientation/offsets, save/restart, simulated interrupted save, PSU/USB isolation, full capped-frame current, PTC warming, wire retention and enclosure fit. The ST7789 landscape offsets are x40/y53 with MADCTL 0x60; verify against the purchased module before final use.

Electrical ERC is not claimed: schematic symbols expose explicit logical pins but use passive pin types. Physical build, optical behavior, sound level and tolerances remain unverified.
