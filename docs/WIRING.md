# Wiring and pin map

Controller pin 1 is the square pad. Headers are signal harnesses; they do not imply the module uses the same physical order. Follow module labels. Disconnect power while wiring.

| Controller | Destination |
|---|---|
| J1 pin1 / pin2 | regulated 5V positive / ground from the 2.1mm adapter |
| J2 pin1 / pin2 / pin3 | left FeatherWing USB power / GND / default Feather control pin #6 |
| J8 pin1 / pin2 / pin3 | right FeatherWing USB power / GND / default Feather control pin #6 |
| J3 pins1–9 | TFT VIN, GND, SCK, MOSI, CS, DC, RST, LITE, SO respectively |
| J4 pins1–3 | target pot outer terminal +3V3, wiper, other outer GND |
| J5 pins1–3 | brightness pot outer +3V3, wiper, other outer GND |
| J6 pins1–2 | passive piezo positive, ground |
| J7 pins1–2 | LDR terminals, nonpolar |

FeatherWing DIN is the **level-shifted output**, so connect GPIO to the default #6 control pad, not to DIN. Leave BAT and DOUT unconnected. Keep its default jumper closed. Supply both Wings independently from J2/J8. Do not stack them on the Pico.

| Pico GPIO | Physical pin | Function |
|---|---:|---|
| GP5 / GP6 / GP7 | 8 / 9 / 10 | RUN / LAP / VIEW, active low with internal pullups |
| GP8 | 12 | piezo PWM through R5 1k |
| GP11 | 15 | TFT backlight PWM |
| GP12 / GP13 | 17 / 18 | TFT DC / reset |
| GP14 / GP15 | 19 / 20 | right / left RGB data through 330R |
| GP16 / GP17 / GP18 / GP19 | 21 / 22 / 24 / 25 | TFT SO / CS / clock / MOSI |
| GP26 / GP27 / GP28 | 31 / 32 / 34 | brightness / ambient / target ADC |
| 3V3 OUT / GND / VSYS | 36 / 38 / 39 | regulated logic / ground / diode-isolated external power |

D1 banded cathode goes toward VSYS. C3 positive goes to +5V_DISPLAY; its striped negative lead goes to ground. Never feed external power into Pico VBUS. The PTC is not reverse-polarity protection. Check adapter polarity before insertion.

The LDR and 10k R4 form a divider from 3.3V to ground. More light raises GP27. C4/C5 filter brightness and ambient readings. Target is read directly from the second 10k pot.
