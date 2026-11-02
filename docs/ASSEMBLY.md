# Assembly, printing and firmware

1. Print the tolerance coupon first. Base and lid each need one copy; matrix retainer two copies; short retainer two copies; plunger three copies. Use 0.2mm layers, 3 walls, 20% infill, ordinary PLA. Print the lid external face down and the base open side up. Use the filament maker’s temperature range.
2. Inspect the bare board, check power-to-ground resistance, and solder resistors, diode, capacitors, PTC and switches. Match C3 polarity and D1 band. Solder Pico with its supplied headers directly to the board, USB end at the top of the PCB.
3. Fit 27 header pins to J1-J8 using spare supplied FeatherWing headers. Fit just the three required pins to each Wing and the supplied TFT header. Prepare female harnesses. Solder and insulate pot/sensor ends rather than relying on loose bare leads.
4. Fasten the PCB at enclosure coordinates (18,42), (110,42), (18,134), (110,134) with four M3x6 screws. Printed bosses support the PCB bottom at z6mm. Do not overtighten pilot holes.
5. Fit the Wings side by side behind the two upper windows, with equal orientation. Two long retainer strips use four screws. Fit the TFT behind its window using two short strips and four screws. Panel pots fit the two 7.6mm holes. Fit the LDR at the 5.2mm opening. The piezo sits behind the vent holes; secure with an insulated wire loop through the vents.
6. Insert three plungers from inside the lid. Their retaining flanges prevent them from falling out. Fit should allow free return without pressing the switches at rest. The 31.8mm design length assumes a switch top at z12mm and cap top at z44mm; trim stems after measuring the actual switch stack. This fit has not been physically checked.
7. Route the two power wires through the side entry and form a strain-relief knot inside before connecting the external terminal adapter. Keep solder joints insulated. Connect harnesses from WIRING.md and retain wire slack away from switch stems.
8. Flash the official Raspberry Pi Pico MicroPython UF2 in BOOTSEL mode. Copy main.py, core.py and st7789.py into the Pico filesystem using Thonny or mpremote. No third-party Python libraries are required. Select the RP2040 Pico build, not Pico 2.
9. First power the controller with displays unplugged. Verify 5V input, diode-fed VSYS and 3.3V. Then power down, attach TFT, and test RGB one panel at a time. Confirm pixel order with a walking-pixel test before comparing the visualization to hardware.
10. Run the bench checklist in VERIFICATION.md. Fit the lid using four M3x6 screws only after wiring and plungers move freely. USB programming requires removing the lid.

MicroSD is unused and no card is needed. This enclosure is a dry indoor desk device and has no water-resistance claim.

Official module references: [FeatherWing pinouts](https://learn.adafruit.com/adafruit-neopixel-featherwing/pinouts), [TFT guide](https://learn.adafruit.com/adafruit-1-14-240x135-color-tft-breakout?view=all), [Pico MicroPython download](https://micropython.org/download/RPI_PICO/).
