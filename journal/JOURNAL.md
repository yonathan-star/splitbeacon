# SplitBeacon existing design notes

These existing design notes were confirmed by the project owner on November 1, 2026 as accurately describing 20 actual hours of work, using the existing 3, 4, 5, 5 and 3-hour allocations. They are entered retrospectively; individual session dates were not supplied. No additional work or results are invented.

## Entry 1 — choosing a useful display

I wanted a display with a job beyond playing an animation. A timer for repeated practice gives the lights a clear meaning: how far through the current interval I am, and how the completed split compares with the goal. I looked through the Displays guides and opened pixelixx, Modular Led Matrix and DAYFRAME. A sound-reactive matrix was already represented, so I moved away from that direction and developed SplitBeacon. The result is a training display with a target knob, lap button, and visible split history.

Evidence: README.md and preview/splitbeacon.png. Owner-confirmed actual time: 3 hours.

## Entry 2 — designing around available parts

The first matrix and rotary encoder choices were unavailable. I replaced them with two in-stock 4x8 FeatherWings and a linear potentiometer. That changed the interface in a useful way: the target can be read directly from an analog input. The separate brightness pot gives a physical override while a photocell handles room brightness. I kept a small TFT for exact timing so the matrix does not need to squeeze numbers into a tiny grid.

The Wing already includes a level shifter. Its DIN pad is the shifted output, so the Pico must connect to the default #6 control pad. I gave each Wing its own GPIO instead of chaining through uncertain module routing.

Evidence: BOM.md, docs/WIRING.md and the actual cart screenshots. Owner-confirmed actual time: 4 hours.

## Entry 3 — controller and power

I laid out a 100x100mm controller with three switches, the Pico, harness headers, analog inputs and protected power. External 5V feeds the display rail through a 500mA resettable fuse. A Schottky diode feeds VSYS while allowing the Pico’s own USB path to remain isolated. The pixel channels have a software ceiling of 16/255 because unrestricted white would exceed the intended load.

The supplier’s bulk capacitor dimensions were 10mm diameter and 5mm lead pitch. I corrected that footprint before the final routing and exports. The final PCB routes all 69 planned links and the DRC report contains no violations or unconnected pads. A separate netlist comparison checks all 88 connected logical pins.

Evidence: hardware/controller, hardware/SplitBeacon-gerbers.zip and verification reports. Owner-confirmed actual time: 5 hours.

## Entry 4 — timing behavior

The timer counts only running time, so pausing does not contaminate a split. I made the current lap latch its target when it starts: changing the knob during that lap changes the next target. This avoids a misleading result where moving the knob rewrites the comparison just before recording. The firmware rejects extremely short duplicate splits, debounces buttons, bounds the saved history, and validates restored records.

Ten portable tests cover these rules and the RGB cap. The display driver and main loop are included, but successful logic tests do not establish that the physical TFT or matrix has been tested.

Evidence: firmware and verification/firmware-tests.txt. Owner-confirmed actual time: 5 hours.

## Entry 5 — enclosure and handoff

I designed a removable lid with two matrix windows, the TFT opening, target and brightness holes, light sensing, and three captive switch plungers. Printed retainers avoid adhesive on the displays. A tolerance coupon lets the actual printer decide the final plunger clearance. The case includes a cable entry and vents, with the Pico accessible when the lid is removed.

I reconciled complete pack quantities and the full filament spool against actual carts. The total exceeds the grant once all purchases are counted, so I left that gap visible. The package ends with assembly instructions and a bench checklist rather than claiming a physical build.

Evidence: mechanical, docs/ASSEMBLY.md and BOM.md. Owner-confirmed actual time: 3 hours.
